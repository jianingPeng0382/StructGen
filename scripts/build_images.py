#!/usr/bin/env python3
"""Render the selected paper figures into web-ready images."""

from pathlib import Path
import shutil
import subprocess

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "StructGen_arxiv_candidate" / "figs"
OUTPUT = ROOT / "static" / "images"

FIGURES = {
    "teaser_v1.pdf": ("teaser.webp", 2400),
    "intro_v2.pdf": ("structured-context.webp", 1400),
    "method.pdf": ("structgen.webp", 2400),
    "benchmark_v1.pdf": ("structgen-bench.webp", 2400),
    "structgen_bench.pdf": ("results.webp", 2400),
}


def render_pdf(source: Path, destination: Path, width: int) -> None:
    temp_prefix = OUTPUT / f".{destination.stem}-render"
    subprocess.run(
        [
            "pdftoppm",
            "-png",
            "-singlefile",
            "-r",
            "144",
            "-scale-to-x",
            str(width),
            "-scale-to-y",
            "-1",
            str(source),
            str(temp_prefix),
        ],
        check=True,
    )
    temp_png = temp_prefix.with_suffix(".png")
    with Image.open(temp_png) as image:
        rgb = image.convert("RGB")
        rgb.save(destination, "WEBP", quality=91, method=6)
    temp_png.unlink()


def make_og_banner(teaser_path: Path) -> None:
    canvas = Image.new("RGB", (1200, 630), "white")
    draw = ImageDraw.Draw(canvas)
    bold_candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    regular_candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    bold_path = next(Path(p) for p in bold_candidates if Path(p).exists())
    regular_path = next(Path(p) for p in regular_candidates if Path(p).exists())
    title_font = ImageFont.truetype(str(bold_path), 52)
    subtitle_font = ImageFont.truetype(str(regular_path), 26)

    draw.rounded_rectangle((42, 34, 1158, 596), radius=34, fill="#f8fafc")
    draw.text((82, 70), "StructGen", font=title_font, fill="#0f172a")
    draw.text(
        (82, 138),
        "Disambiguating Multi-Reference Image Generation",
        font=subtitle_font,
        fill="#334155",
    )
    draw.text(
        (82, 176),
        "via Structured Context Modeling",
        font=subtitle_font,
        fill="#334155",
    )
    draw.rounded_rectangle((930, 68, 1117, 116), radius=22, fill="#2563eb")
    draw.text((958, 79), "ACM MM 2026", font=ImageFont.truetype(str(bold_path), 18), fill="white")

    with Image.open(teaser_path) as teaser:
        teaser = teaser.convert("RGB")
        teaser.thumbnail((1035, 325), Image.Resampling.LANCZOS)
        x = (1200 - teaser.width) // 2
        canvas.paste(teaser, (x, 238))
    canvas.save(OUTPUT / "og-banner.png", optimize=True)


def main() -> None:
    if not shutil.which("pdftoppm"):
        raise SystemExit("pdftoppm is required")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for source_name, (destination_name, width) in FIGURES.items():
        render_pdf(SOURCE / source_name, OUTPUT / destination_name, width)
    make_og_banner(OUTPUT / "teaser.webp")


if __name__ == "__main__":
    main()
