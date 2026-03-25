#!/bin/bash
# 账号3「申论姐妹救助站」内容生成脚本
# 每周一至六 11:53 自动运行

SKILL_DIR="$HOME/.claude/skills/xhs-gongkao-publisher"
LOG_FILE="/tmp/xhs-account3-$(date +%Y%m%d).log"

# 确保 MCP 进程在运行
if ! pgrep -f "xiaohongshu-mcp-darwin-arm64 -port :18062" > /dev/null; then
    cd "$HOME/xiaohongshu-mcp/account-3" && nohup ../xiaohongshu-mcp-darwin-arm64 -port :18062 -headless=true > /tmp/xhs-mcp-3.log 2>&1 &
    sleep 5
fi

DOW=$(date +%u)
case $DOW in
    1) TOPIC="申论题型拆解：归纳概括题的标准解法和失分原因" ;;
    2) TOPIC="时政热点转申论素材：本周重要政策的申论写作角度" ;;
    3) TOPIC="写作框架模板：总分总结构+分论点展开的标准范式" ;;
    4) TOPIC="申论范文拆解：高分答卷的逻辑结构和用词规律" ;;
    5) TOPIC="申论备考路径：从60分到80分的完整提分路线" ;;
    6) TOPIC="踩坑总结：申论最常见的失分点和避坑指南" ;;
    *) exit 0 ;;  # 周日不发
esac

echo "[$(date)] 账号3 开始生成内容，选题：$TOPIC" >> "$LOG_FILE"

# 图片引擎配置
# IMAGE_ENGINE=html  → v3.0 HTML卡片截图（默认，无AI标识）
# IMAGE_ENGINE=ai    → v2.x Doubao Seedream AI图片（有AI标识）
IMAGE_ENGINE="${IMAGE_ENGINE:-html}"

export OPENAI_API_KEY="$ARK_API_KEY"
export OPENAI_BASE_URL="https://ark.cn-beijing.volces.com/api/v3"
export IMAGE_MODEL="doubao-seedream-3-0-t2i-250415"

claude --dangerously-skip-permissions -p "公考种草 账号3

账号：申论姐妹救助站（申论专项persona）
MCP工具：mcp__xiaohongshu-mcp-3__（端口18062）
Persona文件：$SKILL_DIR/references/personas/account-3-shenlun.md
图片引擎：$IMAGE_ENGINE（详见 references/image-engines.md）
  - html = v3.0 HTML卡片截图，无AI标识（推荐）
  - ai   = v2.x Doubao Seedream，有AI标识
今日选题方向：$TOPIC

请读取 persona 文件，按照专业简洁的申论干货语气生成一篇小红书笔记并发布。
发布前先检查登录状态，失败则记录错误后退出。" >> "$LOG_FILE" 2>&1

echo "[$(date)] 账号3 完成" >> "$LOG_FILE"
