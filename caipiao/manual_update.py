#!/usr/bin/env python3
"""
七乐彩手动更新脚本
用于在数据源故障时手动添加开奖号码
"""

import json
from datetime import datetime

DATA_FILE = '/home/lang/.openclaw/workspace/caipiao/qlc_history_full.json'

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def add_manual_result(period, date, numbers, special):
    """手动添加开奖结果"""
    data = load_data()
    
    # 检查是否已存在
    exists = any(d['period'] == period for d in data)
    if exists:
        print(f"❌ 期号 {period} 已存在")
        return False
    
    # 添加新记录
    new_record = {
        "period": period,
        "date": date,
        "basic_numbers": [str(n).zfill(2) for n in numbers],
        "special_number": str(special).zfill(2)
    }
    
    data.append(new_record)
    data.sort(key=lambda x: x['period'])
    
    save_data(data)
    print(f"✅ 添加成功: {period} - {date} - {numbers} (特别号: {special})")
    return True

def show_latest():
    """显示最新开奖数据"""
    data = load_data()
    print(f"\n总数据: {len(data)} 条")
    print("\n最新10期:")
    for d in data[-10:]:
        print(f"  {d['period']} - {d['date']} - {d['basic_numbers']} (特:{d.get('special_number', '-')})")

def main():
    import sys
    
    print("=" * 60)
    print("七乐彩手动更新工具")
    print("=" * 60)
    
    if len(sys.argv) >= 2:
        # 命令行参数模式
        if sys.argv[1] == 'latest':
            show_latest()
        elif sys.argv[1] == 'add' and len(sys.argv) >= 6:
            period = sys.argv[2]
            date = sys.argv[3]
            numbers = [int(x) for x in sys.argv[4:10]]
            special = int(sys.argv[10])
            add_manual_result(period, date, numbers, special)
        else:
            print("用法:")
            print("  python3 manual_update.py latest        # 查看最新")
            print("  python3 manual_update.py add <期号> <日期> <7个号码> <特别号>")
            print("  示例: python3 manual_update.py add 2026019 2026-02-13 01 05 09 12 15 18 22 25")
    else:
        # 交互模式
        show_latest()
        print("\n" + "=" * 60)
        print("输入新开奖数据:")
        print("=" * 60)
        
        period = input("期号 (如 2026019): ").strip()
        date = input("日期 (如 2026-02-13): ").strip()
        
        print("输入7个基本号码 (用空格分隔): ")
        numbers = []
        for i in range(7):
            num = input(f"  号码{i+1}: ").strip()
            numbers.append(int(num))
        
        special = input("特别号码: ").strip()
        
        add_manual_result(period, date, numbers, special)
        
        # 重新运行分析
        print("\n运行分析...")
        import subprocess
        subprocess.run(['python3', 'analyze.py'])

if __name__ == '__main__':
    main()
