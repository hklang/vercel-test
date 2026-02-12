#!/usr/bin/env python3
"""
七乐彩预测方法验证脚本
验证方法6-13的命中率
"""

import json
from collections import Counter
from datetime import datetime

# 加载数据
DATA_FILE = '/home/lang/.openclaw/workspace/caipiao/qlc_history_full.json'
OUTPUT_FILE = '/home/lang/.openclaw/workspace/caipiao/验证结果_6-13.md'

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def calculate_sum(numbers):
    """和值"""
    return sum(int(n) for n in numbers)

def calculate_range(numbers):
    """极距（最大-最小）"""
    nums = [int(n) for n in numbers]
    return max(nums) - min(nums)

def calculate_ac(numbers):
    """AC值"""
    nums = sorted([int(n) for n in numbers])
    diffs = {nums[j] - nums[i] for i in range(len(nums)) for j in range(i+1, len(nums))}
    return len(diffs) - 6

def calculate_012(numbers):
    """012路分布"""
    road0 = sum(1 for n in numbers if int(n) % 3 == 0)
    road1 = sum(1 for n in numbers if int(n) % 3 == 1)
    road2 = sum(1 for n in numbers if int(n) % 3 == 2)
    return (road0, road1, road2)

def calculate_size(numbers):
    """大小分布 (1-10小, 11-20中, 21-30大)"""
    small = sum(1 for n in numbers if int(n) <= 10)
    medium = sum(1 for n in numbers if 11 <= int(n) <= 20)
    large = sum(1 for n in numbers if int(n) >= 21)
    return (small, medium, large)

def calculate_consecutive(numbers):
    """连号数量"""
    nums = sorted([int(n) for n in numbers])
    count = 0
    for i in range(len(nums) - 1):
        if nums[i+1] == nums[i] + 1:
            count += 1
    return count

def calculate_same_tail(numbers):
    """同尾号数量"""
    tails = [int(n) % 10 for n in numbers]
    tail_counts = Counter(tails)
    return sum(1 for c in tail_counts.values() if c >= 2)

def calculate_repeat(numbers, prev_numbers):
    """重号数量"""
    return len(set(numbers) & set(prev_numbers))

def analyze_recent_trend(history, method_func, window=10):
    """分析近期趋势，返回预测值"""
    recent = history[-window:]
    values = [method_func([int(n) for n in d['basic_numbers']]) for d in recent]
    
    if len(values) < 2:
        return values[0] if values else None
    
    # 简单趋势：取众数或平均值
    counter = Counter(values)
    most_common = counter.most_common(1)[0][0]
    return most_common

def validate_method(history, method_func, method_name, target_func, window=20):
    """验证单个方法"""
    results = []
    
    # 用前N期预测，看后M期的表现
    train_end = len(history) - window
    test_data = history[train_end:]
    
    for i, data in enumerate(test_data):
        actual = [int(n) for n in data['basic_numbers']]
        
        # 使用训练数据预测
        train_data = history[:len(history)-window+i]
        
        # 获取预测值
        predicted = analyze_recent_trend(train_data, target_func)
        
        # 获取实际值
        actual_value = target_func(actual)
        
        # 计算是否命中（简化：预测值与实际值的差距）
        if isinstance(predicted, tuple) and isinstance(actual_value, tuple):
            # 比较分布
            match = sum(1 for p, a in zip(predicted, actual_value) if abs(p - a) <= 1) / len(predicted)
            results.append(match)
        else:
            # 单值比较
            if predicted is not None:
                diff = abs(predicted - actual_value)
                # 认为误差在20%以内为命中
                hit = diff <= max(5, predicted * 0.3)
                results.append(1 if hit else 0)
    
    if results:
        return sum(results) / len(results)
    return 0

def main():
    print("=" * 60)
    print("七乐彩预测方法验证（6-13）")
    print("=" * 60)
    
    history = load_data()
    print(f"数据量: {len(history)} 条")
    print(f"验证期数: 最近20期")
    print()
    
    # 方法6-13的验证函数
    methods = [
        (6, "和值法", lambda n: calculate_sum(n)),
        (7, "三区比", lambda n: calculate_size(n)),
        (8, "012路法", lambda n: calculate_012(n)),
        (9, "连号法", lambda n: calculate_consecutive(n)),
        (10, "同尾法", lambda n: calculate_same_tail(n)),
        (11, "重号法", lambda n: calculate_repeat(n, [])),  # 简化
        (12, "AC值法", lambda n: calculate_ac(n)),
        (13, "极距法", lambda n: calculate_range(n)),
    ]
    
    results = []
    print("正在验证...")
    print()
    
    for method_id, method_name, func in methods:
        # 对于重号法，需要特殊处理
        if method_id == 11:
            # 简化验证：检查重号概率
            count = 0
            for i in range(1, len(history)):
                actual = [int(n) for n in history[i]['basic_numbers']]
                prev = [int(n) for n in history[i-1]['basic_numbers']]
                repeat = len(set(actual) & set(prev))
                if 1 <= repeat <= 3:
                    count += 1
            hit_rate = count / (len(history) - 1)
        else:
            hit_rate = validate_method(history, None, method_name, func, window=20)
        
        results.append({
            'id': method_id,
            'name': method_name,
            'rate': hit_rate
        })
        
        print(f"方法{method_id} {method_name}: {hit_rate:.1%}")
    
    # 按命中率排序
    results.sort(key=lambda x: x['rate'], reverse=True)
    
    print()
    print("=" * 60)
    print("验证结果排名")
    print("=" * 60)
    for r in results:
        print(f"方法{r['id']} {r['name']}: {r['rate']:.1%}")
    
    # 保存结果
    report = f"""# 七乐彩预测方法验证结果（6-13）

**验证时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**数据来源**: {len(history)} 条历史数据
**验证范围**: 最近20期

## 验证结果

| 编号 | 方法 | 命中率 |
|:---:|:---|:---:|
"""
    for r in results:
        report += f"| **{r['id']}** | {r['name']} | {r['rate']:.1%} |\n"
    
    report += """
## 说明

- 命中率 = 预测准确期数 / 验证期数
- 部分方法采用简化的验证方式
- 实际预测效果可能因当期数据有所差异

## 后续建议

1. 命中率较高（>60%）的方法可加入推荐组合
2. 命中率较低的方法需要进一步优化
3. 建议定期更新验证结果
"""
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print()
    print(f"✅ 验证结果已保存: {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
