# 🛡️ Brave API 免费次数限制规则

> 防止超出免费额度 | 创建：2026-02-10 | 作者：蒋国春

---

## 📊 Brave API 免费限制

| 套餐 | 价格 | 每月限制 | 我们的使用 |
|------|------|----------|------------|
| **免费** | $0 | 2,000次搜索/月 | 目标 ≤ 1,000次/月 |
| **付费** | $20/千次 | 超额付费 | 尽量避免 |

**来源**: https://api.search.brave.com/pricing

---

## 🎯 我们的使用策略

### 定时推送频率

| 任务 | 频率 | 每次搜索次数 | 每月估算 |
|------|------|--------------|----------|
| Google Trends | 每6小时 | 2次 | 240次 |
| Hacker News | 每4小时 | 1次 | 180次 |
| Reddit 热点 | 每6小时 | 1次 | 120次 |
| GitHub Trending | 每日1次 | 1次 | 30次 |
| **总计** | - | **~5次/天** | **~570次/月** |

**安全余量**: 预留 50% 余量 → 目标 ≤ 1,000次/月

---

## 🔧 自动防超限机制

### 1. 计数器文件

```bash
# 文件位置: ~/.openclaw/brave-api-usage.json
{
  "current_month": "2026-02",
  "used_count": 0,
  "limit": 1000,
  "reset_date": "2026-03-01T00:00:00+08:00"
}
```

### 2. 使用前检查脚本

```bash
#!/bin/bash
# check-brave-limit.sh - 检查 Brave API 使用次数

CONFIG_FILE="$HOME/.openclaw/brave-api-usage.json"
LIMIT=1000
WARN_LEVEL=800

# 读取使用次数
if [ -f "$CONFIG_FILE" ]; then
    used=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['used_count'])" 2>/dev/null || echo "0")
else
    used=0
fi

# 检查是否超限
if [ "$used" -ge "$LIMIT" ]; then
    echo "❌ ERROR: Brave API 已达月度限制 ($used/$LIMIT)"
    echo "📅 重置日期: $(cat $CONFIG_FILE | python3 -c 'import sys,json; print(json.load(sys.stdin)["reset_date"])')"
    exit 1
fi

# 警告
if [ "$used" -ge "$WARN_LEVEL" ]; then
    echo "⚠️ WARNING: Brave API 使用已达 $used/$LIMIT ($(echo "scale=1; $used*100/$LIMIT" | bc)%)"
    echo "📅 距重置还有 $(($(date -d $(cat $CONFIG_FILE | python3 -c 'import sys,json; print(json.load(sys.stdin)["reset_date"])') +%s) - $(date +%s))) 秒"
fi

echo "✅ 使用次数: $used/$LIMIT"
exit 0
```

### 3. 使用后更新计数器

```bash
#!/bin/bash
# update-brave-count.sh - 更新使用次数

CONFIG_FILE="$HOME/.openclaw/brave-api-usage.json"
count=${1:-1}

# 更新计数
python3 << EOF
import json
from datetime import datetime

with open('$CONFIG_FILE', 'r') as f:
    config = json.load(f)

config['used_count'] += $count

with open('$CONFIG_FILE', 'w') as f:
    json.dump(config, f, indent=2)

print(f"✅ 已更新: {config['used_count']}/{config['limit']}")
EOF
```

### 4. 每月自动重置

```bash
#!/bin/bash
# reset-brave-count.sh - 每月1号自动重置

CONFIG_FILE="$HOME/.openclaw/brave-api-usage.json"
CURRENT_MONTH=$(date +%Y-%m)

python3 << EOF
import json
from datetime import datetime

# 计算下个月第一天
next_month = datetime.now().replace(day=1)
if next_month.month == 12:
    next_month = next_month.replace(year=next_month.year+1, month=1)
else:
    next_month = next_month.replace(month=next_month.month+1)

config = {
    "current_month": "$CURRENT_MONTH",
    "used_count": 0,
    "limit": 1000,
    "reset_date": next_month.strftime("%Y-%m-%dT00:00:00+08:00")
}

with open('$CONFIG_FILE', 'w') as f:
    json.dump(config, f, indent=2)

print(f"✅ 已重置: {config['current_month']} -> {config['used_count']}/{config['limit']}")
print(f"📅 下次重置: {config['reset_date']}")
EOF
```

### 5. 添加到 crontab 每月自动执行

```bash
# 添加每月重置任务
(crontab -l 2>/dev/null; echo "0 0 1 * * /home/lang/.openclaw/workspace/zixun/cron/scripts/reset-brave-count.sh") | crontab -

# 验证
crontab -l | grep brave
```

---

## 🔄 在定时任务中使用

### 定时任务示例

