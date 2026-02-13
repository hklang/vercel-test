#!/bin/bash
# 发送优化结果到飞书群
# ====================

FEISHU_WEBHOOK_URL="${FEISHU_WEBHOOK_URL:-YOUR_WEBHOOK_URL_HERE}"

# 调用Python脚本生成消息并发送
python3 /home/lang/.openclaw/workspace/caipiao/v5_platform/notify_feishu.py
