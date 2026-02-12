#!/usr/bin/env python3
"""随机森林模型"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from typing import List, Dict

class RandomForestModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=50, max_depth=5)
    
    def prepare_data(self, history: List[Dict]) -> tuple:
        X, y = [], []
        for i in range(len(history) - 1):
            recent = history[:i+1]
            # 简化的特征
            nums = [int(n) for d in recent for n in d['numbers']]
            X.append([nums.count(n) for n in range(1, 31)])
            
            next_nums = [int(n) for n in history[i+1]['numbers']]
            y.append([1 if n in next_nums else 0 for n in range(1, 31)])
        
        return np.array(X), np.array(y)
    
    def train(self, X, y):
        self.model.fit(X, y)
        return self
    
    def predict(self, X) -> List[int]:
        proba = self.model.predict_proba(X)[0]
        return np.argsort(proba)[::-1][:7].tolist()

def main():
    history = [
        {'numbers': [1, 5, 9, 12, 15, 18, 22]},
        {'numbers': [2, 6, 10, 13, 16, 19, 23]},
        {'numbers': [3, 7, 11, 14, 17, 20, 24]},
    ]
    
    m = RandomForestModel()
    X, y = m.prepare_data(history)
    
    if len(X) > 0:
        m.train(X, y)
        pred = m.predict(X[-1:])
        return len(pred) == 7
    return False

if __name__ == '__main__':
    success = main()
    print("✅ 随机森林模型测试通过" if success else "❌ 测试失败")
    exit(0 if success else 1)
