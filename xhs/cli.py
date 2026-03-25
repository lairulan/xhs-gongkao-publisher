#!/usr/bin/env python3
# xhs/cli.py
# 小红书公考种草 - 统一 CLI 入口
# v3.0.0 新增：整合所有脚本为统一命令行工具
#
# 用法：
#   python -m xhs.cli --help
#   python -m xhs.cli check --env
#   python -m xhs.cli schedule --list
#   python -m xhs.cli publish --account 1 --dry-run

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ============================================================
# 配置
# ============================================================

SKILL_DIR = Path(__file__).parent.parent
OUTPUT_DIR = SKILL_DIR / "output"
METRICS_FILE = OUTPUT_DIR / "metrics.jsonl"
SELECTOR_VERSION = "2026-03-25"


# ============================================================
# 子命令：check 环境检查
# ============================================================

def cmd_check(args):
    """检查运行环境"""
    print(f"[xhs v3.0.0] 环境检查")
    print(f"选择器版本: {SELECTOR_VERSION}")
    print()

    # 检查 Python
    py_version = sys.version_info
    print(f"[{'OK' if py_version >= (3, 9) else 'FAIL'}] Python {py_version.major}.{py_version.minor}")

    # 检查 output 目录
    output_ok = OUTPUT_DIR.exists()
    print(f"[{'OK' if output_ok else 'WARN'}] output/ 目录: {OUTPUT_DIR}")

    # 检查 metrics 文件
    metrics_exists = METRICS_FILE.exists()
    if metrics_exists:
        with open(METRICS_FILE, "r") as f:
            lines = f.readlines()
        print(f"[OK] 数据回流: {len(lines)} 条记录")
    else:
        print(f"[INFO] 数据回流: 暂无记录")

    # 检查 MCP 进程
    mcp_running = _check_mcp_process()
    print(f"[{'OK' if mcp_running else 'INFO'}] MCP 进程: {'运行中' if mcp_running else '未运行'}")

    # 检查 scripts
    scripts_ok = (SKILL_DIR / "scripts" / "check.sh").exists()
    print(f"[{'OK' if scripts_ok else 'FAIL'}] scripts/ 完整")

    print()
    print("详细检查请运行: ./scripts/check.sh")


def _check_mcp_process() -> bool:
    """检查 MCP 进程是否运行"""
    import subprocess
    try:
        result = subprocess.run(
            ["pgrep", "-f", "xiaohongshu-mcp"],
            capture_output=True, text=True
        )
        return result.returncode == 0
    except Exception:
        return False


# ============================================================
# 子命令：schedule 定时管理
# ============================================================

def cmd_schedule(args):
    """定时发布管理"""
    if args.list:
        _schedule_list()
    elif args.set:
        _schedule_set(args.set)
    elif args.remove is not None:
        _schedule_remove(args.remove)
    else:
        _schedule_list()