```bash
#!/bin/bash
# zixun-external-search.sh - 域外搜索定时任务

set -e

# 1. 检查限制
/home/lang/.openclaw/workspace/zixun/cron/scripts/check-brave-limit.sh || exit 1

# 2. 执行搜索
python3 << 'PYEOF'
import subprocess
import json

# 使用 web_search 进行搜索
result = subprocess.run(
    ["openclaw", "web_search", "--query", "Google Trends hot topics today", "--count", "10"],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    data = json.loads(result.stdout)
    print(f"✅ 搜索成功，获取 {len(data.get('results', []))} 条结果")
PYEOF

# 3. 更新计数器
/home/lang/.openclaw/workspace/zixun/cron/scripts/update-brave-count.sh 5

echo "✅ 任务完成"
```

### 定时任务配置

```bash
# 添加到 crontab
crontab -e

# 添加以下行：
# 每6小时执行域外搜索（避开深夜）
0 */6 * * * /home/lang/.openclaw/workspace/zixun/cron/scripts/zixun-external-search.sh >> /var/log/zixun-search.log 2>&1
```

---

## 📊 使用统计监控

### 创建统计脚本

```bash
#!/bin/bash
# brave-stats.sh - 查看 Brave API 使用统计

CONFIG_FILE="$HOME/.openclaw/brave-api-usage.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ 配置文件不存在"
    exit 1
fi

python3 << EOF
import json
from datetime import datetime, timedelta

with open('$CONFIG_FILE') as f:
    config = json.load(f)

current = config['current_month']
used = config['used_count']
limit = config['limit']
remaining = limit - used
reset_date = config['reset_date']

# 计算使用百分比
percent = (used / limit) * 100

# 计算剩余天数
reset_dt = datetime.fromisoformat(reset_date.replace('+08:00', ''))
now = datetime.now()
days_left = (reset_dt - now).days

print(f"""
📊 Brave API 使用统计
━━━━━━━━━━━━━━━━━━━━━━
📅 月份: {current}
📈 已用: {used:,} / {limit:,} ({percent:.1f}%)
📉 剩余: {remaining:,} ({100-percent:.1f}%)
⏰ 重置: {reset_date} ({days_left} 天后)
━━━━━━━━━━━━━━━━━━━━━━
""")

# 进度条
bar_length = 30
filled = int(bar_length * used // limit)
empty = bar_length - filled
bar = "█" * filled + "░" * empty
print(f"进度: [{bar}]")
EOF
```

### 查看统计

```bash
brave-stats.sh
```

输出示例:
```
📊 Brave API 使用统计
━━━━━━━━━━━━━━━━━━━━━━
📅 月份: 2026-02
📈 已用: 240 / 1,000 (24.0%)
📉 剩余: 760 (76.0%)
⏰ 重置: 2026-03-01T00:00:00+08:00 (19 天后)
━━━━━━━━━━━━━━━━━━━━━━
进度: [████████████░░░░░░░░░░░░░░░]
```

---

## 🚨 超限告警

### 1. 微信/飞书告警

```bash
#!/bin/bash
# alert-brave-limit.sh - 发送超限告警

curl -X POST "https://open.feishu.cn/open-apis/bot/v2/hook/你的机器人ID" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "text",
    "content": {
      "text": "⚠️ Brave API 使用告警\n\n❌ 已用: '"$used"'/'"$limit"' ('"$percent"'%)\n📅 重置日期: '"$reset_date"'\n\n请减少搜索频率或升级套餐"
    }
  }'
```

### 2. 自动降级

当使用率达 90% 时，自动禁用定时任务：

```bash
#!/bin/bash
# check-and-disable.sh - 检查并自动禁用

LIMIT=1000
WARN=900

if [ "$used" -ge "$WARN" ]; then
    echo "⚠️ 达到警告阈值，自动禁用定时任务"
    
    # 禁用 cron 任务
    crontab -l | grep -v "zixun-external-search" | crontab -
    
    # 发送通知
    echo "Brave API 使用已达 $used/$LIMIT，已禁用定时任务" | \
        mail -s "Brave API 警告" your@email.com
fi
```

---

## 📋 规则总结

### ✅ 允许的操作
- 每6小时一次 Google Trends 搜索
- 每4小时一次 Hacker News 搜索  
- 每6小时一次 Reddit 搜索
- 每日一次 GitHub Trending 搜索
- **总计**: ≤ 5次/天，≤ 570次/月

### ❌ 禁止的操作
- 手动频繁点击搜索
- 调试时多次重复搜索
- 未配置计数器时使用
- 超过 1,000次/月 限制

### 📊 监控指标
- **使用率 ≤ 80%**: 正常（绿色）
- **使用率 80-90%**: 警告（黄色）
- **使用率 90-100%**: 危险（红色）
- **使用率 > 100%**: 禁用任务（橙色）

---

## 🔗 相关文档

- Brave API 定价: https://api.search.brave.com/pricing
- Brave API 文档: https://api.search.brave.com/docs
- OpenClaw web_search: https://docs.openclaw.ai/tools/web

---

**最后更新**: 2026-02-10  
**下次检查**: 每月1号  
**规则版本**: v1.0
