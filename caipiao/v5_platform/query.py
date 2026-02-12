#!/usr/bin/env python3
"""
预测结果查询系统
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

PREDICT_DIR = Path('/home/lang/.openclaw/workspace/caipiao/v5_platform/predictions')
RESULTS_DIR = Path('/home/lang/.openclaw/workspace/caipiao/v5_platform/results')


def list_all():
    """列出所有预测"""
    print("\n" + "="*60)
    print("历史预测记录")
    print("="*60 + "\n")
    
    files = sorted(PREDICT_DIR.glob('predictions_*.json'), reverse=True)
    
    for f in files:
        name = f.name.replace('predictions_', '').replace('.json', '')
        
        # 解析日期
        try:
            dt = datetime.strptime(name, '%Y%m%d_%H%M')
            date_str = dt.strftime('%Y-%m-%d %H:%M')
        except:
            date_str = name
        
        # 检查验证状态
        period = name.split('_')[0]
        result_file = RESULTS_DIR / f"verify_{period}.json"
        status = "[已验证]" if result_file.exists() else "[待验证]"
        
        print(f"  {date_str}  {status}")
    
    print(f"\n总计: {len(files)} 条预测记录\n")


def show(date_str):
    """显示预测"""
    print("\n" + "="*60)
    print(f"预测结果 - {date_str}")
    print("="*60)
    
    # 查找文件
    patterns = [
        f"predictions_{date_str}*.json",
        f"predictions_{date_str.replace('-', '')}*.json",
    ]
    
    files = []
    for p in patterns:
        files.extend(list(PREDICT_DIR.glob(p)))
    
    if not files:
        print(f"\n未找到 {date_str} 的预测记录\n")
        return
    
    with open(files[0], 'r', encoding='utf-8') as f:
        predictions = json.load(f)
    
    for method_name, data in predictions.items():
        print(f"\n【{method_name}】")
        print(f"  依据: {data.get('依据', '')}")
        print(f"  预测10组:")
        for i, pred in enumerate(data.get('predictions', [])[:10], 1):
            nums = ' '.join(f"{n:02d}" for n in pred)
            print(f"    {i:2d}: {nums}")


def verify(period):
    """显示验证结果"""
    print("\n" + "="*60)
    print(f"验证结果 - 期号 {period}")
    print("="*60)
    
    result_file = RESULTS_DIR / f"verify_{period}.json"
    
    if not result_file.exists():
        print(f"\n未找到 {period} 的验证结果\n")
        return
    
    with open(result_file, 'r', encoding='utf-8') as f:
        result = json.load(f)
    
    print(f"\n开奖号码: {' '.join(f'{n:02d}' for n in result.get('actual', []))}\n")
    
    print("【13种方法】")
    for method_name, data in result.get('results', {}).items():
        print(f"  {method_name}: （3+）{data['hit3']:.0%}（4+）{data['hit4']:.0%}（5+）{data['hit5']:.0%}")


def main():
    if len(sys.argv) < 2:
        list_all()
        print("使用说明:")
        print("  python3 query.py --list           # 列出所有预测")
        print("  python3 query.py --show 20260212  # 显示预测")
        print("  python3 query.py --verify 2026018 # 显示验证结果")
        return
    
    if sys.argv[1] == '--list':
        list_all()
    elif sys.argv[1] == '--show' and len(sys.argv) > 2:
        show(sys.argv[2])
    elif sys.argv[1] == '--verify' and len(sys.argv) > 2:
        verify(sys.argv[2])
    else:
        print("用法: query.py [--list|--show 日期|--verify 期号]")


if __name__ == '__main__':
    main()
