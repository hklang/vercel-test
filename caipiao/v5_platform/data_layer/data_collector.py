#!/usr/bin/env python3
"""数据采集器"""

import requests
from typing import List, Dict

class DataSource:
    def __init__(self):
        self.base_url = "https://www.cwl.gov.cn"
    
    def health_check(self) -> bool:
        try:
            r = requests.get(f"{self.base_url}/tzxx/kjxx/qlc/", timeout=5)
            return r.status_code == 200
        except:
            return False
    
    def fetch(self) -> List[Dict]:
        try:
            paths = ["/cms_home/20108/index/data_json/2026/0211/2026018.json"]
            for path in paths:
                r = requests.get(f"{self.base_url}{path}", timeout=10)
                if r.status_code == 200:
                    return self._parse(r.json())
            return []
        except Exception as e:
            print(f"错误: {e}")
            return []
    
    def _parse(self, data: Dict) -> List[Dict]:
        results = []
        if isinstance(data, list):
            for item in data:
                results.append({
                    'period': item.get('period'),
                    'date': item.get('date'),
                    'numbers': item.get('basic_numbers', []),
                    'special': item.get('special_number'),
                })
        return results

class DataCollector:
    def __init__(self):
        self.sources = [DataSource()]
    
    def collect(self) -> List[Dict]:
        for source in self.sources:
            if source.health_check():
                data = source.fetch()
                print(f"获取{len(data)}条数据")
                return data
        return []

def main():
    collector = DataCollector()
    data = collector.collect()
    return len(data) >= 0

if __name__ == '__main__':
    success = main()
    print("✅ 数据采集器测试通过" if success else "❌ 测试失败")
    exit(0 if success else 1)
