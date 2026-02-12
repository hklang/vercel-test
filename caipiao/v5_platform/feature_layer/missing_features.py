#!/usr/bin/env python3
"""遗漏特征提取器"""

from typing import Dict, List

class MissingFeatures:
    def __init__(self, history: List[Dict]):
        self.history = history
    
    def extract(self) -> Dict[str, int]:
        features = {}
        for num in range(1, 31):
            missing = 0
            for d in reversed(self.history):
                if num in [int(n) for n in d['basic_numbers']]:
                    break
                missing += 1
            features[f'missing_{num}'] = missing
        return features

def main():
    history = [{'numbers': [1, 5, 9, 12, 15, 18, 22]}]
    m = MissingFeatures(history).extract()
    return 'missing_1' in m and 'missing_30' in m

if __name__ == '__main__':
    success = main()
    print("✅ 遗漏特征测试通过" if success else "❌ 测试失败")
    exit(0 if success else 1)
