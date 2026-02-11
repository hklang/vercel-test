#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七乐彩智能预测系统 - 自我学习版
功能：
1. 读取历史数据和经验
2. 生成预测组合
3. 自动对比开奖结果
4. 更新经验文件
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple

# ================== 路径配置 ==================
BASE_DIR = "/home/lang/.openclaw/workspace/caipiao"
DATA_FILE = f"{BASE_DIR}/latest_7lc.txt"
EXPERIENCE_DIR = f"{BASE_DIR}/经验库"

# ================== 经验文件（拆分存储） ==================
EXP_BASE = f"{EXPERIENCE_DIR}/基础规则.json"        # 基础预测规则
EXP_WEIGHT = f"{EXPERIENCE_DIR}/指标权重.json"      # 各指标准确率权重
EXP_TREND = f"{EXPERIENCE_DIR}/趋势记录.json"       # 最近趋势
EXP_HOT_COLD = f"{EXPERIENCE_DIR}/冷热规律.json"    # 冷热号规律
EXP_RECENT = f"{EXPERIENCE_DIR}/最近对比.json"      # 最近10期对比记录


def load_history_data() -> List[Dict]:
    """加载历史开奖数据"""
    data = []
    try:
        with open(DATA_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 10:
                    issue = parts[0]
                    date = parts[1]
                    numbers = [int(x) for x in parts[2:9]]
                    special = int(parts[9])
                    data.append({
                        'issue': issue,
                        'date': date,
                        'numbers': numbers,
                        'special': special
                    })
    except Exception as e:
        print(f"加载数据失败: {e}")
    return data


def load_experience() -> Dict:
    """加载所有经验文件"""
    exp = {
        'base_rules': {},
        'weights': {},
        'trend': [],
        'hot_cold': {'hot': [], 'cold': [], 'warm': []},
        'recent_compare': []
    }
    
    # 加载基础规则
    if os.path.exists(EXP_BASE):
        with open(EXP_BASE, 'r') as f:
            exp['base_rules'] = json.load(f)
    
    # 加载指标权重
    if os.path.exists(EXP_WEIGHT):
        with open(EXP_WEIGHT, 'r') as f:
            exp['weights'] = json.load(f)
    
    # 加载趋势记录
    if os.path.exists(EXP_TREND):
        with open(EXP_TREND, 'r') as f:
            exp['trend'] = json.load(f)
    
    # 加载冷热规律
    if os.path.exists(EXP_HOT_COLD):
        with open(EXP_HOT_COLD, 'r') as f:
            exp['hot_cold'] = json.load(f)
    
    # 加载最近对比
    if os.path.exists(EXP_RECENT):
        with open(EXP_RECENT, 'r') as f:
            exp['recent_compare'] = json.load(f)
    
    return exp


def save_experience(exp: Dict):
    """保存经验文件（拆分存储）"""
    # 保存基础规则
    with open(EXP_BASE, 'w') as f:
        json.dump(exp.get('base_rules', {}), f, ensure_ascii=False, indent=2)
    
    # 保存指标权重
    with open(EXP_WEIGHT, 'w') as f:
        json.dump(exp.get('weights', {}), f, ensure_ascii=False, indent=2)
    
    # 保存趋势记录（保留最近20条）
    with open(EXP_TREND, 'w') as f:
        json.dump(exp.get('trend', [])[-20:], f, ensure_ascii=False, indent=2)
    
    # 保存冷热规律
    with open(EXP_HOT_COLD, 'w') as f:
        json.dump(exp.get('hot_cold', {}), f, ensure_ascii=False, indent=2)
    
    # 保存最近对比（保留最近10条）
    with open(EXP_RECENT, 'w') as f:
        json.dump(exp.get('recent_compare', [])[-10:], f, ensure_ascii=False, indent=2)


def analyze_history(data: List[Dict], count: int = 10) -> Dict:
    """分析最近N期的数据规律"""
    recent = data[:count]
    
    # 基础统计
    stats = {
        'avg_sum': sum(sum(d['numbers']) for d in recent) / count,
        'odd_even_ratio': [],  # 奇数:偶数
        'range_ratio': [],     # 三区比
        '012_ratio': [],       # 012路
        'consecutive_count': [],  # 连号数量
        'repeat_count': 0,     # 重号数量
    }
    
    for i, d in enumerate(recent):
        nums = d['numbers']
        
        # 奇偶比
        odd = len([n for n in nums if n % 2 == 1])
        stats['odd_even_ratio'].append(f"{odd}:{7-odd}")
        
        # 三区比
        q1 = len([n for n in nums if 1 <= n <= 10])
        q2 = len([n for n in nums if 11 <= n <= 20])
        q3 = len([n for n in nums if 21 <= n <= 30])
        stats['range_ratio'].append(f"{q1}:{q2}:{q3}")
        
        # 012路
        c0 = len([n for n in nums if n % 3 == 0])
        c1 = len([n for n in nums if n % 3 == 1])
        c2 = len([n for n in nums if n % 3 == 2])
        stats['012_ratio'].append(f"{c0}:{c1}:{c2}")
        
        # 连号
        consecutive = sum(1 for i in range(6) if nums[i+1] - nums[i] == 1)
        stats['consecutive_count'].append(consecutive)
        
        # 重号（与前一期对比）
        if i > 0:
            repeat = len(set(nums) & set(recent[i-1]['numbers']))
            stats['repeat_count'] += repeat
    
    return stats


def predict_next(exp: Dict, data: List[Dict]) -> Tuple[List[int], Dict]:
    """基于经验和数据预测下一期"""
    stats = analyze_history(data, 10)
    base_rules = exp.get('base_rules', {})
    weights = exp.get('weights', {})
    
    # 预测指标
    predictions = {
        'sum_range': base_rules.get('sum_range', [90, 120]),
        'odd_even': stats['odd_even_ratio'][-1],  # 跟随最近一期
        'range_ratio': stats['range_ratio'][-1],
        '012_ratio': stats['012_ratio'][-1],
        'consecutive': stats['consecutive_count'][-1],
    }
    
    # 生成预测号码（简化版：基于热号和趋势）
    hot_numbers = []
    cold_numbers = []
    
    # 从最近数据提取热号（出现频率高的号码）
    frequency = {}
    for d in data[:10]:
        for n in d['numbers']:
            frequency[n] = frequency.get(n, 0) + 1
    
    # 排序
    sorted_nums = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    hot_numbers = [n for n, c in sorted_nums[:10]]
    cold_numbers = [n for n, c in sorted_nums if c == 1][:5]
    
    # 生成组合（确保包含热号和冷号）
    result = hot_numbers[:5] + cold_numbers[:2]
    result = sorted(list(set(result)))
    
    # 补足7个号码
    all_numbers = list(range(1, 31))
    for n in all_numbers:
        if n not in result and len(result) < 7:
            result.append(n)
    
    return sorted(result[:7]), predictions


def compare_and_update(data: List[Dict], prediction: List[int], issue: str):
    """对比预测和实际，更新经验"""
    # 找到实际开奖
    actual = None
    for d in data:
        if d['issue'] == issue:
            actual = d['numbers']
            break
    
    if not actual:
        return None
    
    # 计算命中率
    hit_count = len(set(prediction) & set(actual))
    hit_rate = hit_count / 7
    
    # 更新最近对比
    exp = load_experience()
    compare_record = {
        'issue': issue,
        'date': data[0].get('date', '') if data else '',
        'prediction': prediction,
        'actual': actual,
        'hit_count': hit_count,
        'hit_rate': round(hit_rate, 4),
        'time': datetime.now().isoformat()
    }
    
    exp['recent_compare'].append(compare_record)
    exp['recent_compare'] = exp['recent_compare'][-10:]
    
    # 更新趋势
    trend_record = {
        'issue': issue,
        'hit_rate': round(hit_rate, 4),
        'time': datetime.now().isoformat()
    }
    exp['trend'].append(trend_record)
    exp['trend'] = exp['trend'][-20:]
    
    # 更新指标权重（根据命中率调整）
    # 这里可以添加更复杂的权重更新逻辑
    
    save_experience(exp)
    
    return compare_record


def predict_batch(data: List[Dict], exp: Dict, start_idx: int = 1, count: int = 10) -> List[Dict]:
    """批量预测历史期数，用于验证准确率"""
    results = []
    
    for i in range(start_idx, min(start_idx + count, len(data))):
        # 预测第 i 期（基于 i+1 期及以后的数据）
        predict_data = data[i+1:]
        if not predict_data:
            break
            
        prediction, _ = predict_next(exp, predict_data)
        actual = data[i]['numbers']
        issue = data[i]['issue']
        
        hit_count = len(set(prediction) & set(actual))
        hit_rate = hit_count / 7
        
        result = {
            'issue': issue,
            'prediction': prediction,
            'actual': actual,
            'hit_count': hit_count,
            'hit_rate': round(hit_rate, 4),
            'time': datetime.now().isoformat()
        }
        results.append(result)
        
        # 每5期输出一次
        if len(results) % 5 == 0:
            print(f"   已完成 {len(results)}/{count} 期...")
    
    return results


def main():
    """主函数：批量预测历史期数，验证准确率"""
    output = []
    output.append("="*60)
    output.append("🧠 七乐彩自我学习预测系统 - 历史验证版")
    output.append(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("="*60)
    
    # 1. 加载数据
    data = load_history_data()
    if not data:
        output.append("❌ 无历史数据")
        print('\n'.join(output))
        return
    
    output.append(f"📊 历史数据: {len(data)} 期")
    output.append("")
    
    # 2. 加载经验
    exp = load_experience()
    output.append("📚 已加载经验文件")
    
    # 3. 批量预测最近20期
    output.append("")
    output.append("🔮 开始批量预测（最近20期）...")
    output.append("-"*60)
    
    results = predict_batch(data, exp, start_idx=1, count=20)
    
    if not results:
        output.append("❌ 预测失败")
        print('\n'.join(output))
        return
    
    # 4. 显示详细结果
    for r in results:
        status = "✅" if r['hit_rate'] >= 0.5 else ("⚠️" if r['hit_rate'] >= 0.3 else "❌")
        output.append(f"{r['issue']} | 预测:{sorted(r['prediction'])} | 命中:{r['hit_count']}/7 {r['hit_rate']*100:.1f}% {status}")
    
    output.append("-"*60)
    
    # 5. 统计汇总
    total = len(results)
    hit_0 = sum(1 for r in results if r['hit_rate'] == 0)
    hit_1 = sum(1 for r in results if r['hit_rate'] == 1/7)
    hit_2 = sum(1 for r in results if r['hit_rate'] == 2/7)
    hit_3 = sum(1 for r in results if r['hit_rate'] >= 3/7)
    
    avg_hit = sum(r['hit_rate'] for r in results) / total
    
    output.append("")
    output.append("📊 预测统计:")
    output.append(f"   总预测: {total} 期")
    output.append(f"   平均命中率: {avg_hit*100:.1f}%")
    output.append(f"   命中0个: {hit_0} 次 ({hit_0/total*100:.0f}%)")
    output.append(f"   命中1个: {hit_1} 次 ({hit_1/total*100:.0f}%)")
    output.append(f"   命中2个: {hit_2} 次 ({hit_2/total*100:.0f}%)")
    output.append(f"   命中3+个: {hit_3} 次 ({hit_3/total*100:.0f}%)")
    
    # 6. 保存对比结果
    output.append("")
    output.append("💾 保存对比结果...")
    exp['recent_compare'] = results[-10:]
    
    # 更新趋势
    exp['trend'] = results[-20:]
    
    # 更新基础规则（根据命中率调整）
    if avg_hit < 0.2:
        # 命中率太低，扩大和值范围
        base = exp.get('base_rules', {})
        base['sum_range'] = [70, 150]  # 扩大范围
        exp['base_rules'] = base
        output.append("   ⚠️ 命中率低，扩大和值范围至 [70, 150]")
    
    save_experience(exp)
    output.append("   ✅ 已保存")
    
    # 7. 最佳预测
    best = max(results, key=lambda x: x['hit_rate'])
    output.append("")
    output.append(f"🏆 最佳预测: {best['issue']}期，命中{best['hit_count']}/7 ({best['hit_rate']*100:.1f}%)")
    
    output.append("="*60)
    
    print('\n'.join(output))
    return '\n'.join(output)


if __name__ == "__main__":
    main()
