"""生成微信链接卡片缩略图（PNG 1200×630 + JPG 300×300）。"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "docs" / "assets"
PNG_OUT = ASSETS / "og-cover.png"
JPG_OUT = ASSETS / "og-cover.jpg"

BG = (20, 20, 19)
TEXT = (250, 249, 245)
MUTED = (176, 174, 165)
ACCENT = (217, 119, 87)
ICON_BG = (40, 40, 38)


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _draw_icon(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=24, fill=ICON_BG)
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    r = (x1 - x0) // 6
    draw.ellipse([cx - r * 2, cy - r, cx + r * 2, cy + r * 3], outline=ACCENT, width=max(3, r // 2))
    draw.line([cx - r * 2, cy + r, cx + r * 2, cy + r], fill=ACCENT, width=max(3, r // 2))


def render_banner(w: int, h: int) -> Image.Image:
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w, 10], fill=ACCENT)

    title = "全球物流每日动态"
    subtitle = "海运 · 空运 · 陆运 · 供应链 — 全球物流观测摘要"

    title_font = _font(max(28, w // 22), bold=True)
    sub_font = _font(max(16, w // 38))

    draw.text((48, 56), title, font=title_font, fill=TEXT)
    draw.text((48, 56 + int(h * 0.18)), subtitle, font=sub_font, fill=MUTED)

    icon_size = int(min(h * 0.55, w * 0.22))
    x1 = w - 48
    y0 = (h - icon_size) // 2
    _draw_icon(draw, (x1 - icon_size, y0, x1, y0 + icon_size))
    return img


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)

    banner = render_banner(1200, 630)
    banner.save(PNG_OUT, format="PNG", optimize=True)

    square = render_banner(300, 300)
    square.save(JPG_OUT, format="JPEG", quality=88, optimize=True)

    print(PNG_OUT)
    print(JPG_OUT)


if __name__ == "__main__":
    main()
