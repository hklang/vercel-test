#!/usr/bin/env python3
"""数据清洗器"""

import re
from typing import List, Dict, Optional

class DataCleaner:
    def clean_period(self, value: str) -> Optional[str]:
        if not value: return None
        cleaned = re.sub(r'[\s\-_]', '', str(value))
        return cleaned if re.match(r'^\d{7}$', cleaned) else None
    
    def clean_numbers(self, values: List) -> List[int]:
        if not isinstance(values, list): return []
        cleaned = []
        for v in values:
            try:
                num = int(v)
                if 1 <= num <= 30:
                    cleaned.append(num)
            except: continue
        return sorted(set(cleaned))
    
    def clean(self, record: Dict) -> Optional[Dict]:
        cleaned = {}
        if 'period' in record:
            p = self.clean_period(record['period'])
            if p: cleaned['period'] = p
        if 'numbers' in record:
            nums = self.clean_numbers(record['numbers'])
            if len(nums) == 7:
                cleaned['numbers'] = nums
        return cleaned if cleaned else None
    
    def clean_all(self, data: List[Dict]) -> List[Dict]:
        return [r for r in [self.clean(d) for d in data] if r]

def main():
    cleaner = DataCleaner()
    test = [{'period': '2026001', 'numbers': ['01', '05', '10', '15', '20', '25', '30']}]
    result = cleaner.clean_all(test)
    return len(result) == 1 and result[0]['numbers'] == [1, 5, 10, 15, 20, 25, 30]

if __name__ == '__main__':
    success = main()
    print("✅ 数据清洗器测试通过" if success else "❌ 测试失败")
    exit(0 if success else 1)
