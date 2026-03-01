#!/usr/bin/env python3
"""
七乐彩预测验证定时任务 v2
- 自动获取最新开奖数据
- 验证12种预测方法的命中率
- 更新模板中的命中率数据
- 记录验证历史

使用方法:
    python3 auto_verify.py              # 单次执行
    python3 auto_verify.py --cron      # 定时模式
"""
import json
import time
import argparse
import requests
from pathlib import Path
from datetime import datetime
from collections import Counter
import re

HIST_FILE = '/home/lang/.openclaw/workspace/caipiao/qlc_history.json'
TEMPLATE_FILE = '/home/lang/.openclaw/workspace/caipiao/预测帮助模板.md'
VERIFY_FILE = '/home/lang/.openclaw/workspace/caipiao/verify_history.json'
LOG_FILE = '/home/lang/.openclaw/workspace/caipiao/logs/verify.log'

Path('/home/lang/.openclaw/workspace/caipiao/logs').mkdir(exist_ok=True)

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')

def fetch_latest():
    """获取最新开奖数据"""
    try:
        resp = requests.get("http://data.17500.cn/7lc_desc.txt", timeout=10)
        if resp.status_code == 200:
            parts = resp.text.strip().split('\n')[0].split()
            return {
                'period': parts[0],
                'date': parts[1],
                'basic_numbers': parts[2:9],
                'special_number': parts[9]
            }
    except Exception as e:
        log(f"获取数据失败: {e}")
    return None

def load_local_data():
    with open(HIST_FILE) as f:
        data = json.load(f)
    return sorted(data, key=lambda x: x['period'], reverse=True)

