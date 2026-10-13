"""Photographic scenes must not contain generated compositor graphics or captions."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageChops

from renderer.render_episode import fit_cover, render_scene


def test_hero_and_hybrid_render_without_overlays(tmp_path: Path) -> None:
    source = tmp_path / "base.png"
    Image.new("RGB", (640, 360), (102, 75, 48)).save(source)
    expected = fit_cover(Image.open(source))
    for mode in ("HERO", "HYBRID"):
        destination = tmp_path / f"{mode}.png"
        render_scene(
            {
                "id": "S022",
                "visual_mode": mode,
                "base_image": "base.png",
                "layout": "conversation_progression",
                "on_screen_text": "4. MORE PERSONAL",
            },
            tmp_path,
            destination,
        )
        with Image.open(destination) as rendered:
            assert ImageChops.difference(expected, rendered.convert("RGB")).getbbox() is None
