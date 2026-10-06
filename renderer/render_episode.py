from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1920, 1080
BG = "#0F0F0F"
CHARCOAL = "#2A2A2A"
IVORY = "#F4EFE6"
AMBER = "#FFB020"
ORANGE = "#FF7A00"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        p = Path(candidate)
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def fit_cover(img: Image.Image, size=(W, H)) -> Image.Image:
    return ImageOps.fit(img.convert("RGB"), size, method=Image.Resampling.LANCZOS)


def draw_text_card(draw: ImageDraw.ImageDraw, text: str, y: int, size: int = 88) -> None:
    if not text:
        return
    f = font(size, bold=True)
    bbox = draw.multiline_textbbox((0, 0), text, font=f, spacing=12, align="center")
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (W - tw) // 2
    draw.rounded_rectangle((x - 38, y - 24, x + tw + 38, y + th + 28), radius=24, fill=(15,15,15,205))
    draw.multiline_text((x, y), text, font=f, fill=IVORY, spacing=12, align="center")


def figure(draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 1.0, engaged: bool = False) -> None:
    r = int(46 * scale)
    draw.ellipse((x-r, y-r, x+r, y+r), fill=IVORY)
    body_w = int(74 * scale)
    body_h = int(180 * scale)
    lean = int(22 * scale) if engaged else 0
    draw.rounded_rectangle((x-body_w//2+lean, y+r-4, x+body_w//2+lean, y+r+body_h), radius=int(30*scale), fill=IVORY)
    arm_y = y + int(105*scale)
    draw.line((x+lean, arm_y, x+int(110*scale), arm_y-int(30*scale)), fill=AMBER if engaged else IVORY, width=max(4,int(12*scale)))


def system_scene(scene: dict[str, Any]) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    visual = scene.get("visual", "")
    layout = scene.get("layout", "")
    text = scene.get("on_screen_text", "")

    # Distinct but cheap layout families.
    if "conversation" in layout or "interaction" in layout or "gaze" in layout:
        figure(draw, 600, 570, 1.15, engaged=True)
        figure(draw, 1320, 570, 1.15, engaged=True)
        draw.line((720, 455, 1200, 455), fill=AMBER, width=10)
        draw.polygon([(1180,438),(1225,455),(1180,472)], fill=AMBER)
    elif "contrast" in layout:
        draw.line((W//2, 120, W//2, H-120), fill=CHARCOAL, width=6)
        figure(draw, 500, 590, 1.0, engaged=False)
        figure(draw, 1420, 590, 1.0, engaged=True)
        draw.text((360, 260), "WEAK", font=font(58, True), fill="#888888")
        draw.text((1280, 260), "STRONGER", font=font(58, True), fill=AMBER)
    elif "diagram" in layout or "pattern" in layout or "heuristic" in layout:
        cx, cy = W//2, H//2 + 30
        for i, dx in enumerate((-420,-210,0,210,420)):
            x = cx + dx
            draw.ellipse((x-44, cy-44, x+44, cy+44), fill=IVORY if i % 2 == 0 else AMBER)
            if i != 2:
                draw.line((x, cy, cx, cy), fill=ORANGE, width=8)
        draw.ellipse((cx-70, cy-70, cx+70, cy+70), outline=AMBER, width=12)
    elif "phone" in layout:
        draw.rounded_rectangle((670,180,1250,900), radius=70, outline=IVORY, width=16, fill="#151515")
        draw.rounded_rectangle((760,330,1150,450), radius=30, fill=CHARCOAL)
        draw.rounded_rectangle((870,510,1160,630), radius=30, fill=AMBER)
    else:
        figure(draw, W//2, 570, 1.25, engaged=True)

    # Small visual-label for debugging; removable in production.
    draw.text((70, 58), scene.get("id", ""), font=font(34, True), fill=AMBER)
    if visual:
        draw.text((70, 105), visual[:85], font=font(28), fill="#B6B1A8")
    draw_text_card(draw, text, 790 if "\n" not in text else 730, 72)
    return img


def render_scene(scene: dict[str, Any], episode_dir: Path, output: Path) -> None:
    mode = scene.get("visual_mode", "SYSTEM").upper()
    base = scene.get("base_image")

    if mode in {"HYBRID", "HERO"} and base:
        p = (episode_dir / base).resolve()
        if not p.exists():
            raise FileNotFoundError(f"Missing base image for {scene['id']}: {p}")
        img = fit_cover(Image.open(p))
        draw = ImageDraw.Draw(img, "RGBA")
        if mode == "HYBRID":
            draw.rectangle((0,0,W,H), fill=(0,0,0,28))
            draw_text_card(draw, scene.get("on_screen_text",""), 820, 68)
    elif mode in {"HYBRID", "HERO"}:
        raise ValueError(f"{scene['id']} is {mode} but has no base_image")
    else:
        img = system_scene(scene)

    output.parent.mkdir(parents=True, exist_ok=True)
    img.save(output, quality=95)


def build_video(stills: list[tuple[Path, float]], output: Path, fps: int = 30) -> None:
    concat = output.with_suffix(".concat.txt")
    lines = []
    for p, duration in stills:
        # ffmpeg concat demuxer requires escaped single quotes.
        safe = str(p.resolve()).replace("'", "'\\''")
        lines.append(f"file '{safe}'")
        lines.append(f"duration {duration:.3f}")
    if stills:
        safe = str(stills[-1][0].resolve()).replace("'", "'\\''")
        lines.append(f"file '{safe}'")
    concat.write_text("\n".join(lines) + "\n", encoding="utf-8")

    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
        "-vf", f"fps={fps},format=yuv420p", "-c:v", "libx264", "-crf", "18",
        "-preset", "medium", "-movflags", "+faststart", str(output)
    ]
    subprocess.run(cmd, check=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", required=True, help="Episode directory, e.g. episodes/MLI-001")
    ap.add_argument("--manifest", default="production_manifest.json")
    ap.add_argument("--output", default="output/preview.mp4")
    ap.add_argument("--limit", type=int, default=0, help="Render first N scenes only")
    args = ap.parse_args()

    episode_dir = Path(args.episode)
    manifest = json.loads((episode_dir / args.manifest).read_text(encoding="utf-8"))
    scenes = manifest["scenes"]
    if args.limit > 0:
        scenes = scenes[:args.limit]

    still_dir = episode_dir / "output" / "stills"
    stills: list[tuple[Path, float]] = []

    for scene in scenes:
        out = still_dir / f"{scene['id']}.png"
        render_scene(scene, episode_dir, out)
        stills.append((out, float(scene["duration_sec"])))
        print(f"[PASS] {scene['id']} -> {out}")

    output = episode_dir / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    build_video(stills, output, int(manifest.get("fps", 30)))
    print(f"[PASS] video -> {output}")


if __name__ == "__main__":
    main()
