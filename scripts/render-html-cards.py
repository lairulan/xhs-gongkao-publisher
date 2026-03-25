#!/usr/bin/env python3
"""
HTML Card Renderer v3.0
将卡片内容渲染为截图PNG，无AI元数据，不触发小红书AI标识。

用法:
  python render-html-cards.py --input cards.json --output ./output/images/ --account 1
  python render-html-cards.py --input cards.json --output ./output/images/ --account 2
  python render-html-cards.py --input cards.json --output ./output/images/ --account 3

输入 JSON 格式:
  [
    {"index": 1, "title": "封面标题", "body": "正文内容", "tags": ["标签1"]},
    {"index": 2, "title": "卡片2标题", "body": "内容..."},
    ...
  ]
"""

import sys
import json
import argparse
import asyncio
from pathlib import Path

# 三个账号的视觉风格配置
ACCOUNT_STYLES = {
    "1": {
        "name": "小鹿备考日记",
        "style": "warm-journal",
        "bg": "#FDF6EC",
        "card_bg": "#FFFDF7",
        "accent": "#E8956D",
        "accent2": "#F7C59F",
        "text": "#3D2B1F",
        "subtext": "#7A5C44",
        "tag_bg": "#FDE8D8",
        "tag_text": "#C4602A",
        "font": "'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif",
        "border": "2px solid #F0D5B8",
        "shadow": "0 4px 20px rgba(200,120,60,0.12)",
        "emoji_accent": "📚",
        "corner": "18px",
        "card_width": 750,
        "card_height": 1000,
    },
    "2": {
        "name": "小云学姐",
        "style": "fresh-green",
        "bg": "#F0F7F4",
        "card_bg": "#FAFFFE",
        "accent": "#4CAF87",
        "accent2": "#A8D8C8",
        "text": "#1A3A2E",
        "subtext": "#4A7A65",
        "tag_bg": "#D4EDE5",
        "tag_text": "#2E7D5A",
        "font": "'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif",
        "border": "2px solid #B8DDD0",
        "shadow": "0 4px 20px rgba(60,160,110,0.12)",
        "emoji_accent": "🌿",
        "corner": "16px",
        "card_width": 750,
        "card_height": 1000,
    },
    "3": {
        "name": "申论姐妹救助站",
        "style": "intellectual-blue",
        "bg": "#F0F4F8",
        "card_bg": "#FAFCFF",
        "accent": "#3B7DD8",
        "accent2": "#90B8E8",
        "text": "#1A2840",
        "subtext": "#3D5A7A",
        "tag_bg": "#D8E8F8",
        "tag_text": "#1F5AA0",
        "font": "'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif",
        "border": "2px solid #B8CDE8",
        "shadow": "0 4px 20px rgba(40,100,200,0.12)",
        "emoji_accent": "✍️",
        "corner": "14px",
        "card_width": 750,
        "card_height": 1000,
    },
}


