#!/bin/bash
# gatekeeper.sh - Agent请求验证器
# 作用：分离Agent和密钥权限，提高安全性

SPOOL_DIR=~/agent-requests
LOG_DIR=~/gatekeeper-logs
API_KEY_FILE=~/.config/moltbook/credentials.json

# 白名单操作
ALLOWLIST=("moltbook_post" "moltbook_feed" "moltbook_search" "moltbook_upvote" "echo_status")

log_request() {
    mkdir -p $LOG_DIR
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> $LOG_DIR/gatekeeper.log
}

# 检查参数
if [ -z "$1" ]; then
    echo "ERROR: No request file provided"
    exit 1
fi

REQUEST_FILE="$SPOOL_DIR/$1"

# 验证请求文件存在
if [ ! -f "$REQUEST_FILE" ]; then
    log_request "BLOCKED: Request file not found: $1"
    echo "ERROR: Request file not found"
    exit 1
fi

# 提取请求类型
REQUEST_TYPE=$(cat "$REQUEST_FILE" | jq -r '.type' 2>/dev/null)

if [ -z "$REQUEST_TYPE" ] || [ "$REQUEST_TYPE" = "null" ]; then
    log_request "BLOCKED: Invalid JSON or missing type field: $1"
    echo "ERROR: Invalid request format"
    exit 1
fi

# 白名单检查
if [[ ! " ${ALLOWLIST[@]} " =~ " ${REQUEST_TYPE} " ]]; then
    log_request "BLOCKED: Unknown request type: $REQUEST_TYPE"
    echo "BLOCKED: Operation not in allowlist"
    exit 1
fi

# 检查API密钥文件
if [ ! -f "$API_KEY_FILE" ]; then
    log_request "ERROR: API key file not found"
    echo "ERROR: API credentials missing"
    exit 1
fi

# 读取API密钥
API_KEY=$(cat "$API_KEY_FILE" | jq -r '.api_key' 2>/dev/null)

if [ -z "$API_KEY" ] || [ "$API_KEY" = "null" ]; then
    log_request "ERROR: Could not read API key"
    echo "ERROR: Invalid credentials"
    exit 1
fi

# 记录执行
log_request "EXECUTE: $REQUEST_TYPE by $(whoami)"

# 执行请求
case $REQUEST_TYPE in
    moltbook_post)
        RESPONSE=$(curl -s -X POST "https://www.moltbook.com/api/v1/posts" \
            -H "Authorization: Bearer $API_KEY" \
            -H "Content-Type: application/json" \
            -d @"$REQUEST_FILE")
        echo "$RESPONSE"
        ;;
    moltbook_feed)
        curl -s "https://www.moltbook.com/api/v1/feed?sort=new&limit=10" \
            -H "Authorization: Bearer $API_KEY"
        ;;
    moltbook_search)
        QUERY=$(cat "$REQUEST_FILE" | jq -r '.query')
        curl -s "https://www.moltbook.com/api/v1/search?q=${QUERY}&limit=10" \
            -H "Authorization: Bearer $API_KEY"
        ;;
    moltbook_upvote)
        POST_ID=$(cat "$REQUEST_FILE" | jq -r '.post_id')
        curl -s -X POST "https://www.moltbook.com/api/v1/posts/${POST_ID}/upvote" \
            -H "Authorization: Bearer $API_KEY"
        ;;
    echo_status)
        cat "$REQUEST_FILE"
        ;;
esac

log_request "SUCCESS: $REQUEST_TYPE completed"
