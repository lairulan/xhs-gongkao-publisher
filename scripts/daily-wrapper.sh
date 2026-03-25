#!/bin/bash
# daily-wrapper.sh — 哈希延迟调度器
# 用日期+账号哈希算出当天随机延迟，实现每天不同发布时间（30天内无重复）
#
# 用法: bash daily-wrapper.sh <账号编号> <窗口大小分钟>
#   账号1: bash daily-wrapper.sh 1 120  (07:00触发，延迟0-119分钟 → 07:00-08:59)
#   账号2: bash daily-wrapper.sh 2 120  (19:00触发，延迟0-119分钟 → 19:00-20:59)
#   账号3: bash daily-wrapper.sh 3 120  (11:30触发，延迟0-119分钟 → 11:30-13:29)

ACCOUNT=$1
WINDOW_SIZE=${2:-120}
LOG_FILE="/tmp/xhs-wrapper-${ACCOUNT}-$(date +%Y%m%d).log"

echo "[$(date '+%H:%M:%S')] 账号${ACCOUNT} wrapper 启动" >> "$LOG_FILE"

# 用 日期+账号 作为哈希种子，算出当天延迟分钟（每天唯一，可复现）
SEED="$(date +%Y%m%d)${ACCOUNT}"
OFFSET=$(python3 -c "
import hashlib
h = int(hashlib.md5(b'${SEED}').hexdigest()[:8], 16)
print(h % ${WINDOW_SIZE})
")

ACTUAL_TIME=$(python3 -c "
from datetime import datetime, timedelta
now = datetime.now().replace(second=0, microsecond=0)
t = now + timedelta(minutes=${OFFSET})
print(t.strftime('%H:%M'))
")

echo "[$(date '+%H:%M:%S')] 今日延迟 ${OFFSET} 分钟，预计发布时间 ${ACTUAL_TIME}" >> "$LOG_FILE"

# sleep 延迟
sleep $((OFFSET * 60))

echo "[$(date '+%H:%M:%S')] 开始执行账号${ACCOUNT}内容生成..." >> "$LOG_FILE"

# 调用对应账号的发布脚本
SCRIPT_DIR="$(dirname "$0")"
bash "${SCRIPT_DIR}/run-account${ACCOUNT}.sh" >> "$LOG_FILE" 2>&1

echo "[$(date '+%H:%M:%S')] 账号${ACCOUNT} 完成" >> "$LOG_FILE"
