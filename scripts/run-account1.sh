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

# 图片引擎配置：强制使用 HTML 卡片（无AI标识，无乱码）
IMAGE_ENGINE="html"

claude --dangerously-skip-permissions -p "公考种草 账号1

账号：小鹿备考日记（备考学生persona）
MCP工具：mcp__xiaohongshu-mcp__（端口18060）
Persona文件：\$SKILL_DIR/references/personas/account-1-student.md
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

echo "[$(date)] 账号1 完成" >> "$LOG_FILE"