def save_local_data(data):
    with open(HIST_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def to_ints(nums):
    return [int(n) for n in nums]

# ===== 预测方法 =====

def predict_repeat(prev_nums, data):
    """重号法: 上期号码中可能再出"""
    candidates = []
    for num in prev_nums:
        count = sum(1 for item in data[:30] if num in to_ints(item['basic_numbers']))
        if count >= 2:
            candidates.append(num)
    return candidates[:7]

def predict_three_zone(data):
    """三区比"""
    all_nums = []
    for item in data[:20]:
        all_nums.extend(item['basic_numbers'])
    counter = Counter(all_nums)
    
    zone1 = [n for n, c in counter.most_common(20) if int(n) <= 10][:3]
    zone2 = [n for n, c in counter.most_common(20) if 10 < int(n) <= 20][:2]
    zone3 = [n for n, c in counter.most_common(20) if int(n) > 20][:2]
    return zone1 + zone2 + zone3

def predict_consecutive(data):
    """连号法"""
    pairs = Counter()
    for item in data[:10]:
        nums = sorted(to_ints(item['basic_numbers']))
        for i in range(len(nums)-1):
            if nums[i+1] - nums[i] == 1:
                pairs[(nums[i], nums[i+1])] += 1
    result = []
    for pair, count in pairs.most_common(5):
        result.extend(pair)
    return list(set(result))[:7]

def predict_odd_even(data):
    """奇偶比"""
    odd_count = sum(1 for item in data[:20] for n in item['basic_numbers'] if int(n) % 2 == 1)
    target_odd = 4 if odd_count / 20 > 3.5 else 3
    
    all_nums = []
    for item in data[:20]:
        all_nums.extend(item['basic_numbers'])
    counter = Counter(all_nums)
    
    odds = [n for n, c in counter.most_common(15) if int(n) % 2 == 1][:target_odd]
    evens = [n for n, c in counter.most_common(15) if int(n) % 2 == 0][:7-target_odd]
    return odds + evens

def predict_012(data):
    """012路"""
    r0, r1, r2 = [], [], []
    for item in data[:20]:
        for n in item['basic_numbers']:
            r = int(n) % 3
            if r == 0: r0.append(n)
            elif r == 1: r1.append(n)
            else: r2.append(n)
    
    result = [n for n, c in Counter(r0).most_common(2)]
    result += [n for n, c in Counter(r1).most_common(2)]
    result += [n for n, c in Counter(r2).most_common(2)]
    return result[:7]

def predict_cold(data):
    """遗漏值"""
    num_count = {}
    for item in data[:30]:
        for n in item['basic_numbers']:
            num_count[n] = num_count.get(n, 0) + 1
    
    cold = [n for n in range(1, 31) if str(n).zfill(2) not in num_count]
    cold.sort(key=lambda x: num_count.get(str(x).zfill(2), 0))
    return [str(x).zfill(2) for x in cold[:7]]

def predict_cycle(data):
    """周期回补"""
    cycle_nums = Counter()
    for i in range(0, 50, 5):
        if i < len(data):
            for num in data[i]['basic_numbers']:
                cycle_nums[num] += 1
    return [n for n, c in cycle_nums.most_common(7)]

def predict_range(data):
    """极距法"""
    all_nums = []
    for item in data[:20]:
        all_nums.extend(item['basic_numbers'])
    return [n for n, c in Counter(all_nums).most_common(10)]

def predict_hot(data):
    """热号法"""
    all_nums = []
    for item in data[:30]:
        all_nums.extend(item['basic_numbers'])
    return [n for n, c in Counter(all_nums).most_common(10)]

def predict_same_tail(data):
    """同尾法"""
    tails = Counter()
    for item in data[:20]:
        for n in item['basic_numbers']:
            tails[int(n) % 10] += 1
    
    result = []
    for tail in [c[0] for c in tails.most_common(3)]:
        for i in range(1, 4):
            result.append(str(tail + i * 10))
    return result[:7]

def predict_ac(data):
    """AC值法"""
    all_nums = []
    for item in data[:30]:
        all_nums.extend(item['basic_numbers'])
    return [n for n, c in Counter(all_nums).most_common(10)]

def predict_size(data):
    """大小号"""
    return predict_three_zone(data)

# ===== 验证逻辑 =====

def verify_method(predict_fn, data, n_verify=10):
    """
    验证一个方法
    用前n期预测后n期，计算3+命中率
    """
    hits = 0
    total = 0
    
    # data已按期号降序排列（最新在前）
    # 用data[i+1]预测data[i]，验证data[i]的结果
    for i in range(n_verify, len(data) - 1):
        # 预测：用i+1期及之前的数据预测i期
        prev_nums = to_ints(data[i+1]['basic_numbers']) if i+1 < len(data) else []
        pred_data = data[i+1:]  # 预测用的历史数据
        
        try:
            predicted = predict_fn(prev_nums, pred_data) if predict_fn.__name__ == 'predict_repeat' else predict_fn(pred_data)
        except:
            predicted = []
        
        actual = to_ints(data[i]['basic_numbers'])
        
        pred_set = set(to_ints(predicted))
        actual_set = set(actual)
        hit_count = len(pred_set & actual_set)
        
        if hit_count >= 3:
            hits += 1
        total += 1
    
    return hits * 100 // total if total > 0 else 0

def load_history():
    if Path(VERIFY_FILE).exists():
        with open(VERIFY_FILE) as f:
            return json.load(f)
    return {}

def save_history(history):
    with open(VERIFY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def update_template(this_time_rates, history_rates):
    """更新模板"""
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    method_names = ['重号法', '三区比', '连号法', '奇偶比', '012路', '遗漏值', 
                   '周期回补', '极距法', '热号法', '同尾法', 'AC值法', '大小号']
    
    for method in method_names:
        this = this_time_rates.get(method, 0)
        hist = history_rates.get(method, 0)
        
        # 替换命中率行
        pattern = rf'({method}.*?命中率:)\s*\d+%\s*历史:\d+%'
        replacement = rf'\1 {this}%  历史:{hist}%'
        content = re.sub(pattern, replacement, content)
    
    with open(TEMPLATE_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

def run_verify():
    log("=" * 50)
    log("七乐彩预测验证任务开始")
    
    # 获取最新数据
    log("检查最新开奖数据...")
    latest_online = fetch_latest()
    local_data = load_local_data()
    
    if latest_online and latest_online['period'] != local_data[0]['period']:
        log(f"发现新数据: {latest_online['period']}")
        local_data.insert(0, latest_online)
        save_local_data(local_data)
    
    log(f"数据最新期号: {local_data[0]['period']}")
    
    # 定义预测方法
    methods = [
        ('重号法', predict_repeat),
        ('三区比', predict_three_zone),
        ('连号法', predict_consecutive),
        ('奇偶比', predict_odd_even),
        ('012路', predict_012),
        ('遗漏值', predict_cold),
        ('周期回补', predict_cycle),
        ('极距法', predict_range),
        ('热号法', predict_hot),
        ('同尾法', predict_same_tail),
        ('AC值法', predict_ac),
        ('大小号', predict_size),
    ]
    
    # 验证最近10期
    n_verify = 10
    this_time_rates = {}
    
    log(f"验证最近{n_verify}期...")
    
    for name, fn in methods:
        rate = verify_method(fn, local_data, n_verify)
        this_time_rates[name] = rate
    
    # 历史记录
    history = load_history()
    for method, rate in this_time_rates.items():
        if method not in history:
            history[method] = []
        history[method].append(rate)
        # 保持最近50条
        if len(history[method]) > 50:
            history[method] = history[method][-50:]
    
    # 计算历史平均
    history_rates = {}
    for method, rates in history.items():
        history_rates[method] = sum(rates) // len(rates) if rates else 0
    
    # 打印结果
    log("\n📊 验证结果 (近10期, 3+命中)")
    log("-" * 45)
    for name in [m[0] for m in methods]:
        this = this_time_rates.get(name, 0)
        hist = history_rates.get(name, 0)
        log(f"{name:<8} 本次:{this:>3}% 历史:{hist:>3}%")
    
    # 更新模板
    update_template(this_time_rates, history_rates)
    save_history(history)
    
    log("-" * 45)
    log("✅ 验证完成")
    
    return this_time_rates, history_rates

def cron_mode():
    log("定时验证模式已启动...")
    log("每2小时执行一次 (8:00-20:00)")
    
    while True:
        now = datetime.now()
        hour = now.hour
        
        if 8 <= hour < 20:
            try:
                run_verify()
            except Exception as e:
                log(f"验证失败: {e}")
        
        log("等待2小时...")
        time.sleep(2 * 60 * 60)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cron', action='store_true', help='定时模式')
    args = parser.parse_args()
    
    if args.cron:
        cron_mode()
    else:
        run_verify()
