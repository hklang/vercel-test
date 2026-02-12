#!/usr/bin/env python3
"""
七乐彩预测分析脚本
功能：
1. 分析最近10期各方法表现
2. 动态调整权重
3. 更新预测策略
"""

import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

# 读取历史数据
DATA_FILE = '/home/lang/.openclaw/workspace/caipiao/qlc_history_full.json'
WEIGHTS_FILE = '/home/lang/.openclaw/workspace/caipiao/weights.json'

def load_history():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def load_weights():
    """加载权重配置"""
    try:
        with open(WEIGHTS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {
            'missing': 0.60,  # 遗漏值法
            'hot': 0.20,      # 热号法
            'random': 0.20,   # 随机法
            'history': []     # 权重调整历史
        }

def save_weights(weights):
    """保存权重配置"""
    with open(WEIGHTS_FILE, 'w') as f:
        json.dump(weights, f, indent=2)

def analyze_hot_cold(history, window=10):
    """分析热号和冷号"""
    recent_numbers = []
    for draw in history[-window:]:
        recent_numbers.extend(draw['basic_numbers'])
    
    counter = Counter(recent_numbers)
    hot = [num for num, count in counter.most_common(10)]  # 出现次数最多的
    cold = [num for num, count in counter.most_common()[-10:]]  # 出现次数最少的
    
    return hot, cold

def analyze_parity_distribution(history, window=20):
    """分析奇偶分布"""
    parities = []
    for draw in history[-window:]:
        odd_count = sum(1 for n in draw['basic_numbers'] if int(n) % 2 == 1)
        parities.append(odd_count)
    
    most_common = Counter(parities).most_common(1)[0][0]
    return most_common

def analyze_size_distribution(history, window=20):
    """分析大小分布 (1-10/11-20/21-30)"""
    distributions = []
    for draw in history[-window:]:
        small = sum(1 for n in draw['basic_numbers'] if int(n) <= 10)
        medium = sum(1 for n in draw['basic_numbers'] if 11 <= int(n) <= 20)
        large = sum(1 for n in draw['basic_numbers'] if int(n) >= 21)
        distributions.append((small, medium, large))
    
    # 找出最常见的分布
    most_common = Counter(distributions).most_common(1)[0][0]
    return most_common

def evaluate_prediction_methods(history, window=20):
    """评估各预测方法在最近的表现"""
    # 模拟各方法在最近window期的预测
    
    results = {
        'missing_method': [],  # 遗漏值法
        'hot_method': [],      # 热号法
        'random_method': [],   # 随机法
    }
    
    for i in range(window, len(history)):
        # 实际上我们无法准确模拟预测，只能分析趋势
        # 这里用历史数据做一些简单分析
        
        period = history[i]['period']
        winning = set(history[i]['basic_numbers'])
        
        # 分析遗漏值分布
        missing_values = {}
        for num in range(1, 31):
            appeared = False
            for j in range(i-1, -1, -1):
                if str(num) in history[j]['basic_numbers']:
                    missing_values[num] = i - j
                    appeared = True
                    break
            if not appeared:
                missing_values[num] = float('inf')
        
        # 遗漏最大的10个号码
        top_missing = [str(num) for num, _ in sorted(missing_values.items(), key=lambda x: x[1], reverse=True)[:10]]
        missing_hits = len(set(top_missing) & winning)
        results['missing_method'].append(missing_hits)
        
        # 热号（前10个）
        recent_numbers = []
        for j in range(max(0, i-window), i):
            recent_numbers.extend(history[j]['basic_numbers'])
        hot_counter = Counter(recent_numbers)
        top_hot = [num for num, _ in hot_counter.most_common(10)]
        hot_hits = len(set(top_hot) & winning)
        results['hot_method'].append(hot_hits)
        
        # 随机（平均命中）
        avg_random = 10 * 7 / 30  # 期望值
        results['random_method'].append(avg_random)
    
    # 计算平均命中
    avg_missing = sum(results['missing_method'][-window:]) / window
    avg_hot = sum(results['hot_method'][-window:]) / window
    avg_random = sum(results['random_method'][-window:]) / window
    
    return {
        'missing': avg_missing,
        'hot': avg_hot,
        'random': avg_random,
        'recent_window': results['missing_method'][-window:]
    }

def adjust_weights(evaluation, current_weights):
    """根据评估结果调整权重"""
    scores = {
        'missing': evaluation['missing'],
        'hot': evaluation['hot'],
        'random': evaluation['random']
    }
    
    total = sum(scores.values())
    if total == 0:
        return current_weights
    
    # 基础权重（根据表现）
    new_weights = {
        'missing': scores['missing'] / total,
        'hot': scores['hot'] / total,
        'random': scores['random'] / total,
        'history': current_weights.get('history', [])
    }
    
    # 添加调整记录
    record = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'scores': scores,
        'weights': {
            'missing': round(new_weights['missing'], 2),
            'hot': round(new_weights['hot'], 2),
            'random': round(new_weights['random'], 2)
        }
    }
    new_weights['history'].append(record)
    
    # 保留最近20条记录
    if len(new_weights['history']) > 20:
        new_weights['history'] = new_weights['history'][-20:]
    
    return new_weights

