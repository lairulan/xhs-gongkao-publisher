#!/bin/bash
# 一键安装/卸载三账号定时任务
# 用法: ./setup-launchd.sh [install|uninstall|status]

SCRIPTS_DIR="$HOME/.claude/skills/xhs-gongkao-publisher/scripts"
LAUNCH_AGENTS="$HOME/Library/LaunchAgents"
JOBS=(
    "com.xhs.gongkao.account1"
    "com.xhs.gongkao.account2"
    "com.xhs.gongkao.account3"
)

chmod +x "$SCRIPTS_DIR"/run-account*.sh

case "${1:-install}" in
    install)
        echo "安装三账号定时任务..."
        for JOB in "${JOBS[@]}"; do
            cp "$SCRIPTS_DIR/$JOB.plist" "$LAUNCH_AGENTS/"
            launchctl unload "$LAUNCH_AGENTS/$JOB.plist" 2>/dev/null
            launchctl load "$LAUNCH_AGENTS/$JOB.plist"
            echo "✅ $JOB 已加载"
        done
        echo ""
        echo "发布时间表："
        echo "  账号1「小鹿备考日记」 — 周一至五 07:03"
        echo "  账号2「小云学姐」     — 周一至五 19:47"
        echo "  账号3「申论姐妹救助站」— 周一至六 11:53"
        ;;
    uninstall)
        echo "卸载定时任务..."
        for JOB in "${JOBS[@]}"; do
            launchctl unload "$LAUNCH_AGENTS/$JOB.plist" 2>/dev/null
            rm -f "$LAUNCH_AGENTS/$JOB.plist"
            echo "✅ $JOB 已卸载"
        done
        ;;
    status)
        echo "定时任务状态："
        for JOB in "${JOBS[@]}"; do
            if launchctl list | grep -q "$JOB"; then
                echo "  ✅ $JOB — 运行中"
            else
                echo "  ❌ $JOB — 未加载"
            fi
        done
        ;;
    *)
        echo "用法: $0 [install|uninstall|status]"
        ;;
esac