def _schedule_list():
    """列出当前定时任务"""
    print("[定时任务列表]")
    plist_dir = SKILL_DIR / "scripts"
    plists = list(plist_dir.glob("com.xhs.gongkao.account*.plist"))

    if not plists:
        print("  暂无定时任务")
        return

    for plist in sorted(plists):
        account = plist.stem.split("account")[-1]
        print(f"  账号 {account}: {plist}")
        # 读取 launchd 状态
        import subprocess
        result = subprocess.run(
            ["launchctl", "list", f"com.xhs.gongkao.account{account}"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"    状态: 已加载")
        else:
            print(f"    状态: 未加载")
    print()
    print(f"管理定时任务: ./scripts/setup-launchd.sh [install|remove]")


def _schedule_set(account: str):
    """设置定时任务"""
    print(f"[设置定时任务] 账号 {account}")
    import subprocess
    result = subprocess.run(
        ["./scripts/setup-launchd.sh", "install", "--account", account],
        cwd=SKILL_DIR,
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        sys.exit(1)


def _schedule_remove(account: str):
    """移除定时任务"""
    print(f"[移除定时任务] 账号 {account}")
    import subprocess
    result = subprocess.run(
        ["./scripts/setup-launchd.sh", "remove", "--account", account],
        cwd=SKILL_DIR,
        capture_output=True, text=True
    )
    print(result.stdout)


# ============================================================
# 子命令：metrics 数据分析
# ============================================================

def cmd_metrics(args):
    """数据分析"""
    if not METRICS_FILE.exists():
        print("暂无数据，请先发布笔记")
        return

    with open(METRICS_FILE, "r") as f:
        records = [json.loads(line) for line in f if line.strip()]

    if not records:
        print("暂无数据")
        return

    if args.summary:
        _metrics_summary(records)
    elif args.top:
        _metrics_top(records, args.top)
    elif args.trend:
        _metrics_trend(records)
    else:
        _metrics_summary(records)


def _metrics_summary(records: list):
    """汇总统计"""
    if not records:
        return

    total = len(records)
    total_likes = sum(r.get("likes", 0) for r in records)
    total_collects = sum(r.get("collects", 0) for r in records)
    avg_likes = total_likes / total if total > 0 else 0
    avg_collects = total_collects / total if total > 0 else 0

    print(f"[数据汇总] 共 {total} 篇笔记")
    print(f"  平均点赞: {avg_likes:.1f}")
    print(f"  平均收藏: {avg_collects:.1f}")
    print(f"  最高点赞: {max(r.get('likes', 0) for r in records)}")
    print(f"  最高收藏: {max(r.get('collects', 0) for r in records)}")


def _metrics_top(records: list, n: int = 5):
    """Top N 爆款"""
    sorted_records = sorted(records, key=lambda r: r.get("likes", 0), reverse=True)
    print(f"[Top {n} 爆款]")
    for i, r in enumerate(sorted_records[:n], 1):
        title = r.get("title", "未知")[:30]
        likes = r.get("likes", 0)
        collects = r.get("collects", 0)
        print(f"  {i}. {title}")
        print(f"     点赞: {likes} | 收藏: {collects}")


def _metrics_trend(records: list):
    """趋势分析"""
    # 按天分组
    by_day = {}
    for r in records:
        day = r.get("publish_time", "")[:10]
        if day:
            by_day.setdefault(day, []).append(r)

    print("[趋势] 近7天发布")
    sorted_days = sorted(by_day.keys(), reverse=True)[:7]
    for day in sorted_days:
        day_records = by_day[day]
        day_likes = sum(r.get("likes", 0) for r in day_records)
        day_collects = sum(r.get("collects", 0) for r in day_records)
        count = len(day_records)
        print(f"  {day}: {count}篇 | 点赞{day_likes} | 收藏{day_collects}")


# ============================================================
# 子命令：selectors 选择器管理
# ============================================================

def cmd_selectors(args):
    """选择器管理"""
    if args.version:
        print(f"选择器版本: {SELECTOR_VERSION}")
    elif args.test:
        _selectors_test()
    elif args.export:
        _selectors_export(args.export)
    else:
        # 默认显示版本
        print(f"选择器版本: {SELECTOR_VERSION}")
        print(f"路径: {SKILL_DIR}/xhs/selectors.py")
        print("用法:")
        print("  --version  显示版本")
        print("  --test      测试选择器")
        print("  --export    导出选择器到文件")


def _selectors_test():
    """测试选择器"""
    from xhs.selectors import XHSSelectors, FALLBACK_SELECTORS
    sel = XHSSelectors()

    print("[选择器测试]")
    print(f"  发布页 URL: {sel.publish_page['url']}")
    print(f"  标题选择器: {sel.title['input']}")
    print(f"  发布按钮: {sel.publish['btn']}")
    print(f"  降级选择器数: {len(FALLBACK_SELECTORS)}")


def _selectors_export(path: str):
    """导出选择器到 JSON"""
    from xhs.selectors import XHSSelectors
    import json

    sel = XHSSelectors()
    data = {
        "version": SELECTOR_VERSION,
        "date": datetime.now().isoformat(),
        "publish_page": sel.publish_page,
        "image_upload": sel.image_upload,
        "title": sel.title,
        "content": sel.content,
        "tags": sel.tags,
        "visibility": sel.visibility,
        "publish": sel.publish,
        "search": sel.search,
        "note_detail": sel.note_detail,
        "login": sel.login,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"已导出到: {path}")


# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="小红书公考种草 CLI (v3.0.0)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # check
    p_check = subparsers.add_parser("check", help="检查运行环境")
    p_check.add_argument("--env", action="store_true", help="详细环境信息")
    p_check.set_defaults(func=cmd_check)

    # schedule
    p_schedule = subparsers.add_parser("schedule", help="定时任务管理")
    p_schedule.add_argument("--list", action="store_true", help="列出定时任务")
    p_schedule.add_argument("--set", metavar="ACCOUNT", help="设置定时任务")
    p_schedule.add_argument("--remove", metavar="ACCOUNT", help="移除定时任务")
    p_schedule.set_defaults(func=cmd_schedule)

    # metrics
    p_metrics = subparsers.add_parser("metrics", help="数据分析")
    p_metrics.add_argument("--summary", action="store_true", help="汇总统计")
    p_metrics.add_argument("--top", type=int, metavar="N", help="Top N 爆款")
    p_metrics.add_argument("--trend", action="store_true", help="趋势分析")
    p_metrics.set_defaults(func=cmd_metrics)

    # selectors
    p_sel = subparsers.add_parser("selectors", help="选择器管理")
    p_sel.add_argument("--version", action="store_true", help="显示版本")
    p_sel.add_argument("--test", action="store_true", help="测试选择器")
    p_sel.add_argument("--export", metavar="FILE", help="导出选择器")
    p_sel.set_defaults(func=cmd_selectors)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
