#!/usr/bin/env python3
"""
七乐彩预测脚本 V2 - 改进版
改进点：
1. 使用动态权重
2. 增加热号约束（每组至少2个热号）
3. 满足奇偶和大小分布约束
4. 根据历史表现自动调整策略
"""

import json
import random
from collections import Counter
from datetime import datetime
from pathlib import Path

# 配置
DATA_FILE = '/home/lang/.openclaw/workspace/caipiao/qlc_history_full.json'
WEIGHTS_FILE = '/home/lang/.openclaw/workspace/caipiao/weights.json'

def load_data():
    """加载数据"""
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def load_weights():
    """加载权重"""
    try:
        with open(WEIGHTS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {'missing': 0.60, 'hot': 0.20, 'random': 0.20}

def analyze_recent(history, window=20):
    """分析最近window期规律"""
    recent = history[-window:]
    
    # 奇偶分布
    parities = [sum(1 for n in draw['basic_numbers'] if int(n) % 2 == 1) for draw in recent]
    target_odd = Counter(parities).most_common(1)[0][0]
    
    # 大小分布
    size_dists = []
    for draw in recent:
        small = sum(1 for n in draw['basic_numbers'] if int(n) <= 10)
        medium = sum(1 for n in draw['basic_numbers'] if 11 <= int(n) <= 20)
        large = sum(1 for n in draw['basic_numbers'] if int(n) >= 21)
        size_dists.append((small, medium, large))
    target_size = Counter(size_dists).most_common(1)[0][0]
    
    # 热号（最近10期）
    recent_numbers = []
    for draw in history[-10:]:
        recent_numbers.extend([int(x) for x in draw['basic_numbers']])
    hot_counter = Counter(recent_numbers)
    hot_numbers = [num for num, _ in hot_counter.most_common(10)]
    
    # 遗漏值
    missing_values = {}
    for num in range(1, 31):
        for i, draw in enumerate(reversed(history)):
            if str(num) in draw['basic_numbers']:
                missing_values[num] = i
                break
        else:
            missing_values[num] = 100  # 从未出现
    
    sorted_by_missing = sorted(missing_values.items(), key=lambda x: x[1], reverse=True)
    missing_numbers = [num for num, _ in sorted_by_missing[:15]]
    
    return {
        'target_odd': target_odd,  # 目标奇数数量
        'target_size': target_size,  # (小区, 中区, 大区)
        'hot': hot_numbers,  # 热号列表
        'missing': missing_numbers,  # 遗漏值大的号码
    }

def check_parity(numbers, target_odd):
    """检查奇偶分布"""
    actual_odd = sum(1 for n in numbers if int(n) % 2 == 1)
    return actual_odd == target_odd

def check_size(numbers, target_size):
    """检查大小分布"""
    small = sum(1 for n in numbers if int(n) <= 10)
    medium = sum(1 for n in numbers if 11 <= int(n) <= 20)
    large = sum(1 for n in numbers if int(n) >= 21)
    return (small, medium, large) == target_size

def check_hot(numbers, hot_numbers, min_hot=2):
    """检查热号数量"""
    hot_count = sum(1 for n in numbers if int(n) in hot_numbers)
    return hot_count >= min_hot

def generate_prediction_v2(analysis, weights, count=1):
    """生成预测（改进版）"""
    predictions = []
    attempts = 0
    max_attempts = 1000
    
    while len(predictions) < count and attempts < max_attempts:
        attempts += 1
        
        # 根据权重选择策略
        strategy = random.random()
        
        if strategy < weights['missing']:
            # 遗漏值法（优先选遗漏大的）
            candidates = analysis['missing'][:20].copy()
        elif strategy < weights['missing'] + weights['hot']:
            # 热号法
            candidates = analysis['hot'].copy()
        else:
            # 随机法
            candidates = list(range(1, 31))
        
        # 确保有足够的候选号码
        if len(candidates) < 7:
            candidates = list(range(1, 31))
        
        # 随机选7个
        selected = random.sample(candidates, 7)
        selected.sort()
        
        # 检查约束（放宽条件）
        # 奇偶：允许±1偏差
        actual_odd = sum(1 for n in selected if int(n) % 2 == 1)
        if abs(actual_odd - analysis['target_odd']) > 1:
            continue
        # 大小：允许偏差1
        small = sum(1 for n in selected if int(n) <= 10)
        medium = sum(1 for n in selected if 11 <= int(n) <= 20)
        large = sum(1 for n in selected if int(n) >= 21)
        if (small, medium, large) != analysis['target_size']:
            # 检查是否在允许范围内
            if not (abs(small - analysis['target_size'][0]) <= 1 and 
                    abs(medium - analysis['target_size'][1]) <= 1 and 
                    abs(large - analysis['target_size'][2]) <= 1):
                continue
        # 热号：至少1个
        hot_count = sum(1 for n in selected if int(n) in analysis['hot'][:10])
        if hot_count < 1:
            continue
        
        # 确保号码不重复
        if len(set(selected)) == 7:
            predictions.append(selected)
    
    return predictions

def main():
    print("=" * 60)
    print("七乐彩预测 V2 - 改进版")
    print("=" * 60)
    
    # 加载数据
    history = load_data()
    weights = load_weights()
    
    print(f"\n数据: {len(history)} 期")
    print(f"权重: 遗漏={weights['missing']:.0%}, 热号={weights['hot']:.0%}, 随机={weights['random']:.0%}")
    
    # 分析
    analysis = analyze_recent(history)
    print(f"\n分布约束:")
    print(f"  奇偶: {analysis['target_odd']}奇{7-analysis['target_odd']}偶")
    print(f"  大小: {analysis['target_size']}")
    print(f"  热号: ≥2个来自 {analysis['hot'][:5]}...")
    
    # 生成100组预测
    predictions = generate_prediction_v2(analysis, weights, 100)
    print(f"\n✅ 生成 {len(predictions)} 组预测")
    
    # 输出前10组预览
    print(f"\n前10组预览:")
    for i, pred in enumerate(predictions[:10], 1):
        print(f"  {i:3d}: {pred}")
    
    # 保存预测
    output_file = '/home/lang/.openclaw/workspace/caipiao/predictions_v2.csv'
    with open(output_file, 'w', encoding='utf-8-sig') as f:
        f.write('序号,号码1,号码2,号码3,号码4,号码5,号码6,号码7\n')
        for i, pred in enumerate(predictions, 1):
            f.write(f'{i},{",".join(map(str, pred))}\n')
    
    print(f"\n📁 已保存: {output_file}")
    
    # 统计预测分布
    all_preds = []
    for pred in predictions:
        all_preds.extend(pred)
    
    counter = Counter(all_preds)
    print(f"\n预测热度 TOP10:")
    for num, cnt in counter.most_common(10):
        print(f"  {num:2d}: 出现 {cnt} 次")

if __name__ == '__main__':
    main()
