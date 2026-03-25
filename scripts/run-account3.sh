#!/bin/bash
# 账号3「申论姐妹救助站」内容生成脚本
# 每周一至六 11:53 自动运行

set -e

SKILL_DIR="$HOME/.claude/skills/xhs-gongkao-publisher"
LOG_FILE="/tmp/xhs-account3-$(date +%Y%m%d).log"
CONTENT_FILE="/tmp/xhs-content-account3-$(date +%Y%m%d).json"
MCP_PORT=18062
MCP_TOOL="mcp__xiaohongshu-mcp-3__"
RENDERER="$SKILL_DIR/scripts/render-html-cards.py"

echo "[$(date)] ===== 账号3 开始 =====" >> "$LOG_FILE"

# -----------------------------------------------------------------------------
# Step 0: MCP Pre-flight 检查
# -----------------------------------------------------------------------------
echo "[$(date)] [检查] 验证 MCP 端口 $MCP_PORT ..." >> "$LOG_FILE"

if ! pgrep -f "xiaohongshu-mcp-darwin-arm64 -port :$MCP_PORT" > /dev/null; then
    echo "[$(date)] [启动] MCP 进程未运行，正在启动..." >> "$LOG_FILE"
    cd "$HOME/xiaohongshu-mcp/account-3" && nohup ../xiaohongshu-mcp-darwin-arm64 -port :$MCP_PORT -headless=true > /tmp/xhs-mcp-3.log 2>&1 &
    sleep 5
fi

if ! nc -z localhost $MCP_PORT 2>/dev/null; then
    echo "[$(date)] [错误] MCP 端口 $MCP_PORT 未监听，跳过发布" >> "$LOG_FILE"
    exit 1
fi

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$MCP_PORT/health 2>/dev/null || echo "000")
if [ "$HTTP_CODE" != "200" ]; then
    echo "[$(date)] [错误] MCP health 检查失败 (HTTP $HTTP_CODE)，跳过发布" >> "$LOG_FILE"
    exit 1
fi

echo "[$(date)] [OK] MCP $MCP_PORT 运行正常" >> "$LOG_FILE"

# -----------------------------------------------------------------------------
# Step 1: 选题
# -----------------------------------------------------------------------------
DOW=$(date +%u)
case $DOW in
    1) TOPIC="申论题型拆解：归纳概括题的标准解法和失分原因" ;;
    2) TOPIC="时政热点转申论素材：本周重要政策的申论写作角度" ;;
    3) TOPIC="写作框架模板：总分总结构+分论点展开的标准范式" ;;
    4) TOPIC="申论范文拆解：高分答卷的逻辑结构和用词规律" ;;
    5) TOPIC="申论备考路径：从60分到80分的完整提分路线" ;;
    6) TOPIC="踩坑总结：申论最常见的失分点和避坑指南" ;;
    *) echo "[$(date)] 周日跳过发布" >> "$LOG_FILE"; exit 0 ;;
esac

echo "[$(date)] [选题] $TOPIC" >> "$LOG_FILE"

# -----------------------------------------------------------------------------
# Step 2-4: Claude 生成内容 + HTML 卡片
# -----------------------------------------------------------------------------
IMAGE_ENGINE="html"

claude --dangerously-skip-permissions -p "公考种草 账号3

账号：申论姐妹救助站（申论专项persona）
MCP工具：${MCP_TOOL}（端口${MCP_PORT}）
Persona文件：\$SKILL_DIR/references/personas/account-3-shenlun.md
文案规则文件：\$SKILL_DIR/references/xhs-copywriting-rules.md（必读）
渲染器：\$SKILL_DIR/scripts/render-html-cards.py
今日选题：\$TOPIC

【强制工作流程，必须全部执行】

1. 读取 persona 和 xhs-copywriting-rules.md

2. 生成小红书笔记：
   - 标题 ≤20 字
   - 正文 300-500 字（信息图模式）
   - 符合去AI味规则（7条至少满足4条）
   - 自检不通过则重新改写

3. 将内容写入 /tmp/xhs-content-account3.json：
   {
     \"title\": \"标题\",
     \"body\": \"正文\",
     \"tags\": [\"#申论\", \"#公考\"],
     \"images\": []
   }

4. 生成 HTML 卡片：
   - 调用 python \$RENDERER --input /tmp/xhs-content-account3.json --output /tmp/xhs-cards-account3/ --account 3
   - 读取输出的 manifest.json 获取图片路径
   - 将图片路径填入 content JSON 的 images 字段

5. 发布：
   a) 先调用 MCP 的 check_login_status 检查登录状态
   b) 如果已登录：调用 publish_content 发布
   c) 如果返回 404/错误：降级为 Browser 通道，使用 CDP 操作发布
   d) 发布成功后保存 note_id 到 content JSON

6. 如 MCP 和 Browser 均失败：
   - 保存完整内容到 output/ 供手动发布
   - 在日志中记录失败原因

7. 所有操作记录到 $LOG_FILE" >> "$LOG_FILE" 2>&1

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "[$(date)] [完成] 账号3 任务成功" >> "$LOG_FILE"
else
    echo "[$(date)] [失败] 账号3 任务异常 (exit $EXIT_CODE)" >> "$LOG_FILE"
fi

echo "[$(date)] ===== 账号3 结束 =====" >> "$LOG_FILE"
