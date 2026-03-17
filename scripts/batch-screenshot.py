#!/usr/bin/env python3
"""
小红书信息图批量生成工具
=========================
将HTML卡片内容批量转为3:4比例PNG图片。
单个浏览器实例 + setContent 直接注入，比逐张打开文件快3倍。

用法:
  python3 batch-screenshot.py --input-dir /tmp/cards --output-dir /tmp/output
  python3 batch-screenshot.py --html-glob "/tmp/cards/card-*.html" --output-dir /tmp/output
  python3 batch-screenshot.py --html-list card1.html card2.html --output-dir /tmp/output
"""

import argparse
import glob
import os
import sys
import time

def find_chromium():
    """查找系统中可用的 Chromium 路径"""
    paths = [
        "/ms-playwright/chromium-1208/chrome-linux64/chrome",
        "/ms-playwright/chromium-1148/chrome-linux64/chrome",
    ]
    # 动态查找
    pw_dirs = glob.glob("/ms-playwright/chromium-*/chrome-linux64/chrome")
    paths = pw_dirs + paths

    for p in paths:
        if os.path.isfile(p):
            return p
    return None

def batch_screenshot(html_files, output_dir, width=900, height=1200, scale=2):
    """批量截图HTML文件"""
    from playwright.sync_api import sync_playwright

    os.makedirs(output_dir, exist_ok=True)

    chromium_path = find_chromium()
    print(f"[info] Chromium: {chromium_path or 'default'}")
    print(f"[info] 输入: {len(html_files)} 个HTML文件")
    print(f"[info] 输出: {output_dir}")
    print(f"[info] 尺寸: {width}x{height} (scale={scale}x)")
    print()

    start_time = time.time()

    with sync_playwright() as p:
        launch_args = {
            "headless": True,
            "args": [
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
            ]
        }
        if chromium_path:
            launch_args["executable_path"] = chromium_path

        browser = p.chromium.launch(**launch_args)
        context = browser.new_context(
            viewport={"width": width, "height": height},
            device_scale_factor=scale,
        )
        page = context.new_page()

        results = []
        for i, html_file in enumerate(html_files, 1):
            card_start = time.time()

            # 读取HTML内容
            with open(html_file, "r", encoding="utf-8") as f:
                html_content = f.read()

            # 直接注入HTML（比navigate file://快得多）
            page.set_content(html_content, wait_until="networkidle")

            # 截图body元素
            output_name = f"xhs-{i:02d}.png"
            output_path = os.path.join(output_dir, output_name)

            page.locator("body").screenshot(path=output_path)

            elapsed = time.time() - card_start
            file_size = os.path.getsize(output_path) / 1024
            print(f"  [{i}/{len(html_files)}] {output_name} ({file_size:.0f}KB, {elapsed:.2f}s)")
            results.append(output_path)

        browser.close()

    total_time = time.time() - start_time
    print(f"\n[done] {len(results)} 张图片生成完毕，总耗时 {total_time:.2f}s")
    print(f"[done] 平均每张 {total_time/len(results):.2f}s")
    return results


def main():
    parser = argparse.ArgumentParser(description="小红书信息图批量生成工具")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input-dir", help="包含HTML文件的目录")
    group.add_argument("--html-glob", help="HTML文件的glob模式")
    group.add_argument("--html-list", nargs="+", help="HTML文件路径列表")

    parser.add_argument("--output-dir", required=True, help="图片输出目录")
    parser.add_argument("--width", type=int, default=900, help="卡片宽度 (默认900)")
    parser.add_argument("--height", type=int, default=1200, help="卡片高度 (默认1200)")
    parser.add_argument("--scale", type=int, default=2, help="缩放倍数 (默认2x)")

    args = parser.parse_args()

    # 收集HTML文件
    if args.input_dir:
        html_files = sorted(glob.glob(os.path.join(args.input_dir, "card-*.html")))
        if not html_files:
            html_files = sorted(glob.glob(os.path.join(args.input_dir, "*.html")))
    elif args.html_glob:
        html_files = sorted(glob.glob(args.html_glob))
    else:
        html_files = args.html_list

    if not html_files:
        print("[error] 未找到HTML文件", file=sys.stderr)
        sys.exit(1)

    batch_screenshot(html_files, args.output_dir, args.width, args.height, args.scale)


if __name__ == "__main__":
    main()
