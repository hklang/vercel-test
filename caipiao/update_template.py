#!/usr/bin/env python3
"""更新预测帮助模板"""
import json
from pathlib import Path

hist_file = '/home/lang/.openclaw/workspace/caipiao/qlc_history_full.json'
template_file = '/home/lang/.openclaw/workspace/caipiao/预测帮助模板.md'

with open(hist_file) as f:
    all_data = json.load(f)

sorted_data = sorted(all_data, key=lambda x: x['period'], reverse=True)
latest = sorted_data[0]

# 计算统计数据
from collections import Counter
recent_nums = []
for item in sorted_data[:30]:
    recent_nums.extend(item['basic_numbers'])
hot = Counter(recent_nums).most_common(10)

num_count = {}
for item in sorted_data[:30]:
    for num in item['basic_numbers']:
        num_count[num] = num_count.get(num, 0) + 1
cold = [(k, v) for k, v in num_count.items() if v <= 15][:6]

prev_nums = latest['basic_numbers']
repeat = []
for num in prev_nums:
    cnt = sum(1 for item in sorted_data[1:30] if num in item['basic_numbers'])
    repeat.append(f"{num}({cnt})")

# 生成新的头部
new_header = f"""🎯 七乐彩预测帮助

📊 上期开奖 ({latest['period']} {latest['date']})
   {' '.join(latest['basic_numbers'])}

📈 近期数据
 🔥 热号: {' '.join([f'{n}({c})' for n,c in hot[:6]])}
 ❄️ 冷号: {' '.join([f'{n}' for n,c in cold])}
 🔁 重号: {', '.join(repeat)}
"""

# 读取模板
with open(template_file) as f:
    content = f.read()

# 替换头部
lines = content.split('\n')
# 找到第一个空行或分隔线为止
start = 0
for i, line in enumerate(lines):
    if '━━' in line or i > 10:
        start = i
        break

# 更新模板
new_content = new_header + '\n'.join(lines[start:])
with open(template_file, 'w') as f:
    f.write(new_content)

print(f"✅ 模板已更新: {latest['period']}")
