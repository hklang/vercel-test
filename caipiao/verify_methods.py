#!/usr/bin/env python3
"""
七乐彩预测方法验证脚本 - 12种方法完整版
本次 = 近10期验证结果
历史 = 所有验证次数的平均值
"""
import json
from pathlib import Path
from collections import Counter

HIST_FILE = '/home/lang/.openclaw/workspace/caipiao/qlc_history_full.json'
TEMPLATE_FILE = '/home/lang/.openclaw/workspace/caipiao/预测帮助模板.md'
VERIFY_FILE = '/home/lang/.openclaw/workspace/caipiao/verify_history.json'

def load_data():
    with open(HIST_FILE) as f:
        data = json.load(f)
    return sorted(data, key=lambda x: x['period'])

def to_ints(nums):
    return [int(n) for n in nums]

# ===== 12种方法验证 =====

def eval_repeat(data, n=10):
    """重号法：上期号本期有出现"""
    hits = 0
    for i in range(len(data) - n, len(data) - 1):
        prev = set(to_ints(data[i]['basic_numbers']))
        curr = set(to_ints(data[i+1]['basic_numbers']))
        hit = len(prev & curr)
        if hit >= 1:  # 有重号就算命中
            hits += 1
    return hits * 100 // n

def eval_three_zone(data, n=10):
    """三区比：每区都有号"""
    hits = 0
    for i in range(len(data) - n, len(data) - 1):
        curr = to_ints(data[i+1]['basic_numbers'])
        q1 = sum(1 for x in curr if x <= 10)
        q2 = sum(1 for x in curr if 10 < x <= 20)
        q3 = sum(1 for x in curr if x > 20)
        if q1 >= 1 and q2 >= 1 and q3 >= 1:
            hits += 1
    return hits * 100 // n

def eval_consecutive(data, n=10):
    """连号法：本期有连号"""
    hits = 0
    for i in range(len(data) - n, len(data) - 1):
        curr = sorted(to_ints(data[i+1]['basic_numbers']))
        has_consecutive = any(curr[j+1] - curr[j] == 1 for j in range(len(curr)-1))
        if has_consecutive:
            hits += 1
    return hits * 100 // n

def eval_odd_even(data, n=10):
    """奇偶比：3:4或4:3"""
    hits = 0
    for i in range(len(data) - n, len(data) - 1):
        curr = to_ints(data[i+1]['basic_numbers'])
        odd = sum(1 for x in curr if x % 2 == 1)
        if odd in [3, 4]:
            hits += 1
    return hits * 100 // n

def eval_012(data, n=10):
    """012路：每路都有"""
    hits = 0
    for i in range(len(data) - n, len(data) - 1):
        curr = [int(x) % 3 for x in data[i+1]['basic_numbers']]
        r0, r1, r2 = curr.count(0), curr.count(1), curr.count(2)
        if r0 >= 1 and r1 >= 1 and r2 >= 1:
            hits += 1
    return hits * 100 // n

def eval_cold(data, n=10):
    """遗漏值/冷号：有冷号出现"""
    hits = 0
    for i in range(len(data) - n, len(data) - 1):
        num_count = {}
        for item in data[i-30:i]:
            for num in item['basic_numbers']:
                num_count[num] = num_count.get(num, 0) + 1
        cold = set(k for k, v in num_count.items() if v <= 3)
        curr = set(data[i+1]['basic_numbers'])
        if len(cold & curr) >= 1:
            hits += 1
    return hits * 100 // n

def eval_cycle(data, n=10):
    """周期回补：每5期出现1次的号"""
    hits = 0
    for i in range(len(data) - n, len(data) - 1):
        # 找周期号
        cycle_nums = set()
        for j in range(i-50, i, 5):
            if j >= 0:
                cycle_nums.update(data[j]['basic_numbers'])
        curr = set(data[i+1]['basic_numbers'])
        if len(cycle_nums & curr) >= 1:
            hits += 1
    return hits * 100 // n

def eval_range(data, n=10):
    """极距法：差值在15-25"""
    hits = 0
    for i in range(len(data) - n, len(data) - 1):
        curr = to_ints(data[i+1]['basic_numbers'])
        r = max(curr) - min(curr)
        if 15 <= r <= 25:
            hits += 1
    return hits * 100 // n

def eval_hot(data, n=10):
    """热号法：有热号出现"""
    hits = 0
    for i in range(len(data) - n, len(data) - 1):
        all_nums = []
        for item in data[i-10:i]:
            all_nums.extend(item['basic_numbers'])
        hot = set([n for n, c in Counter(all_nums).most_common(10)])
        curr = set(data[i+1]['basic_numbers'])
        if len(hot & curr) >= 1:
            hits += 1
    return hits * 100 // n

