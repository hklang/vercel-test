#!/usr/bin/env python3
"""模型集成"""

import numpy as np
from typing import List, Dict

class ModelEnsemble:
    def __init__(self):
        self.models = []
        self.weights = []
    
    def add_model(self, model, predict_func, weight=1.0):
        self.models.append({'model': model, 'predict': predict_func, 'weight': weight})
        self.weights.append(weight)
    
    def predict(self, data) -> List[int]:
        all_scores = np.zeros(30)
        
        for m_info in self.models:
            pred = m_info['predict'](data)
            for num in pred:
                all_scores[num-1] += m_info['weight']
        
        return np.argsort(all_scores)[::-1][:7].tolist()

def main():
    def pred1(d): return [1, 2, 3, 4, 5, 6, 7]
    def pred2(d): return [3, 4, 5, 6, 7, 8, 9]
    
    ensemble = ModelEnsemble()
    ensemble.add_model({}, pred1, 0.4)
    ensemble.add_model({}, pred2, 0.6)
    
    result = ensemble.predict({})
    
    return len(result) == 7

if __name__ == '__main__':
    success = main()
    print("✅ 模型集成测试通过" if success else "❌ 测试失败")
    exit(0 if success else 1)