def generate_html(card: dict, style: dict, card_index: int, total: int) -> str:
    title = card.get("title", "")
    body = card.get("body", "")
    tags = card.get("tags", [])
    is_cover = card_index == 1

    # body 转换：换行转 <br>，列表项识别（• 开头）
    body_lines = body.strip().split("\n")
    body_html = ""
    for line in body_lines:
        line = line.strip()
        if not line:
            body_html += "<br>"
        elif line.startswith("•") or line.startswith("-"):
            body_html += f'<div class="list-item">{line[1:].strip()}</div>'
        elif line.startswith("→") or line.startswith("►"):
            body_html += f'<div class="insight">{line}</div>'
        else:
            body_html += f'<p>{line}</p>'

    tags_html = "".join(
        f'<span class="tag">{t}</span>' for t in tags
    ) if tags else ""

    page_indicator = f"{card_index}/{total}" if total > 1 else ""

    cover_extra = ""
    if is_cover:
        cover_extra = f"""
        <div class="cover-badge">{style['emoji_accent']} {style['name']}</div>
        """

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: {style['card_width']}px;
    height: {style['card_height']}px;
    background: {style['bg']};
    font-family: {style['font']};
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }}
  .card {{
    width: {style['card_width'] - 40}px;
    min-height: {style['card_height'] - 40}px;
    max-height: {style['card_height'] - 40}px;
    background: {style['card_bg']};
    border-radius: {style['corner']};
    border: {style['border']};
    box-shadow: {style['shadow']};
    padding: 52px 48px 44px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    overflow: hidden;
  }}
  .header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }}
  .accent-bar {{
    width: 6px;
    height: 44px;
    background: linear-gradient(to bottom, {style['accent']}, {style['accent2']});
    border-radius: 3px;
    flex-shrink: 0;
    margin-right: 16px;
    margin-top: 4px;
  }}
  .title-wrap {{
    flex: 1;
  }}
  .title {{
    font-size: 32px;
    font-weight: 700;
    color: {style['text']};
    line-height: 1.35;
    letter-spacing: 0.5px;
  }}
  .page-num {{
    font-size: 18px;
    color: {style['subtext']};
    opacity: 0.6;
    flex-shrink: 0;
    margin-left: 16px;
    margin-top: 6px;
  }}
  .divider {{
    height: 2px;
    background: linear-gradient(to right, {style['accent']}, transparent);
    border-radius: 1px;
    opacity: 0.35;
  }}
  .body {{
    flex: 1;
    font-size: 26px;
    color: {style['text']};
    line-height: 1.7;
    overflow: hidden;
  }}
  .body p {{
    margin-bottom: 10px;
  }}
  .body br {{
    display: block;
    margin: 4px 0;
  }}
  .list-item {{
    padding: 8px 16px 8px 20px;
    border-left: 4px solid {style['accent2']};
    margin: 8px 0;
    border-radius: 0 8px 8px 0;
    background: {style['tag_bg']};
    font-size: 25px;
    color: {style['text']};
  }}
  .insight {{
    font-size: 24px;
    color: {style['accent']};
    font-weight: 600;
    margin: 10px 0;
  }}
  .tags {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: auto;
    padding-top: 8px;
  }}
  .tag {{
    background: {style['tag_bg']};
    color: {style['tag_text']};
    font-size: 21px;
    padding: 6px 16px;
    border-radius: 20px;
    font-weight: 500;
  }}
  .cover-badge {{
    font-size: 22px;
    color: {style['subtext']};
    font-weight: 500;
    margin-top: -8px;
  }}
  .footer {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 16px;
    border-top: 1px solid {style['accent2']}55;
  }}
  .footer-name {{
    font-size: 20px;
    color: {style['subtext']};
    opacity: 0.7;
  }}
  .footer-dot {{
    width: 28px;
    height: 6px;
    background: {style['accent']};
    border-radius: 3px;
    opacity: 0.5;
  }}
</style>
</head>
<body>
  <div class="card">
    <div class="header">
      <div class="accent-bar"></div>
      <div class="title-wrap">
        <div class="title">{title}</div>
        {cover_extra}
      </div>
      {f'<div class="page-num">{page_indicator}</div>' if page_indicator else ''}
    </div>
    <div class="divider"></div>
    <div class="body">{body_html}</div>
    {f'<div class="tags">{tags_html}</div>' if tags_html else ''}
    <div class="footer">
      <div class="footer-name">{style['name']}</div>
      <div class="footer-dot"></div>
    </div>
  </div>
</body>
</html>"""


async def render_card(html_content: str, output_path: str, width: int, height: int):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": width, "height": height})
        await page.set_content(html_content, wait_until="networkidle")
        await page.screenshot(path=output_path, full_page=False)
        await browser.close()


def main():
    parser = argparse.ArgumentParser(description="HTML卡片渲染器 v3.0")
    parser.add_argument("--input", required=True, help="卡片内容JSON文件路径")
    parser.add_argument("--output", required=True, help="输出图片目录")
    parser.add_argument("--account", required=True, choices=["1", "2", "3"], help="账号编号")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        raw = f.read()
    # 防御性清洗：将中文弯引号替换为直引号，避免 JSON 解析失败
    raw = raw.replace("\u201c", '"').replace("\u201d", '"').replace("\u2018", "'").replace("\u2019", "'")
    cards = json.loads(raw)

    style = ACCOUNT_STYLES[args.account]
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    total = len(cards)
    output_files = []

    for i, card in enumerate(cards, 1):
        html = generate_html(card, style, i, total)
        html_path = output_dir / f"card_{i:02d}.html"
        png_path = output_dir / f"card_{i:02d}.png"

        # 写 HTML（调试用）
        html_path.write_text(html, encoding="utf-8")

        # 截图
        asyncio.run(render_card(
            html,
            str(png_path),
            style["card_width"],
            style["card_height"]
        ))
        output_files.append(str(png_path))
        print(f"[✓] 卡片 {i}/{total}: {png_path.name}", flush=True)

    # 输出文件列表供调用者使用
    manifest = output_dir / "manifest.json"
    manifest.write_text(json.dumps(output_files, ensure_ascii=False, indent=2))
    print(f"\n[完成] {total} 张卡片已渲染到 {output_dir}/")
    print(f"[清单] {manifest}")


if __name__ == "__main__":
    main()
