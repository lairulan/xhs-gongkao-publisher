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

# 图片引擎配置：强制使用 HTML 卡片（无AI标识，无乱码）
IMAGE_ENGINE="html"

claude --dangerously-skip-permissions -p "公考种草 账号2

账号：小云学姐（江苏公务员学姐persona）
MCP工具：mcp__xiaohongshu-mcp-2__（端口18061）
Persona文件：\$SKILL_DIR/references/personas/account-2-xuejie.md
文案规则文件：\$SKILL_DIR/references/xhs-copywriting-rules.md（必读）
图片引擎：\$IMAGE_ENGINE（强制 HTML 卡片，无AI标识）
今日选题方向：\$TOPIC

工作流程：
1. 读取 persona 文件和 xhs-copywriting-rules.md
2. 生成小红书笔记（标题≤20字，正文符合去AI味规则）
3. 生成后自检：检查是否符合7条去AI味规则（至少满足4条）
   - 私人化场景≥2处、不完美表达≥1处、情绪波动≥1处
   - 句式长短交替、口语化词汇≥3处、非模板化结尾
4. 如自检不通过，重新改写直到通过
5. 检查登录状态，发布

发布前先检查登录状态，失败则记录错误后退出。" >> "$LOG_FILE" 2>&1

echo "[$(date)] 账号2 完成" >> "$LOG_FILE"
