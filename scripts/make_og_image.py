"""生成微信链接卡片缩略图（右侧小方图）。"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets" / "og-cover.png"

W, H = 1200, 630
BG = (250, 249, 245)
TEXT = (20, 20, 19)
MUTED = (120, 118, 110)
ACCENT_BG = (20, 20, 19)
ACCENT = (106, 155, 204)


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


def draw_icon(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    r = min(x1 - x0, y1 - y0) // 5

    # 简化地球 + 航线图标，适配微信右侧小方图
    draw.ellipse([cx - r * 2, cy - r * 2, cx + r * 2, cy + r * 2], outline=ACCENT, width=max(4, r // 3))
    draw.arc([cx - r, cy - r * 2, cx + r, cy + r * 2], 200, 340, fill=ACCENT, width=max(3, r // 4))
    draw.line([cx - r * 2, cy, cx + r * 2, cy], fill=ACCENT, width=max(3, r // 4))
    draw.polygon(
        [
            (cx - r // 2, cy - r * 2 - r // 2),
            (cx + r // 2, cy - r * 2 - r // 2),
            (cx + r // 4, cy - r * 2 + r // 3),
            (cx - r // 4, cy - r * 2 + r // 3),
        ],
        fill=ACCENT,
    )


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    title_font = _font(56, bold=True)
    desc_font = _font(30)
    badge_font = _font(22, bold=True)

    title = "全球物流每日动态"
    desc = "筛选全球货代与 EPC 工程物流资讯，每日一封邮件直达中文摘要。"

    draw.rounded_rectangle([40, 40, W - 40, H - 40], radius=24, outline=(232, 230, 220), width=2, fill=(255, 255, 255))

    draw.text((72, 92), title, font=title_font, fill=TEXT)

    # 自动换行描述
    max_width = 640
    words = desc
    lines: list[str] = []
    current = ""
    for ch in words:
        trial = current + ch
        if draw.textlength(trial, font=desc_font) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = ch
    if current:
        lines.append(current)
    y = 190
    for line in lines:
        draw.text((72, y), line, font=desc_font, fill=MUTED)
        y += 44

    draw.rounded_rectangle([72, y + 20, 250, y + 64], radius=18, fill=(255, 248, 245))
    draw.text((92, y + 30), "Global Logistics", font=badge_font, fill=(217, 119, 87))

    icon_box = (W - 280, (H - 220) // 2, W - 80, (H + 220) // 2)
    draw.rounded_rectangle(icon_box, radius=28, fill=ACCENT_BG)
    draw_icon(draw, icon_box)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    print(OUT)


if __name__ == "__main__":
    main()
