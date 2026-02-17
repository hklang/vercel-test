#!/usr/bin/env python3
"""
Qilecai Prediction Tool - Flexible Combo
Support: single method, multi-method, select-then-filter
"""

import json
import sys
from pathlib import Path

PREDICT_DIR = '/home/lang/.openclaw/workspace/caipiao/v5_platform/predictions'

METHODS = {
    '1': '重号法', '2': '三区比', '3': '连号法', '4': '奇偶法',
    '5': '和值法', '6': '012路法', '7': '周期回补', '8': '极距法',
    '9': '热号法', '10': '同尾法', '11': 'AC值法', '12': '大小号',
    '13': '遗漏值', 'A': '稳扎稳打', 'B': '追热防冷',
}

COMBOS = {'A': '稳扎稳打', 'B': '追热防冷'}

def load_predictions():
    files = sorted(Path(PREDICT_DIR).glob('predictions_*.json'))
    if not files:
        return None
    with open(str(files[-1])) as f:
        return json.load(f)

def filter_by_method(predictions, method_name, count=5):
    method_data = predictions.get(method_name, {})
    return method_data.get('predictions', [])[:count]

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  qlc_combo.sh 1         # single method")
        print("  qlc_combo.sh 1,10,12  # multiple methods")
        print("  qlc_combo.sh 1>10      # select 10 from 1, filter 5 by 10")
        print("  qlc_combo.sh A         # combo A")
        return

    arg = sys.argv[1].strip()
    preds = load_predictions()
    if not preds:
        print("No prediction data. Run: qlc_predict.sh")
        return

    # Select-then-filter mode
    if '>' in arg:
        parts = arg.split('>')
        method1 = METHODS.get(parts[0], parts[0])
        method2 = METHODS.get(parts[1], parts[1])
        filtered = filter_by_method(preds, method2, 5)
        print(f"\nSelect 10 from [{method1}], filter 5 by [{method2}]:\n")
        for i, nums in enumerate(filtered, 1):
            print(f"  {i}: {' '.join(f'{n:02d}' for n in nums)}")
        return

    # Multi-method mode
    if ',' in arg:
        nums = arg.split(',')
        print(f"\nMultiple methods (5 each):\n")
        for num in nums:
            method = METHODS.get(num, num)
            groups = filter_by_method(preds, method, 5)
            print(f"[{method}]")
            for i, g in enumerate(groups, 1):
                print(f"  {i}: {' '.join(f'{n:02d}' for n in g)}")
            print()
        return

    # Combo mode
    if arg in COMBOS:
        combo = COMBOS[arg]
        print(f"\n[{combo}] Combo:\n")
        if combo == '稳扎稳打':
            g1 = filter_by_method(preds, '重号法', 5)
            g2 = filter_by_method(preds, '三区比', 5)
            print("重号法:")
            for i, g in enumerate(g1, 1):
                print(f"  {i}: {' '.join(f'{n:02d}' for n in g)}")
            print("\n三区比:")
            for i, g in enumerate(g2, 1):
                print(f"  {i}: {' '.join(f'{n:02d}' for n in g)}")
        else:
            g1 = filter_by_method(preds, '热号法', 5)
            g2 = filter_by_method(preds, '遗漏值', 5)
            print("热号法:")
            for i, g in enumerate(g1, 1):
                print(f"  {i}: {' '.join(f'{n:02d}' for n in g)}")
            print("\n遗漏值:")
            for i, g in enumerate(g2, 1):
                print(f"  {i}: {' '.join(f'{n:02d}' for n in g)}")
        return

    # Single method
    method = METHODS.get(arg, arg)
    print(f"\n[{method}] (5 groups):\n")
    groups = filter_by_method(preds, method, 5)
    for i, g in enumerate(groups, 1):
        print(f"  {i}: {' '.join(f'{n:02d}' for n in g)}")

if __name__ == '__main__':
    main()
