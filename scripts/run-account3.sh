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

# 图片引擎配置：强制使用 HTML 卡片（无AI标识，无乱码）
IMAGE_ENGINE="html"

claude --dangerously-skip-permissions -p "公考种草 账号3

账号：申论姐妹救助站（申论专项persona）
MCP工具：mcp__xiaohongshu-mcp-3__（端口18062）
Persona文件：\$SKILL_DIR/references/personas/account-3-shenlun.md
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

echo "[$(date)] 账号3 完成" >> "$LOG_FILE"