def generate_report(history, weights, evaluation):
    """生成分析报告"""
    hot, cold = analyze_hot_cold(history)
    parity = analyze_parity_distribution(history)
    size_dist = analyze_size_distribution(history)
    
    report = f"""
七乐彩预测分析报告
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

一、当前权重配置
━━━━━━━━━━━━━━━━━━━━━━
遗漏值法: {weights['missing']*100:.0f}%
热号法:   {weights['hot']*100:.0f}%
随机法:   {weights['random']*100:.0f}%

二、历史表现（最近10期平均）
━━━━━━━━━━━━━━━━━━━━━━
遗漏值法平均命中: {evaluation['missing']:.2f}个
热号法平均命中: {evaluation['hot']:.2f}个
随机法平均命中: {evaluation['random']:.2f}个

三、分布规律
━━━━━━━━━━━━━━━━━━━━━━
奇偶分布众数: {parity}个奇数
大小分布众数: 小区{size_dist[0]}个 / 中区{size_dist[1]}个 / 大区{size_dist[2]}个

四、热号 TOP10
━━━━━━━━━━━━━━━━━━━━━━
{', '.join(hot[:10])}

五、冷号 TOP10
━━━━━━━━━━━━━━━━━━━━━━
{', '.join(cold[:10])}

六、建议
━━━━━━━━━━━━━━━━━━━━━━
"""
    
    # 根据分析给出建议
    if evaluation['missing'] > evaluation['hot']:
        report += "• 遗漏值法表现优于热号法，建议保持或增加其权重\n"
    else:
        report += "• 热号法表现优于遗漏值法，建议适当增加热号权重\n"
    
    report += f"• 奇偶比例建议: {parity}奇{7-parity}偶\n"
    report += f"• 大小分布建议: {size_dist[0]}-{size_dist[1]}-{size_dist[2]}\n"
    
    return report

def main():
    print("=" * 60)
    print("七乐彩预测分析脚本")
    print("=" * 60)
    
    # 加载数据
    history = load_history()
    weights = load_weights()
    
    print(f"\n历史数据: {len(history)} 期")
    print(f"最新期号: {history[-1]['period']}")
    
    # 评估各方法
    evaluation = evaluate_prediction_methods(history, window=10)
    
    # 调整权重
    new_weights = adjust_weights(evaluation, weights)
    
    # 生成报告
    report = generate_report(history, new_weights, evaluation)
    print(report)
    
    # 保存新权重
    if new_weights != weights:
        save_weights(new_weights)
        print("\n✅ 权重已更新！")
    else:
        print("\n⚪ 权重无需调整")
    
    # 保存报告
    report_file = f'/home/lang/.openclaw/workspace/caipiao/analysis_report_{datetime.now().strftime("%Y%m%d")}.txt'
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"📄 报告已保存: {report_file}")

if __name__ == '__main__':
    main()
