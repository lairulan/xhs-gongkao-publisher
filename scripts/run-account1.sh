#!/bin/bash
# 账号1「小鹿备考日记」内容生成脚本
# 每周一至五 07:03 自动运行

SKILL_DIR="$HOME/.claude/skills/xhs-gongkao-publisher"
LOG_FILE="/tmp/xhs-account1-$(date +%Y%m%d).log"

# 确保 MCP 进程在运行
if ! pgrep -f "xiaohongshu-mcp-darwin-arm64 -port :18060" > /dev/null; then
    cd "$HOME/xiaohongshu-mcp" && nohup ./xiaohongshu-mcp-darwin-arm64 -port :18060 -headless=true > /tmp/xhs-mcp-1.log 2>&1 &
    sleep 5
fi

# 按星期几决定内容类型
DOW=$(date +%u)  # 1=周一 ... 7=周日
case $DOW in
    1) TOPIC="备考打卡日记：今天的学习安排和进度记录" ;;
    2) TOPIC="学习方法分享：我发现的行测/申论高效技巧" ;;
    3) TOPIC="错题复盘：最近的错题分析和改进方案" ;;
    4) TOPIC="备考资料种草：我正在用的APP/书籍/工具推荐" ;;
    5) TOPIC="备考心态：焦虑→调整→重新出发的真实记录" ;;
    *) exit 0 ;;  # 周末不发
esac

echo "[$(date)] 账号1 开始生成内容，选题：$TOPIC" >> "$LOG_FILE"

# 图片引擎配置
# IMAGE_ENGINE=html  → v3.0 HTML卡片截图（默认，无AI标识）
# IMAGE_ENGINE=ai    → v2.x Doubao Seedream AI图片（有AI标识）
IMAGE_ENGINE="${IMAGE_ENGINE:-html}"

export OPENAI_API_KEY="$ARK_API_KEY"
export OPENAI_BASE_URL="https://ark.cn-beijing.volces.com/api/v3"
export IMAGE_MODEL="doubao-seedream-3-0-t2i-250415"

claude --dangerously-skip-permissions -p "公考种草 账号1

账号：小鹿备考日记（备考学生persona）
MCP工具：mcp__xiaohongshu-mcp__（端口18060）
Persona文件：$SKILL_DIR/references/personas/account-1-student.md
图片引擎：$IMAGE_ENGINE（详见 references/image-engines.md）
  - html = v3.0 HTML卡片截图，无AI标识（推荐）
  - ai   = v2.x Doubao Seedream，有AI标识
今日选题方向：$TOPIC

请读取 persona 文件，按照学生备考的真实语气生成一篇小红书笔记并发布。
发布前先检查登录状态，失败则记录错误后退出。" >> "$LOG_FILE" 2>&1

echo "[$(date)] 账号1 完成" >> "$LOG_FILE"
