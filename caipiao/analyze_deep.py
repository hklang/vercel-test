#!/usr/bin/env python3
"""
七乐彩深度分析脚本 V3
利用大数据分析，找出隐藏规律
"""

import json
from collections import Counter, defaultdict
from datetime import datetime
from itertools import combinations

DATA_FILE = '/home/lang/.openclaw/workspace/caipiao/qlc_history_full.json'

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def analyze_basic_patterns(history):
    """基础规律分析"""
    print("\n" + "=" * 60)
    print("一、基础规律分析")
    print("=" * 60)
    
    # 奇偶分布
    parities = []
    for draw in history:
        odd = sum(1 for n in draw['basic_numbers'] if int(n) % 2 == 1)
        parities.append(odd)
    
    print("\n奇偶分布:")
    for num, count in Counter(parities).most_common():
        pct = count / len(parities) * 100
        bar = "█" * int(pct / 2)
        print(f"  {num}个奇数: {count:4d}次 ({pct:5.1f}%) {bar}")
    
    # 大小分布
    print("\n大小分布 (1-10/11-20/21-30):")
    sizes = []
    for draw in history:
        small = sum(1 for n in draw['basic_numbers'] if int(n) <= 10)
        medium = sum(1 for n in draw['basic_numbers'] if 11 <= int(n) <= 20)
        large = sum(1 for n in draw['basic_numbers'] if int(n) >= 21)
        sizes.append((small, medium, large))
    
    for size, count in Counter(sizes).most_common(5):
        pct = count / len(sizes) * 100
        bar = "█" * int(pct)
        print(f"  {size[0]}-{size[1]}-{size[2]}: {count:4d}次 ({pct:5.1f}%) {bar}")

def analyze_combinations(history):
    """组合规律分析"""
    print("\n" + "=" * 60)
    print("二、组合规律分析")
    print("=" * 60)
    
    # 统计所有两两组合
    pair_counts = Counter()
    triple_counts = Counter()
    
    for draw in history:
        nums = [int(n) for n in draw['basic_numbers']]
        
        # 两两组合
        for pair in combinations(sorted(nums), 2):
            pair_counts[pair] += 1
        
        # 三三组合
        for triple in combinations(sorted(nums), 3):
            triple_counts[triple] += 1
    
    print("\n最常见的两两组合 (TOP10):")
    for pair, count in pair_counts.most_common(10):
        pct = count / len(history) * 100
        print(f"  {pair[0]:2d} - {pair[1]:2d}: {count:3d}次 ({pct:.1f}%)")
    
    print("\n最常见的三三组合 (TOP10):")
    for triple, count in triple_counts.most_common(10):
        pct = count / len(history) * 100
        print(f"  {triple}: {count:3d}次 ({pct:.1f}%)")

def analyze_number_cycles(history):
    """号码周期分析"""
    print("\n" + "=" * 60)
    print("三、号码周期分析")
    print("=" * 60)
    
    # 计算每个号码的平均间隔
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
    
    print("\n号码平均间隔周期:")
    sorted_nums = sorted(intervals.keys(), key=lambda x: sum(intervals[x]) / len(intervals[x]))
    for num in sorted_nums[:10]:
        avg = sum(intervals[num]) / len(intervals[num])
        print(f"  {num:2d}: 平均{avg:.1f}期出现一次")
    
    print("\n最稳定的号码 (周期波动小):")
    sorted_stable = sorted(intervals.keys(), key=lambda x: (sum(intervals[x]) / len(intervals[x]), max(intervals[x]) - min(intervals[x])))
    for num in sorted_stable[:10]:
        avg = sum(intervals[num]) / len(intervals[num])
        var = max(intervals[num]) - min(intervals[num])
        print(f"  {num:2d}: 周期{avg:.1f}±{var:.1f}期")

def analyze_trends(history, window=10):
    """趋势分析"""
    print("\n" + "=" * 60)
    print("四、趋势分析 (最近10期)")
    print("=" * 60)
    
    recent = history[-window:]
    
    # 热号
    all_nums = []
    for draw in recent:
        all_nums.extend([int(n) for n in draw['basic_numbers']])
    
    hot_counter = Counter(all_nums)
    print("\n热号 TOP10:")
    for num, count in hot_counter.most_common(10):
        bar = "█" * count
        print(f"  {num:2d}: {count:2d}次 {bar}")
    
    # 冷号
    cold_nums = [n for n in range(1, 31) if n not in hot_counter]
    cold_counter = Counter({n: hot_counter.get(n, 0) for n in cold_nums})
    print("\n冷号 TOP10:")
    for num, count in sorted(cold_counter.items(), key=lambda x: x[1])[:10]:
        print(f"  {num:2d}: {count}次")
    
    # 遗漏值
    print("\n遗漏值最大的号码:")
    current = recent[0]
    missing = []
    for num in range(1, 31):
        for i, draw in enumerate(reversed(recent)):
            if num in [int(n) for n in draw['basic_numbers']]:
                missing.append((num, i))
                break
        else:
            missing.append((num, window))
    
    for num, gap in sorted(missing, key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {num:2d}: 已遗漏{gap}期")

def generate_strategies(history):
    """生成策略建议"""
    print("\n" + "=" * 60)
    print("五、策略建议")
    print("=" * 60)
    
    recent = history[-10:]
    
    # 分析最近趋势
    hot_counter = Counter()
    for draw in recent:
        hot_counter.update([int(n) for n in draw['basic_numbers']])
    
    # 最热的5个号码
    top_hot = [n for n, _ in hot_counter.most_common(5)]
    
    # 最冷的5个号码
    all_nums = set(range(1, 31))
    recent_nums = set(hot_counter.keys())
    cold_nums = sorted(all_nums - recent_nums, key=lambda x: hot_counter.get(x, 0))
    top_cold = cold_nums[:5]
    
    # 回补信号（遗漏值高的号码）
    missing = []
    for num in range(1, 31):
        for i, draw in enumerate(reversed(recent)):
            if num in [int(n) for n in draw['basic_numbers']]:
                missing.append((num, i))
                break
        else:
            missing.append((num, 10))
    
    back补充 = [n for n, g in sorted(missing, key=lambda x: x[1], reverse=True)[:5]]
    
    print("\n推荐策略:")
    print(f"\n🔥 热号策略 (出现频繁):")
    print(f"   重点关注: {top_hot}")
    print(f"   建议: 每组至少包含2-3个热号")
    
    print(f"\n❄️ 冷号策略 (长期未出):")
    print(f"   关注回补: {top_cold}")
    print(f"   建议: 包含1-2个冷号作为补充")
    
    print(f"\n📈 回补信号 (遗漏值高):")
    print(f"   可能出现: {back补充}")
    print(f"   建议: 遗漏>5期的号码重点考虑")

def main():
    print("=" * 60)
    print("七乐彩深度分析报告 V3")
    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("=" * 60)
    
    history = load_data()
    print(f"\n数据量: {len(history)} 期")
    print(f"最新期号: {history[-1]['period']}")
    print(f"最新号码: {history[-1]['basic_numbers']}")
    
    # 基础分析
    analyze_basic_patterns(history)
    
    # 组合分析
    analyze_combinations(history)
    
    # 周期分析
    analyze_number_cycles(history)
    
    # 趋势分析
    analyze_trends(history)
    
    # 策略建议
    generate_strategies(history)
    
    print("\n" + "=" * 60)
    print("分析完成")
    print("=" * 60)

if __name__ == '__main__':
    main()
