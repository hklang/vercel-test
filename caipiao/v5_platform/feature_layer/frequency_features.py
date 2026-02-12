#!/usr/bin/env python3
"""频率特征提取器"""

from collections import Counter
from typing import Dict, List

class FrequencyFeatures:
    def __init__(self, history: List[Dict], windows: List[int] = [5, 10, 20]):
        self.history = history
        self.windows = windows
    
    def extract(self) -> Dict[str, int]:
        features = {}
        for w in self.windows:
            recent = self.history[-w:]
            counts = Counter()
            for d in recent:
                counts.update([int(n) for n in d['basic_numbers']])
            features[f'freq_{w}_mean'] = sum(counts.values()) / 30
            for n in range(1, 31):
                features[f'freq_{w}_{n}'] = counts.get(n, 0)
        return features

def main():
    history = [
        {'numbers': [1, 5, 9, 12, 15, 18, 22]},
        {'numbers': [2, 6, 10, 13, 16, 19, 23]},
    ]
    f = FrequencyFeatures(history, windows=[2]).extract()
    return len(f) > 10

if __name__ == '__main__':
    success = main()
    print("✅ 频率特征测试通过" if success else "❌ 测试失败")
    exit(0 if success else 1)
