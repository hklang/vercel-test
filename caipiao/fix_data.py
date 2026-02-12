#!/usr/bin/env python3
"""
手动添加七乐彩开奖数据 - 最小版本
只添加已知的数据
"""

import json
from datetime import datetime

# 已知的数据（从用户反馈）
KNOWN_RESULTS = {
    # 2026001期及之后的数据（用户需要提供）
}

# 用户已确认的数据
CONFIRMED_RESULTS = {
    "2026018": {"date": "2026-02-11", "numbers": ["12", "15", "16", "18", "19", "23", "29"], "special": "26"},
}

def main():
    # 读取现有数据
    with open('/home/lang/.openclaw/workspace/caipiao/qlc_history_full.json', 'r') as f:
        data = json.load(f)
    
    # 删除损坏的数据（2007001及之后）
    valid_data = [d for d in data if not d.get('period', '').startswith('2007')]
    
    print(f"清理后: {len(valid_data)} 条数据")
    print(f"最后一条: {valid_data[-1]['period']} - {valid_data[-1]['date']}")
    
    # 添加确认的数据
    added = []
    for period, info in CONFIRMED_RESULTS.items():
        exists = any(d['period'] == period for d in valid_data)
        if not exists:
            new_record = {
                "period": period,
                "date": info['date'],
                "basic_numbers": info['numbers'],
                "special_number": info['special']
            }
            valid_data.append(new_record)
            added.append(period)
            print(f"添加: {period} - {info['numbers']}")
    
    if not added:
        print("\n⚠️ 2026018期已存在")
    
    # 按期号排序
    valid_data.sort(key=lambda x: x['period'])
    
    # 保存
    with open('/home/lang/.openclaw/workspace/caipiao/qlc_history_full.json', 'w') as f:
        json.dump(valid_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n保存完成: {len(valid_data)} 条数据")
    
    # 显示最新5条
    print("\n最新5条:")
    for d in valid_data[-5:]:
        print(f"  {d['period']} - {d['date']} - {d['basic_numbers']}")

if __name__ == '__main__':
    main()
