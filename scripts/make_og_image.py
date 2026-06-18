"""生成微信链接卡片缩略图（PNG 1200×630 + JPG 300×300）。

仅本地手动运行；GitHub Actions 使用 docs/assets/ 中已提交的静态图片，避免 CI 无中文字体导致乱码。
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "docs" / "assets"
FONT_DIR = ROOT / "assets" / "fonts"
PNG_OUT = ASSETS / "og-cover.png"
JPG_OUT = ASSETS / "og-cover.jpg"

BG = (20, 20, 19)
TEXT = (250, 249, 245)
MUTED = (176, 174, 165)
ACCENT = (217, 119, 87)
ICON_BG = (40, 40, 38)

FONT_CANDIDATES = {
    False: [
        FONT_DIR / "NotoSansSC-Regular.otf",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
        "/System/Library/Fonts/PingFang.ttc",
    ],
    True: [
        FONT_DIR / "NotoSansSC-Bold.otf",
        "C:/Windows/Fonts/msyhbd.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
        "/System/Library/Fonts/PingFang.ttc",
    ],
}


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES[bold]:
        p = Path(path) if not isinstance(path, Path) else path
        if not p.exists() and not isinstance(path, str):
            continue
        try:
            return ImageFont.truetype(str(p), size)
        except OSError:
            continue
    raise RuntimeError(
        "未找到中文字体。本地请安装微软雅黑；CI 请安装 fonts-noto-cjk。"
    )


def _draw_icon(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=max(8, (x1 - x0) // 8), fill=ICON_BG)
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    r = (x1 - x0) // 6
    draw.ellipse(
        [cx - r * 2, cy - r, cx + r * 2, cy + r * 3],
        outline=ACCENT,
        width=max(2, r // 2),
    )
    draw.line([cx - r * 2, cy + r, cx + r * 2, cy + r], fill=ACCENT, width=max(2, r // 2))


def render_banner() -> Image.Image:
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w, 10], fill=ACCENT)

    title_font = _font(56, bold=True)
    sub_font = _font(28)

    draw.text((48, 72), "全球物流每日动态", font=title_font, fill=TEXT)
    draw.text(
        (48, 160),
        "筛选全球货代与 EPC 工程物流资讯，每日邮件直达摘要。",
        font=sub_font,
        fill=MUTED,
    )

    icon_size = 220
    _draw_icon(draw, (w - 48 - icon_size, (h - icon_size) // 2, w - 48, (h + icon_size) // 2))
    return img


def render_square() -> Image.Image:
    """微信卡片右侧小图：300×300，精简文案避免溢出。"""
    w, h = 300, 300
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w, 6], fill=ACCENT)

    title_font = _font(26, bold=True)
    sub_font = _font(14)

    draw.text((16, 24), "全球物流", font=title_font, fill=TEXT)
    draw.text((16, 58), "每日动态", font=title_font, fill=TEXT)
    draw.text((16, 96), "Global Logistics", font=sub_font, fill=ACCENT)

    icon_size = 88
    _draw_icon(draw, (w - 16 - icon_size, h - 16 - icon_size, w - 16, h - 16))
    return img


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)

    banner = render_banner()
    banner.save(PNG_OUT, format="PNG", optimize=True)

    square = render_square()
    square.save(JPG_OUT, format="JPEG", quality=90, optimize=True)

    # 简单校验：若标题 bbox 过窄，说明字体可能异常
    probe = ImageDraw.Draw(square)
    bbox = probe.textbbox((0, 0), "全球物流", font=_font(26, bold=True))
    if bbox[2] - bbox[0] < 40:
        print("警告：中文字体渲染宽度异常", file=sys.stderr)
        sys.exit(1)

    print(PNG_OUT)
    print(JPG_OUT)


if __name__ == "__main__":
    main()
