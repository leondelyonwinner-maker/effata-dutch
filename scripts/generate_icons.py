"""One-time asset generation: rasterizes app/static/icons/icon.svg into the
PNG sizes iOS actually requires for a home-screen icon (Safari/Chrome on iOS
don't reliably use SVG for apple-touch-icon the way desktop browsers do).

Usage:
    pip install pillow cairosvg
    python scripts/generate_icons.py

Not run automatically at build/deploy time on purpose -- it's a design asset
step, not application logic, and cairosvg is a heavy optional dependency we
don't want in the production image.
"""
from pathlib import Path

import cairosvg

ICONS_DIR = Path(__file__).resolve().parent.parent / "app" / "static" / "icons"
SVG_SOURCE = ICONS_DIR / "icon.svg"
SIZES = (180, 192, 512)  # 180 = apple-touch-icon default, 192/512 = manifest


def main() -> None:
    for size in SIZES:
        out_path = ICONS_DIR / f"icon-{size}.png"
        cairosvg.svg2png(url=str(SVG_SOURCE), write_to=str(out_path), output_width=size, output_height=size)
        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
