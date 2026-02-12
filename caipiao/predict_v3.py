#!/usr/bin/env python3
"""
七乐彩预测脚本 V3 - 深度优化版
结合大数据分析结果，优化预测策略
"""

import json
import random
from collections import Counter, defaultdict
from datetime import datetime
from itertools import combinations

DATA_FILE = '/home/lang/.openclaw/workspace/caipiao/qlc_history_full.json'

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def analyze_all(history):
    """完整分析"""
    analysis = {}
    
    # 1. 奇偶分布
    parities = [sum(1 for n in draw['basic_numbers'] if int(n) % 2 == 1) for draw in history]
    analysis['parity'] = Counter(parities).most_common(3)  # TOP3
    
    # 2. 大小分布
    sizes = []
    for draw in history:
        small = sum(1 for n in draw['basic_numbers'] if int(n) <= 10)
        medium = sum(1 for n in draw['basic_numbers'] if 11 <= int(n) <= 20)
        large = sum(1 for n in draw['basic_numbers'] if int(n) >= 21)
        sizes.append((small, medium, large))
    analysis['size'] = Counter(sizes).most_common(3)  # TOP3
    
    # 3. 热号
    recent_nums = []
    for draw in history[-10:]:
        recent_nums.extend([int(n) for n in draw['basic_numbers']])
    analysis['hot'] = [n for n, _ in Counter(recent_nums).most_common(12)]
    
    # 4. 冷号
    all_nums = set(range(1, 31))
    recent_set = set(recent_nums)
    cold = sorted(all_nums - recent_set, key=lambda x: Counter(recent_nums).get(x, 0))
    analysis['cold'] = cold[:8]
    
    # 5. 遗漏值
    missing = []
    for num in range(1, 31):
        for i, draw in enumerate(reversed(history)):
            if num in [int(n) for n in draw['basic_numbers']]:
                missing.append((num, i))
                break
        else:
            missing.append((num, 10))
    analysis['missing'] = [n for n, _ in sorted(missing, key=lambda x: x[1], reverse=True)]
    
    # 6. 常见组合
    pair_counts = Counter()
    for draw in history:
        nums = [int(n) for n in draw['basic_numbers']]
        for pair in combinations(sorted(nums), 2):
            pair_counts[pair] += 1
    analysis['top_pairs'] = [pair for pair, _ in pair_counts.most_common(20)]
    
    # 7. 号码周期稳定性
    intervals = defaultdict(list)
    for num in range(1, 31):
        gaps = []
        last_pos = None
        for i, draw in enumerate(reversed(history)):
            if str(num) in draw['basic_numbers']:
                if last_pos is not None:
                    gaps.append(last_pos)
                last_pos = i
        if gaps:
            intervals[num] = gaps
    
    # 稳定的号码（周期波动小）
    stable_nums = sorted(intervals.keys(), 
                        key=lambda x: sum(intervals[x]) / len(intervals[x]))[:15]
    analysis['stable'] = stable_nums
    
    return analysis

def generate_v3_predictions(analysis, count=100):
    """V3版预测"""
    predictions = []
    attempts = 0
    max_attempts = 5000
    
    # 目标分布
    target_parity = analysis['parity'][0][0]  # 最常见的奇数数量
    target_size = list(analysis['size'][0][0])  # 最常见的大小分布
    
    while len(predictions) < count and attempts < max_attempts:
        attempts += 1
        
        # 策略1：热号为主（50%概率）
        if random.random() < 0.50:
            candidates = analysis['hot'][:15].copy()
        # 策略2：遗漏回补（30%概率）
        elif random.random() < 0.80:
            candidates = analysis['missing'][:12].copy()
        # 策略3：随机（20%概率）
        else:
            candidates = list(range(1, 31))
        
        if len(candidates) < 7:
            candidates = list(range(1, 31))
        
        # 随机选7个
        selected = random.sample(candidates, 7)
        selected = sorted(selected)
        
        # 约束1：奇偶分布（允许±1）
        actual_odd = sum(1 for n in selected if n % 2 == 1)
        if abs(actual_odd - target_parity) > 1:
            continue
        
        # 约束2：大小分布（允许±1）
        small = sum(1 for n in selected if n <= 10)
        medium = sum(1 for n in selected if 11 <= n <= 20)
        large = sum(1 for n in selected if n >= 21)
        size = (small, medium, large)
        if any(abs(size[i] - target_size[i]) > 1 for i in range(3)):
            continue
        
        # 约束3：至少2个热号
        hot_count = sum(1 for n in selected if n in analysis['hot'][:8])
        if hot_count < 2:
            continue
        
        # 约束4：避免全部冷号
        cold_count = sum(1 for n in selected if n in analysis['cold'][:5])
        if cold_count >= 4:
            continue
        
        # 约束5：号码不重复
        if len(set(selected)) != 7:
            continue
        
        # 避免重复
        if selected not in predictions:
            predictions.append(selected)
    
    return predictions, analysis

def calculate_prediction_stats(predictions, analysis):
    """计算预测统计"""
    all_preds = []
    for pred in predictions:
        all_preds.extend(pred)
    
    counter = Counter(all_preds)
    
    print("\n" + "=" * 60)
    print("预测统计")
    print("=" * 60)
    
    print(f"\n预测数量: {len(predictions)} 组")
    print(f"\n号码热度 TOP15:")
    for num, cnt in counter.most_common(15):
        bar = "█" * int(cnt / len(predictions) * 100)
        pct = cnt / len(predictions) * 100
        print(f"  {num:2d}: {cnt:3d}次 ({pct:5.1f}%) {bar}")
    
    print(f"\n热号包含率:")
    print(f"  TOP8热号: {sum(1 for n in analysis['hot'][:8] if n in [p for preds in predictions for p in preds[:7]])}")
    
    return counter

def main():
    print("=" * 60)
    print("七乐彩预测 V3 - 深度优化版")
    print("=" * 60)
    
    history = load_data()
    print(f"\n数据: {len(history)} 期")
    print(f"最新: {history[-1]['period']} - {history[-1]['date']}")
    
    # 完整分析
    print("\n正在分析数据...")
    analysis = analyze_all(history)
    
    # 生成预测
    print("正在生成预测...")
    predictions, analysis = generate_v3_predictions(analysis, 100)
    
    print(f"\n✅ 生成 {len(predictions)} 组预测")
    
    # 统计
    calculate_prediction_stats(predictions, analysis)
    
    # 保存
    output_file = '/home/lang/.openclaw/workspace/caipiao/predictions_v3.csv'
    with open(output_file, 'w', encoding='utf-8-sig') as f:
        f.write('序号,号码1,号码2,号码3,号码4,号码5,号码6,号码7\n')
        for i, pred in enumerate(predictions, 1):
            f.write(f'{i},{",".join(map(str, pred))}\n')
    
    print(f"\n📁 已保存: {output_file}")
    
    # 显示前10组
    print(f"\n前10组预测:")
    for i, pred in enumerate(predictions[:10], 1):
        print(f"  {i:3d}: {pred}")

if __name__ == '__main__':
    main()
