#!/bin/bash
# 完全免费域外搜索定时任务
# 无API限制，100%免费使用

set -e

# 代理配置
export http_proxy="http://127.0.0.1:20171"
export https_proxy="http://127.0.0.1:20171"

# 日志
LOG_FILE="/var/log/zixun-external-search.log"
echo "=== $(date) ===" >> $LOG_FILE

# 切换到脚本目录
cd /home/lang/.openclaw/workspace/zixun/cron/scripts

# 1. 获取 GitHub Trending
echo "📦 获取 GitHub Trending..." >> $LOG_FILE
python3 free_sources.py >> $LOG_FILE 2>&1

# 2. 发送飞书消息
echo "📱 发送飞书消息..." >> $LOG_FILE
python3 << 'PYEOF' >> $LOG_FILE 2>&1
import json
from free_sources import get_all_sources, format_for_feishu

# 获取数据
data = get_all_sources()

# 保存到文件
with open('/tmp/free_sources_data.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 格式化为飞书消息
message = format_for_feishu(data)

# 发送到飞书
import subprocess
result = subprocess.run(
    ["openclaw", "message", "send", "--channel", "feishu", 
     "--to", "oc_982e81066ead19e659ccff0f5f509ddd", "--message", message],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("✅ 飞书消息已发送")
else:
    print(f"❌ 发送失败: {result.stderr}")
PYEOF

echo "✅ 任务完成" >> $LOG_FILE
