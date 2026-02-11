#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七乐彩预测经验学习系统
核心：记录预测方法的经验教训，而非预测结果
支持方法：热号法、冷号法、遗漏值法、奇偶法、大小号法
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple
from collections import Counter

# ================== 路径配置 ==================
BASE_DIR = "/home/lang/.openclaw/workspace/caipiao"
DATA_FILE = f"{BASE_DIR}/latest_7lc.txt"
EXP_DIR = f"{BASE_DIR}/经验库"

# ================== 经验文件 ==================
EXP_METHODS = f"{EXP_DIR}/方法经验.json"    # 预测方法的有效性
EXP_RULES = f"{EXP_DIR}/规则调整.json"     # 规则调整记录
EXP_LESSONS = f"{EXP_DIR}/教训总结.json"   # 失败教训


def load_history_data() -> List[Dict]:
    """加载历史数据"""
    data = []
    try:
        with open(DATA_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 10:
                    data.append({
                        'issue': parts[0],
                        'date': parts[1],
                        'numbers': [int(x) for x in parts[2:9]],
                        'special': int(parts[9])
                    })
    except Exception as e:
        print(f"加载数据失败: {e}")
    return data


def load_experience() -> Dict:
    """加载所有经验"""
    return {
        'methods': load_json(EXP_METHODS, {}),
        'rules': load_json(EXP_RULES, {}),
        'lessons': load_json(EXP_LESSONS, [])
    }


def load_json(path: str, default):
    """安全加载JSON"""
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            pass
    return default


def save_experience(exp: Dict):
    """保存经验"""
    # 保存方法经验
    with open(EXP_METHODS, 'w') as f:
        json.dump(exp.get('methods', {}), f, ensure_ascii=False, indent=2)
    
    # 保存规则调整
    with open(EXP_RULES, 'w') as f:
        json.dump(exp.get('rules', {}), f, ensure_ascii=False, indent=2)
    
    # 保存教训（保留最近20条）
    with open(EXP_LESSONS, 'w') as f:
        json.dump(exp.get('lessons', [])[-20:], f, ensure_ascii=False, indent=2)


def analyze_issue(data: List[Dict], idx: int) -> Dict:
    """分析单期特征"""
    nums = data[idx]['numbers']
    next_nums = data[idx+1]['numbers'] if idx+1 < len(data) else []
    
    return {
        'issue': data[idx]['issue'],
        'numbers': nums,
        'sum': sum(nums),
        'odd_count': len([n for n in nums if n % 2 == 1]),
        'even_count': 7 - len([n for n in nums if n % 2 == 1]),
        'range_q1': len([n for n in nums if 1 <= n <= 10]),
        'range_q2': len([n for n in nums if 11 <= n <= 20]),
        'range_q3': len([n for n in nums if 21 <= n <= 30]),
        'consecutive': sum(1 for i in range(6) if nums[i+1] - nums[i] == 1),
        'repeat_with_next': len(set(nums) & set(next_nums)) if next_nums else 0,
        'repeat_with_prev': len(set(nums) & set(data[idx-1]['numbers'])) if idx > 0 else 0,
    }


def predict_with_hot(data: List[Dict], idx: int) -> Dict:
    """方法1：基于热号预测"""
    # 取最近10期（不包括当前期）
    recent = data[idx+1:idx+11]
    if not recent:
        return {'method': 'hot', 'numbers': [], 'reason': '数据不足'}
    
    # 统计出现频率
    freq = Counter()
    for d in recent:
        freq.update(d['numbers'])
    
    top7 = [n for n, _ in freq.most_common(7)]
    return {
        'method': 'hot',
        'numbers': sorted(top7),
        'reason': '选取最近10期出现频率最高的7个号码'
    }


def predict_with_cold(data: List[Dict], idx: int) -> Dict:
    """方法2：基于冷号回补预测"""
    recent = data[idx+1:idx+11]
    if not recent:
        return {'method': 'cold', 'numbers': [], 'reason': '数据不足'}
    
    freq = Counter()
    for d in recent:
        freq.update(d['numbers'])
    
    # 所有号码
    all_nums = set(range(1, 31))
    appeared = set(freq.keys())
    not_appeared = all_nums - appeared
    
    # 冷号（未出现）+ 温号（出现1-2次）
    cold = list(not_appeared)
    warm = [n for n, c in freq.items() if c <= 2]
    
    # 选5个温号 + 2个冷号
    selection = sorted(warm[:5] + cold[:2])
    return {
        'method': 'cold',
        'numbers': selection,
        'reason': '5个温号(出现1-2次) + 2个冷号(未出现)'
    }


def predict_with_missing(data: List[Dict], idx: int) -> Dict:
    """方法3：基于遗漏值预测（回补理论）"""
    recent = data[idx+1:idx+31]  # 最近30期
    if not recent or len(recent) < 10:
        return {'method': 'missing', 'numbers': [], 'reason': '数据不足'}
    
    # 计算每个号码的遗漏值（距上次出现的期数）
    last_appearance = {}
    for i, d in enumerate(recent):
        for num in d['numbers']:
            last_appearance[num] = i  # 记录最近一次出现的位置
    
    # 遗漏值最大的号码（很长时间没出现的）
    all_nums = set(range(1, 31))
    for num in all_nums:
        if num not in last_appearance:
            last_appearance[num] = len(recent) + 1  # 从未出现
    
    # 选择遗漏值最大的7个号码
    sorted_by_missing = sorted(last_appearance.items(), key=lambda x: x[1], reverse=True)
    selected = [n for n, _ in sorted_by_missing[:7]]
    
    return {
        'method': 'missing',
        'numbers': sorted(selected),
        'reason': '选取遗漏值最大的7个号码（回补理论）'
    }


def predict_with_odd_even(data: List[Dict], idx: int) -> Dict:
    """方法4：基于奇偶分布预测"""
    recent = data[idx+1:idx+11]
    if not recent or len(recent) < 5:
        return {'method': 'odd_even', 'numbers': [], 'reason': '数据不足'}
    
    # 分析最近10期的奇偶分布
    odd_counts = []
    for d in recent:
        nums = d['numbers']
        odd_counts.append(len([n for n in nums if n % 2 == 1]))
    
    # 取众数
    odd_mode = Counter(odd_counts).most_common(1)[0][0]
    even_mode = 7 - odd_mode
    
    # 选取对应数量的奇数和偶数
    all_odd = [n for n in range(1, 31) if n % 2 == 1]
    all_even = [n for n in range(1, 31) if n % 2 == 0]
    
    # 从历史出现频率中选择
    freq = Counter()
    for d in recent:
        freq.update(d['numbers'])
    
    odd_nums = sorted([n for n in all_odd if n in freq], key=lambda x: freq.get(x, 0), reverse=True)[:odd_mode]
    even_nums = sorted([n for n in all_even if n in freq], key=lambda x: freq.get(x, 0), reverse=True)[:even_mode]
    
    # 如果数量不足，从未出现的补足
    while len(odd_nums) < odd_mode:
        remaining = [n for n in all_odd if n not in odd_nums]
        if remaining:
            odd_nums.append(remaining[-1])
        else:
            break
    
    while len(even_nums) < even_mode:
        remaining = [n for n in all_even if n not in even_nums]
        if remaining:
            even_nums.append(remaining[-1])
        else:
            break
    
    selection = odd_nums + even_nums
    return {
        'method': 'odd_even',
        'numbers': sorted(selection),
        'reason': f'奇偶分布{odd_mode}:{even_mode}（众数），选取高频奇偶号'
    }


def predict_with_range(data: List[Dict], idx: int) -> Dict:
    """方法5：基于区间分布预测（大小号法）"""
    recent = data[idx+1:idx+11]
    if not recent or len(recent) < 5:
        return {'method': 'range', 'numbers': [], 'reason': '数据不足', 'q1': 0, 'q2': 0, 'q3': 0}
    
    # 分析最近10期的区间分布
    q1_counts, q2_counts, q3_counts = [], [], []
    for d in recent:
        nums = d['numbers']
        q1_counts.append(len([n for n in nums if 1 <= n <= 10]))      # 小号区
        q2_counts.append(len([n for n in nums if 11 <= n <= 20]))     # 中号区
        q3_counts.append(len([n for n in nums if 21 <= n <= 30]))     # 大号区
    
    # 取众数
    q1_mode = Counter(q1_counts).most_common(1)[0][0]
    q2_mode = Counter(q2_counts).most_common(1)[0][0]
    q3_mode = Counter(q3_counts).most_common(1)[0][0]
    
    # 确保总和为7
    total = q1_mode + q2_mode + q3_mode
    if total != 7:
        q3_mode = 7 - q1_mode - q2_mode
    
    # 选取对应区间的号码
    range1 = [n for n in range(1, 11)]
    range2 = [n for n in range(11, 21)]
    range3 = [n for n in range(21, 31)]
    
    freq = Counter()
    for d in recent:
        freq.update(d['numbers'])
    
    nums1 = sorted(range1, key=lambda x: freq.get(x, 0), reverse=True)[:q1_mode]
    nums2 = sorted(range2, key=lambda x: freq.get(x, 0), reverse=True)[:q2_mode]
    nums3 = sorted(range3, key=lambda x: freq.get(x, 0), reverse=True)[:q3_mode]
    
    selection = nums1 + nums2 + nums3
    
    return {
        'method': 'range',
        'numbers': sorted(selection),
        'reason': f'区间分布{q1_mode}:{q2_mode}:{q3_mode}（众数），选取高频号码',
        'q1': q1_mode, 'q2': q2_mode, 'q3': q3_mode
    }


def evaluate_methods(data: List[Dict], exp: Dict, count: int = 10) -> Dict:
    """评估各种预测方法的有效性"""
    results = {
        'hot': {'hit_rates': [], 'hit_counts': [], 'avg': 0, 'hit_3plus': 0},
        'cold': {'hit_rates': [], 'hit_counts': [], 'avg': 0, 'hit_3plus': 0},
        'missing': {'hit_rates': [], 'hit_counts': [], 'avg': 0, 'hit_3plus': 0},
        'odd_even': {'hit_rates': [], 'hit_counts': [], 'avg': 0, 'hit_3plus': 0},
        'range': {'hit_rates': [], 'hit_counts': [], 'avg': 0, 'hit_3plus': 0},
    }
    
    for i in range(count):
        if i+1 >= len(data):
            break
            
        actual = set(data[i]['numbers'])
        
        # 方法1：热号预测
        hot_pred = predict_with_hot(data, i)
        if hot_pred['numbers']:
            hot_hits = len(set(hot_pred['numbers']) & actual)
            hot_rate = hot_hits / 7
            results['hot']['hit_rates'].append(hot_rate)
            results['hot']['hit_counts'].append(hot_hits)
        
        # 方法2：冷号预测
        cold_pred = predict_with_cold(data, i)
        if cold_pred['numbers']:
            cold_hits = len(set(cold_pred['numbers']) & actual)
            cold_rate = cold_hits / 7
            results['cold']['hit_rates'].append(cold_rate)
            results['cold']['hit_counts'].append(cold_hits)
        
        # 方法3：遗漏值预测
        missing_pred = predict_with_missing(data, i)
        if missing_pred['numbers']:
            missing_hits = len(set(missing_pred['numbers']) & actual)
            missing_rate = missing_hits / 7
            results['missing']['hit_rates'].append(missing_rate)
            results['missing']['hit_counts'].append(missing_hits)
        
        # 方法4：奇偶预测
        odd_even_pred = predict_with_odd_even(data, i)
        if odd_even_pred['numbers']:
            odd_even_hits = len(set(odd_even_pred['numbers']) & actual)
            odd_even_rate = odd_even_hits / 7
            results['odd_even']['hit_rates'].append(odd_even_rate)
            results['odd_even']['hit_counts'].append(odd_even_hits)
        
        # 方法5：区间分布预测
        range_pred = predict_with_range(data, i)
        if range_pred['numbers']:
            range_hits = len(set(range_pred['numbers']) & actual)
            range_rate = range_hits / 7
            results['range']['hit_rates'].append(range_rate)
            results['range']['hit_counts'].append(range_hits)
    
    # 计算平均值
    for method in results:
        rates = results[method]['hit_rates']
        if rates:
            results[method]['avg'] = sum(rates) / len(rates)
            results[method]['hit_3plus'] = sum(1 for r in rates if r >= 3/7)
            results[method]['total'] = len(rates)
            results[method]['hit_3plus_rate'] = results[method]['hit_3plus'] / len(rates)
    
    return results


def extract_lessons(results: Dict, exp: Dict) -> List[str]:
    """从结果中提取教训"""
    lessons = []
    
    methods_data = {
        'hot': '热号法',
        'cold': '冷号法',
        'missing': '遗漏值法',
        'odd_even': '奇偶法',
        'range': '大小号法'
    }
    
    # 找出最佳方法
    best_method = None
    best_avg = -1
    for method, data in results.items():
        if data.get('avg', 0) > best_avg:
            best_avg = data.get('avg', 0)
            best_method = method
    
    if best_method:
        lessons.append(f"🏆 最佳方法: {methods_data.get(best_method, best_method)}，平均命中率 {best_avg*100:.1f}%")
    
    # 分析各方法表现
    for method, data in results.items():
        avg = data.get('avg', 0)
        method_name = methods_data.get(method, method)
        
        if avg < 0.15:
            lessons.append(f"⚠️ {method_name}表现不佳，平均命中率仅{avg*100:.1f}%")
        elif avg > 0.30:
            lessons.append(f"✅ {method_name}表现良好，平均命中率{avg*100:.1f}%")
    
    # 比较热号和冷号
    hot_avg = results.get('hot', {}).get('avg', 0)
    cold_avg = results.get('cold', {}).get('avg', 0)
    if hot_avg > cold_avg:
        lessons.append(f"📊 热号法({hot_avg*100:.1f}%)优于冷号法({cold_avg*100:.1f}%)，当前趋势偏向热号")
    else:
        lessons.append(f"📊 冷号法({cold_avg*100:.1f}%)优于热号法({hot_avg*100:.1f}%)，存在回补可能")
    
    # 遗漏值分析
    missing_avg = results.get('missing', {}).get('avg', 0)
    if missing_avg > hot_avg and missing_avg > cold_avg:
        lessons.append(f"💡 遗漏回补理论有效，遗漏值法命中率{missing_avg*100:.1f}%")
    
    return lessons


def main():
    """主函数：评估预测方法，记录经验"""
    output = []
    output.append("="*70)
    output.append("🧠 七乐彩预测经验学习系统")
    output.append(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("="*70)
    
    # 1. 加载数据
    data = load_history_data()
    if not data:
        output.append("❌ 无历史数据")
        print('\n'.join(output))
        return
    
    output.append(f"📊 历史数据: {len(data)} 期")
    
    # 2. 加载已有经验
    exp = load_experience()
    output.append("📚 已加载经验文件")
    
    # 3. 评估各种预测方法
    output.append("")
    output.append("🔍 评估预测方法（最近20期）...")
    results = evaluate_methods(data, exp, count=20)
    
    # 4. 分析结果
    output.append("-"*70)
    
    methods_info = {
        'hot': '热号法',
        'cold': '冷号法',
        'missing': '遗漏值法',
        'odd_even': '奇偶法',
        'range': '大小号法'
    }
    
    # 打印各方法结果
    for method, data in results.items():
        if data.get('total', 0) > 0:
            avg = data['avg'] * 100
            hit_3plus_rate = data['hit_3plus_rate'] * 100
            total = data['total']
            hit_3plus = data['hit_3plus']
            
            symbol = '📈' if method == 'hot' else '📉' if method == 'cold' else '📊'
            output.append(f"{symbol} {methods_info.get(method, method)}: 平均{avg:.1f}% | 命中3+次:{hit_3plus}/{total}({hit_3plus_rate:.0f}%)")
    
    output.append("")
    
    # 5. 提取教训并保存
    lessons = extract_lessons(results, exp)
    for lesson in lessons:
        output.append(lesson)
    
    # 更新经验
    methods = exp.get('methods', {})
    
    for method, data in results.items():
        if data.get('total', 0) > 0:
            methods[f'{method}_avg'] = round(data['avg'], 4)
            methods[f'{method}_3plus_rate'] = round(data['hit_3plus_rate'], 4)
    
    # 确定最佳方法
    best_method = None
    best_avg = -1
    for method, data in results.items():
        if data.get('avg', 0) > best_avg:
            best_avg = data.get('avg', 0)
            best_method = method
    
    if best_method:
        methods['best_method'] = best_method
        methods['best_method_name'] = methods_info.get(best_method, best_method)
        methods['best_avg'] = round(best_avg, 4)
    
    # 保存教训
    new_lessons = [{
        'time': datetime.now().isoformat(),
        'lessons': lessons,
        'results': {m: results[m].get('avg', 0) for m in results}
    }]
    exp['lessons'].extend(new_lessons)
    exp['lessons'] = exp['lessons'][-10:]
    exp['methods'] = methods
    
    save_experience(exp)
    output.append("")
    output.append("💾 经验已保存")
    
    # 6. 显示保存的经验摘要
    output.append("")
    output.append("📋 当前方法经验摘要:")
    for method in ['hot', 'cold', 'missing', 'odd_even', 'range']:
        if method in methods:
            name = methods_info.get(method, method)
            avg = methods.get(f'{method}_avg', 0) * 100
            output.append(f"   {name}: {avg:.1f}%")
    
    output.append(f"   🏆 最佳方法: {methods.get('best_method_name', 'N/A')}")
    
    output.append("="*70)
    
    print('\n'.join(output))
    return '\n'.join(output)


if __name__ == "__main__":
    main()
