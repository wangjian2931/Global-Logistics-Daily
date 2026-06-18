"""生成 GitHub Pages 落地页与每日预览页（含微信 og 标签、Buttondown 订阅表单）。"""

from __future__ import annotations

import html
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
SITE_CONFIG = ROOT / "config" / "site.yaml"
DOCS_DIR = ROOT / "docs"
PREVIEWS_DIR = DOCS_DIR / "previews"


def load_site_config() -> dict:
    with SITE_CONFIG.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def markdown_to_html(body_md: str) -> str:
    return markdown.markdown(body_md, extensions=["extra", "nl2br", "sane_lists"])


def list_preview_dates(limit: int = 14) -> list[str]:
    if not PREVIEWS_DIR.exists():
        return []
    return sorted((p.stem for p in PREVIEWS_DIR.glob("*.html")), reverse=True)[:limit]


def render_page(
    *,
    site: dict,
    page_title: str,
    main_html: str,
    og_description: str | None = None,
    asset_prefix: str = "",
) -> str:
    base_url = site["base_url"].rstrip("/")
    og_image = f"{base_url}{site['og_image']}"
    description = og_description or site["description"]
    username = site["buttondown_username"]

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(page_title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{html.escape(site['title'])}">
  <meta property="og:title" content="{html.escape(site['title'])}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:image" content="{html.escape(og_image)}">
  <meta property="og:url" content="{html.escape(base_url)}/">
  <link rel="stylesheet" href="{asset_prefix}assets/style.css">
</head>
<body>
  <div class="wrap">
    {main_html}
    <footer>
      <p>由 <a href="https://github.com/wangjian2931/global-logistics-daily">Global Logistics Daily</a> 自动生成 · 邮件由 Buttondown 推送</p>
    </footer>
  </div>
</body>
</html>
"""


def subscribe_block(site: dict) -> str:
    username = site["buttondown_username"]
    return f"""
    <section class="card">
      <h2>邮件订阅</h2>
      <p class="meta">由 Buttondown 推送 · 订阅后每日自动收到邮件</p>
      <form
        action="https://buttondown.com/api/emails/embed-subscribe/{html.escape(username)}"
        method="post"
        class="subscribe-form"
      >
        <label for="bd-email">输入你的邮箱</label>
        <input type="email" name="email" id="bd-email" placeholder="you@example.com" required>
        <input type="hidden" name="embed" value="1">
        <input type="submit" value="订阅">
      </form>
      <div class="subscribe-note">
        提交后请去邮箱点击「确认订阅」。本页托管在 GitHub Pages，国内一般可直接打开，无需 VPN。
      </div>
    </section>
    """


def render_index(site: dict, today: str, preview_html: str) -> str:
    base_url = site["base_url"].rstrip("/")
    archives = [d for d in list_preview_dates() if d != today]
    archive_items = "".join(
        f'<li><a href="previews/{html.escape(d)}.html">{html.escape(d)}</a></li>' for d in archives
    )
    archive_block = (
        f'<ul class="archive-list">{archive_items}</ul>' if archive_items else '<p class="meta">暂无归档</p>'
    )

    main = f"""
    <header>
      <h1>{html.escape(site['title'])}</h1>
      <p class="tagline">{html.escape(site['tagline'])}</p>
      <p>{html.escape(site['description'])}</p>
    </header>

    <section class="card">
      <h2>今日邮件预览 · {html.escape(today)}</h2>
      <p class="meta">作者 {html.escape(site['author'])} · {html.escape(today)}</p>
      <div class="preview-content">{preview_html}</div>
      <p><a href="previews/{html.escape(today)}.html">在新标签页打开完整预览</a></p>
    </section>

    <section class="card">
      <h2>往期归档</h2>
      {archive_block}
    </section>

    {subscribe_block(site)}
    """

    return render_page(
        site=site,
        page_title=f"{site['title']} | {today}",
        main_html=main,
        og_description=site["tagline"],
    )


def render_preview_page(site: dict, today: str, subject: str, preview_html: str) -> str:
    main = f"""
    <a class="back-link" href="../index.html">← 返回首页</a>
    <header>
      <h1>{html.escape(subject)}</h1>
      <p class="meta">{html.escape(today)} · {html.escape(site['author'])}</p>
    </header>
    <section class="card preview-content">{preview_html}</section>
    {subscribe_block(site)}
    """
    return render_page(
        site=site,
        page_title=subject,
        main_html=main,
        og_description=f"{site['title']} · {today}",
        asset_prefix="../",
    )


def publish_site_pages(today: str, subject: str, body_md: str) -> Path:
    site = load_site_config()
    PREVIEWS_DIR.mkdir(parents=True, exist_ok=True)

    preview_html = markdown_to_html(body_md)
    (PREVIEWS_DIR / f"{today}.html").write_text(
        render_preview_page(site, today, subject, preview_html),
        encoding="utf-8",
    )

    index_file = DOCS_DIR / "index.html"
    index_file.write_text(render_index(site, today, preview_html), encoding="utf-8")
    return index_file