def eval_same_tail(data, n=10):
    """同尾法：有同尾号"""
    hits = 0
    for i in range(len(data) - n, len(data) - 1):
        curr = [int(x) % 10 for x in data[i+1]['basic_numbers']]
        tail_count = Counter(curr)
        if any(c >= 2 for c in tail_count.values()):  # 有2个同尾
            hits += 1
    return hits * 100 // n

def eval_ac(data, n=10):
    """AC值法：AC值5-8"""
    hits = 0
    for i in range(len(data) - n, len(data) - 1):
        curr = sorted(to_ints(data[i+1]['basic_numbers']))
        diffs = sorted(set(curr[j+1] - curr[j] for j in range(len(curr)-1)))
        ac = len(diffs)
        if 5 <= ac <= 8:
            hits += 1
    return hits * 100 // n

def eval_size(data, n=10):
    """大小号：三区都有"""
    hits = 0
    for i in range(len(data) - n, len(data) - 1):
        curr = to_ints(data[i+1]['basic_numbers'])
        small = sum(1 for x in curr if x <= 10)
        medium = sum(1 for x in curr if 10 < x <= 20)
        large = sum(1 for x in curr if x > 20)
        if small >= 1 and medium >= 1 and large >= 1:
            hits += 1
    return hits * 100 // n

# ===== 主程序 =====

def load_history():
    if Path(VERIFY_FILE).exists():
        with open(VERIFY_FILE) as f:
            return json.load(f)
    return {}

def save_history(history):
    with open(VERIFY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def main():
    data = load_data()
    print(f"Loaded {len(data)} periods")
    
    # 12种方法验证
    results = {
        '重号法': eval_repeat(data, 10),
        '三区比': eval_three_zone(data, 10),
        '连号法': eval_consecutive(data, 10),
        '奇偶比': eval_odd_even(data, 10),
        '012路': eval_012(data, 10),
        '遗漏值': eval_cold(data, 10),
        '周期回补': eval_cycle(data, 10),
        '极距法': eval_range(data, 10),
        '热号法': eval_hot(data, 10),
        '同尾法': eval_same_tail(data, 10),
        'AC值法': eval_ac(data, 10),
        '大小号': eval_size(data, 10),
    }
    
    print("\n📊 方法准确率验证 (近10期)")
    print("-" * 45)
    print(f"{'方法':<10} {'本次':>6} {'历史':>6}")
    print("-" * 45)
    
    history = load_history()
    final_results = {}
    
    for method, rate in results.items():
        rate_str = f"{rate}%"
        
        # 本次
        this_time = rate_str
        
        # 历史平均
        if method in history:
            history[method].append(rate)
            avg = sum(history[method]) / len(history[method])
            hist_avg = f"{int(avg)}%"
        else:
            history[method] = [rate]
            hist_avg = rate_str
        
        final_results[method] = {'本次': this_time, '历史': hist_avg}
        print(f"{method:<10} {this_time:>6} {hist_avg:>6}")
    
    save_history(history)
    
    # 更新模板 - 按行处理，替换每种方法的第一个命中率
    with open(TEMPLATE_FILE, 'r') as f:
        lines = f.readlines()
    
    method_names = ['重号法', '三区比', '连号法', '奇偶比', '012路', '遗漏值', 
                    '周期回补', '极距法', '热号法', '同尾法', 'AC值法', '大小号']
    
    current_method = -1
    new_lines = []
    
    for line in lines:
        # 检查是否是某个方法的第一行（以数字+方法名开头）
        for i, method in enumerate(method_names):
            if f'{i+1} ' in line and method in line:
                current_method = i
                break
        
        # 如果当前行有命中率且是当前方法的第一条
        if '命中率:' in line and current_method >= 0:
            method = method_names[current_method]
            rate = results.get(method, 0)
            hist = history.get(method, [0])
            avg = sum(hist) // len(hist) if hist else 0
            
            # 替换整行，移除后面的其他命中率历史记录
            import re
            # 找到 "命中率: XX%  历史:YY%" 这一段，整段替换
            match = re.search(r'(命中率:\s*\d+%\s+历史:\d+%).*', line)
            if match:
                line = line[:match.start()] + f'命中率: {rate}%  历史:{avg}%' + '\n'
                current_method = -1  # 重置，确保只替换第一个
        
        new_lines.append(line)
    
    with open(TEMPLATE_FILE, 'w') as f:
        f.writelines(new_lines)
    
    print("-" * 45)
    print("✅ 验证完成，历史记录已保存")

if __name__ == '__main__':
    main()
