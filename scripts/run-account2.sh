#!/bin/bash
# 账号2「小云学姐」内容生成脚本
# 每周一至五 19:47 自动运行

SKILL_DIR="$HOME/.claude/skills/xhs-gongkao-publisher"
LOG_FILE="/tmp/xhs-account2-$(date +%Y%m%d).log"

# 确保 MCP 进程在运行
if ! pgrep -f "xiaohongshu-mcp-darwin-arm64 -port :18061" > /dev/null; then
    cd "$HOME/xiaohongshu-mcp/account-2" && nohup ../xiaohongshu-mcp-darwin-arm64 -port :18061 -headless=true > /tmp/xhs-mcp-2.log 2>&1 &
    sleep 5
fi

DOW=$(date +%u)
case $DOW in
    1) TOPIC="江苏省考备考攻略：报名/时间线/备考节奏全解析" ;;
    2) TOPIC="资料分享：本周整理的备考资料包（行测/申论/面试）" ;;
    3) TOPIC="事业编备考指导：事业编 vs 公务员，哪个更适合你" ;;
    4) TOPIC="公务员知识科普：编制类型/待遇/晋升通道真实解析" ;;
    5) TOPIC="上岸经历分享：我备考那年做对了哪些事" ;;
    *) exit 0 ;;
esac

echo "[$(date)] 账号2 开始生成内容，选题：$TOPIC" >> "$LOG_FILE"

# 图片引擎配置
# IMAGE_ENGINE=html  → v3.0 HTML卡片截图（默认，无AI标识）
# IMAGE_ENGINE=ai    → v2.x Doubao Seedream AI图片（有AI标识）
IMAGE_ENGINE="${IMAGE_ENGINE:-html}"

export OPENAI_API_KEY="$ARK_API_KEY"
export OPENAI_BASE_URL="https://ark.cn-beijing.volces.com/api/v3"
export IMAGE_MODEL="doubao-seedream-3-0-t2i-250415"

claude --dangerously-skip-permissions -p "公考种草 账号2

账号：小云学姐（江苏公务员学姐persona）
MCP工具：mcp__xiaohongshu-mcp-2__（端口18061）
Persona文件：$SKILL_DIR/references/personas/account-2-xuejie.md
图片引擎：$IMAGE_ENGINE（详见 references/image-engines.md）
  - html = v3.0 HTML卡片截图，无AI标识（推荐）
  - ai   = v2.x Doubao Seedream，有AI标识
今日选题方向：$TOPIC

请读取 persona 文件，按照小云学姐的温柔亲切语气生成一篇小红书笔记并发布。
发布前先检查登录状态，失败则记录错误后退出。" >> "$LOG_FILE" 2>&1

echo "[$(date)] 账号2 完成" >> "$LOG_FILE"
