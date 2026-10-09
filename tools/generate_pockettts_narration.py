#!/usr/bin/env python3
"""Generate episode narration through VoiceStudio's PocketTTS sidecar.

Repository source of truth:
  config/voice_production.json
  docs/VOICE_PRODUCTION.md

This intentionally bypasses VoiceStudio POST /generate. VoiceStudio is only
used to resolve/export the saved voice profile when no local reference WAV is
available.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import time
import urllib.request
import wave
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "voice_production.json"
DEFAULT_EPISODE = ROOT / "episodes" / "MLI-001"
MAX_FRAME_BYTES = 64 * 1024 * 1024


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def expand_env_path(value: str) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(value)))


def fetch_json(url: str, timeout: float = 10.0):
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def download(url: str, destination: Path, timeout: float = 30.0) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=timeout) as response:
        destination.write_bytes(response.read())


def resolve_reference(
    config: dict,
    episode: Path,
    explicit_reference: str | None,
    api_base: str,
) -> Path:
    if explicit_reference:
        path = Path(explicit_reference).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"Reference WAV not found: {path}")
        return path

    runtime_name = config["voice"]["reference_runtime_filename"]
    cached = episode / "media" / runtime_name
    if cached.is_file():
        print(f"[REF] Using cached reference: {cached}")
        return cached

    profile_name = config["voice"]["name"]
    try:
        profiles = fetch_json(f"{api_base}/profiles")
    except Exception as exc:
        raise RuntimeError(
            f"Reference WAV is not cached and VoiceStudio profiles could not be read "
            f"from {api_base}. Start VoiceStudio or pass --reference. Root error: {exc}"
        ) from exc

    matches = [p for p in profiles if p.get("name") == profile_name]
    if not matches:
        raise RuntimeError(f"VoiceStudio profile not found: {profile_name!r}")

    profile = matches[0]
    audio_url = profile.get("audio_url")
    if not audio_url:
        raise RuntimeError(f"VoiceStudio profile {profile_name!r} has no audio_url")

    if audio_url.startswith("http://") or audio_url.startswith("https://"):
        url = audio_url
    else:
        url = f"{api_base}{audio_url}"

    print(f"[REF] Exporting VoiceStudio profile {profile_name!r} -> {cached}")
    download(url, cached)
    return cached


def send_frame(proc: subprocess.Popen, payload: dict) -> None:
    assert proc.stdin is not None
    body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    proc.stdin.write(struct.pack("!I", len(body)))
    proc.stdin.write(body)
    proc.stdin.flush()


def recv_frame(proc: subprocess.Popen) -> dict:
    assert proc.stdout is not None
    header = proc.stdout.read(4)
    if len(header) != 4:
        code = proc.poll()
        raise RuntimeError(f"PocketTTS sidecar closed unexpectedly (exit={code}).")
    (size,) = struct.unpack("!I", header)
    if size > MAX_FRAME_BYTES:
        raise RuntimeError(f"PocketTTS frame too large: {size} bytes")
    body = proc.stdout.read(size)
    if len(body) != size:
        raise RuntimeError("PocketTTS returned a short frame.")
    return json.loads(body.decode("utf-8"))


class PocketTTS:
    def __init__(self, python_exe: Path, sidecar: Path):
        self.python_exe = python_exe
        self.sidecar = sidecar
        self.proc: subprocess.Popen | None = None

    def __enter__(self):
        print(f"[BOOT] PocketTTS sidecar: {self.sidecar}")
        self.proc = subprocess.Popen(
            [str(self.python_exe), str(self.sidecar)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=None,
            env=os.environ.copy(),
        )
        ready = recv_frame(self.proc)
        if ready.get("op") != "ready":
            raise RuntimeError(f"Unexpected PocketTTS startup frame: {ready}")
        print(
            f"[READY] {ready.get('engine', 'pockettts')} "
            f"{ready.get('sample_rate', '?')} Hz"
        )
        return self

    def synthesize(self, text: str, language: str, reference: Path) -> tuple[bytes, int, float, float]:
        if not self.proc:
            raise RuntimeError("PocketTTS sidecar is not running.")

        started = time.perf_counter()
        send_frame(
            self.proc,
            {
                "op": "synthesize",
                "text": text,
                "language": language,
                "ref_audio": str(reference),
            },
        )

        while True:
            msg = recv_frame(self.proc)
            op = msg.get("op")
            if op == "progress":
                print(
                    f"        {msg.get('stage', 'progress')} "
                    f"{msg.get('percent', '?')}%"
                )
                continue
            if op == "error":
                detail = msg.get("message") or "PocketTTS synthesis failed"
                trace = msg.get("traceback")
                if trace:
                    detail += f"\n{trace}"
                raise RuntimeError(detail)
            if op == "audio":
                pcm = base64.b64decode(msg["audio_pcm_b64"])
                sr = int(msg["sample_rate"])
                seconds = int(msg["n_samples"]) / sr
                elapsed = time.perf_counter() - started
                return pcm, sr, seconds, elapsed
            raise RuntimeError(f"Unexpected PocketTTS frame: {msg}")

    def __exit__(self, exc_type, exc, tb):
        if not self.proc:
            return
        try:
            if self.proc.poll() is None:
                send_frame(self.proc, {"op": "shutdown"})
                self.proc.wait(timeout=10)
        except Exception:
            if self.proc.poll() is None:
                self.proc.kill()
                self.proc.wait()
        finally:
            print(f"[EXIT] PocketTTS sidecar exit={self.proc.returncode}")


def semantic_segments(text: str) -> list[str]:
    """Preserve authored paragraph boundaries as narration units."""
    return [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]


def write_wav(path: Path, pcm: bytes, sample_rate: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".part")
    with wave.open(str(temp), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(pcm)
    temp.replace(path)


def read_wav(path: Path) -> tuple[bytes, int]:
    with wave.open(str(path), "rb") as wav:
        if wav.getnchannels() != 1 or wav.getsampwidth() != 2:
            raise RuntimeError(f"Expected mono PCM16 WAV: {path}")
        return wav.readframes(wav.getnframes()), wav.getframerate()


def silence(sample_rate: int, milliseconds: int) -> bytes:
    samples = round(sample_rate * milliseconds / 1000.0)
    return b"\x00\x00" * samples


def build_chunk(
    engine: PocketTTS,
    chunk: dict,
    language: str,
    reference: Path,
    paragraph_pause_ms: int,
) -> tuple[bytes, int]:
    units = semantic_segments(str(chunk["text"]))
    if not units:
        raise RuntimeError(f"Chunk {chunk['id']} has no speakable text.")

    combined = bytearray()
    sample_rate = None
    for index, unit in enumerate(units, start=1):
        print(f"    [UNIT {index}/{len(units)}] {unit[:72]}")
        pcm, sr, audio_seconds, elapsed = engine.synthesize(unit, language, reference)
        print(f"        {audio_seconds:.2f}s audio / {elapsed:.2f}s generation")
        if sample_rate is None:
            sample_rate = sr
        elif sample_rate != sr:
            raise RuntimeError(
                f"Sample rate changed inside chunk {chunk['id']}: "
                f"{sample_rate} -> {sr}"
            )
        combined.extend(pcm)
        if index < len(units):
            combined.extend(silence(sr, paragraph_pause_ms))

    assert sample_rate is not None
    return bytes(combined), sample_rate


def assemble_chunks(
    manifest: dict,
    chunks_dir: Path,
    raw_output: Path,
    chunk_pause_ms: int,
) -> float:
    combined = bytearray()
    sample_rate = None
    chunks = list(manifest["chunks"])

    for index, chunk in enumerate(chunks):
        chunk_path = chunks_dir / f"chunk-{chunk['id']}.wav"
        if not chunk_path.is_file():
            raise RuntimeError(f"Missing chunk: {chunk_path}")
        pcm, sr = read_wav(chunk_path)
        if sample_rate is None:
            sample_rate = sr
        elif sample_rate != sr:
            raise RuntimeError(f"Sample-rate mismatch in {chunk_path}: {sr}")
        combined.extend(pcm)
        if index < len(chunks) - 1:
            pause_ms = int(chunk.get("pause_after_ms", chunk_pause_ms))
            combined.extend(silence(sr, pause_ms))

    assert sample_rate is not None
    write_wav(raw_output, bytes(combined), sample_rate)
    return (len(combined) // 2) / sample_rate


def run_postprocess(raw_output: Path, final_output: Path, config: dict) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg was not found on PATH.")

    audio = config["audio"]
    post = config["postprocess"]
    command = [
        ffmpeg,
        "-y",
        "-i",
        str(raw_output),
        "-af",
        str(post["ffmpeg_filter"]),
        "-c:a",
        str(audio["sample_format"]),
        "-ar",
        str(audio["sample_rate_hz"]),
        "-ac",
        str(audio["channels"]),
        str(final_output),
    ]
    print(f"[POST] {post['ffmpeg_filter']}")
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg post-processing failed with exit code {result.returncode}.")
    if not final_output.is_file():
        raise RuntimeError(f"Final narration was not created: {final_output}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", default=str(DEFAULT_EPISODE))
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--reference")
    parser.add_argument("--api-base", default="http://127.0.0.1:3900")
    parser.add_argument("--start-at", type=int, default=1)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--no-assemble", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = Path(args.config).resolve()
    episode = Path(args.episode).resolve()

    config = load_json(config_path)
    manifest_path = episode / "narration_chunks.json"
    manifest = load_json(manifest_path)

    if config["engine"]["id"] != "pockettts":
        raise RuntimeError("voice_production.json does not select PocketTTS.")
    if manifest.get("engine") not in (None, "pockettts"):
        raise RuntimeError(
            f"Narration manifest engine is {manifest.get('engine')!r}, expected 'pockettts'."
        )

    language = str(config["engine"]["language"])
    python_exe = expand_env_path(config["engine"]["python_path"])
    sidecar = expand_env_path(config["engine"]["sidecar_path"])
    if not python_exe.is_file():
        raise FileNotFoundError(f"VoiceStudio Python not found: {python_exe}")
    if not sidecar.is_file():
        raise FileNotFoundError(f"PocketTTS sidecar not found: {sidecar}")

    reference = resolve_reference(config, episode, args.reference, args.api_base)
    print(f"[REF] {reference}")

    chunks_dir = episode / "media" / "narration_chunks"
    raw_output = episode / "media" / "narration_raw.wav"
    final_output = episode / "media" / "narration.wav"
    chunks_dir.mkdir(parents=True, exist_ok=True)

    chunking = config["chunking"]
    paragraph_pause_ms = int(chunking.get("paragraph_pause_ms", chunking["pause_ms_default"]))
    chunk_pause_ms = int(chunking.get("chunk_pause_ms", max(chunking["pause_ms_range"])))

    selected = [
        chunk for chunk in manifest["chunks"] if int(chunk["id"]) >= int(args.start_at)
    ]
    if not selected:
        raise RuntimeError(f"No chunks selected from --start-at {args.start_at}.")

    started = time.perf_counter()
    generated = 0

    with PocketTTS(python_exe, sidecar) as engine:
        for chunk in selected:
            chunk_id = str(chunk["id"])
            output = chunks_dir / f"chunk-{chunk_id}.wav"

            if output.is_file() and not args.force:
                print(f"[SKIP] {chunk_id} already exists")
                continue

            print(f"[GEN] {chunk_id} ({chunk.get('section', 'unknown')})")
            pcm, sample_rate = build_chunk(
                engine,
                chunk,
                language,
                reference,
                paragraph_pause_ms,
            )
            write_wav(output, pcm, sample_rate)
            generated += 1
            print(f"[PASS] {chunk_id} -> {output}")

    elapsed = time.perf_counter() - started
    print(f"[GEN DONE] {generated} chunk(s) generated in {elapsed:.2f}s")

    if args.no_assemble:
        print("[DONE] Assembly skipped.")
        return 0

    raw_seconds = assemble_chunks(manifest, chunks_dir, raw_output, chunk_pause_ms)
    print(f"[ASSEMBLE] Raw narration: {raw_seconds:.2f}s -> {raw_output}")

    run_postprocess(raw_output, final_output, config)
    with wave.open(str(final_output), "rb") as wav:
        final_seconds = wav.getnframes() / wav.getframerate()

    print(f"[PASS] Final narration: {final_seconds:.2f}s")
    print(final_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
