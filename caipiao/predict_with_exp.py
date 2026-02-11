#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七乐彩预测 - 基于已学经验
预测前先读取经验，使用最佳方法
"""

import json
import os
from datetime import datetime
from collections import Counter
from typing import List, Dict

BASE_DIR = "/home/lang/.openclaw/workspace/caipiao"
DATA_FILE = f"{BASE_DIR}/latest_7lc.txt"
EXP_DIR = f"{BASE_DIR}/经验库"


def load_data():
    """加载历史数据"""
    data = []
    with open(DATA_FILE, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 10:
                data.append({
                    'issue': parts[0],
                    'date': parts[1],
                    'numbers': [int(x) for x in parts[2:9]]
                })
    return data


def load_experience():
    """加载已学经验"""
    methods = {}
    rules = {}
    
    path = f"{EXP_DIR}/方法经验.json"
    if os.path.exists(path):
        with open(path, 'r') as f:
            methods = json.load(f)
    
    path = f"{EXP_DIR}/规则调整.json"
    if os.path.exists(path):
        with open(path, 'r') as f:
            rules = json.load(f)
    
    return methods, rules


def predict_with_method(data: List[Dict], method: str, range_param: int = 10) -> Dict:
    """根据指定方法预测"""
    
    if method == 'hot':
        # 热号法：取最近N期出现频率最高的号码
        recent = data[1:1+range_param]
        freq = Counter()
        for d in recent:
            freq.update(d['numbers'])
        top7 = [n for n, _ in freq.most_common(7)]
        return {
            'method': 'hot',
            'numbers': sorted(top7),
            'range': range_param,
            'confidence': methods.get('hot_avg', 0.24)
        }
    
    elif method == 'cold':
        # 冷号法：选温号+冷号
        recent = data[1:1+range_param]
        freq = Counter()
        for d in recent:
            freq.update(d['numbers'])
        
        all_nums = set(range(1, 31))
        appeared = set(freq.keys())
        not_appeared = all_nums - appeared
        
        cold = list(not_appeared)[:2]
        warm = [n for n, c in freq.items() if c <= 2][:5]
        selection = sorted(warm + cold)
        
        return {
            'method': 'cold',
            'numbers': selection,
            'range': range_param,
            'confidence': methods.get('cold_avg', 0.19)
        }
    
    return {'method': method, 'numbers': [], 'error': '未知方法'}


def main():
    """预测下一期"""
    output = []
    output.append("="*60)
    output.append("🎯 七乐彩预测（基于已学经验）")
    output.append(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("="*60)
    
    data = load_data()
    global methods, rules
    methods, rules = load_experience()
    
    output.append(f"📊 历史数据: {len(data)} 期")
    output.append("")
    output.append("📖 已学经验:")
    output.append(f"   热号法平均命中率: {methods.get('hot_avg', 0)*100:.1f}%")
    output.append(f"   冷号法平均命中率: {methods.get('cold_avg', 0)*100:.1f}%")
    output.append(f"   最佳方法: {methods.get('best_method', 'hot')}")
    output.append("")
    
    # 根据经验选择最佳方法
    best = methods.get('best_method', 'hot')
    output.append(f"🔮 使用【{best}】法预测下一期:")
    
    pred = predict_with_method(data, best)
    
    output.append(f"   号码: {' '.join(f'{n:02d}' for n in pred['numbers'])}")
    output.append(f"   置信度: {pred.get('confidence', 0)*100:.1f}%")
    
    # 与最新一期对比
    latest = data[0]
    hits = len(set(pred['numbers']) & set(latest['numbers']))
    
    output.append("")
    output.append("📊 验证（vs最新一期）:")
    output.append(f"   实际: {' '.join(f'{n:02d}' for n in latest['numbers'])}")
    output.append(f"   命中: {hits}/7 ({hits/7*100:.1f}%)")
    
    output.append("="*60)
    
    print('\n'.join(output))
    return '\n'.join(output)


if __name__ == "__main__":
    main()
