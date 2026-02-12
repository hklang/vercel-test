#!/bin/bash
# 发送优化结果到飞书群

FEISHU_WEBHOOK_URL="${FEISHU_WEBHOOK_URL:-YOUR_WEBHOOK_URL_HERE}"
RESULT_FILE="/home/lang/.openclaw/workspace/caipiao/v5_platform/optimizer_logs/latest_result.txt"

if [ ! -f "$RESULT_FILE" ]; then
    exit 0
fi

# 读取结果（去掉日志级别前缀）
RESULT_TEXT=$(cat "$RESULT_FILE" | sed 's/^[0-9\-]* [0-9:,]* - INFO - //' | grep -v "^=" | grep -v "^运行自优化" | sed '/./,/^$/!d')

if [ -n "$RESULT_TEXT" ]; then
    # 发送到飞书
    curl -s -X POST "$FEISHU_WEBHOOK_URL" \
        -H "Content-Type: application/json" \
        -d "{
            \"msg_type\": \"text\",
            \"content\": {
                \"text\": \"【优化任务完成】
$result_TEXT\"
            }
        }" > /dev/null 2>&1
fi
