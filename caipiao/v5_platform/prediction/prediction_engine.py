#!/usr/bin/env python3
"""预测引擎 - 完整版"""

import json
from typing import List, Dict, Optional
from datetime import datetime

class PredictionEngine:
    """预测引擎"""
    
    def __init__(self):
        self.checker = ConstraintChecker()
        self.scorer = ConfidenceScorer()
        self.history = []
    
    def load_history(self, filepath: str = '/home/lang/.openclaw/workspace/caipiao/qlc_history_full.json'):
        """加载历史数据"""
        try:
            with open(filepath, 'r') as f:
                self.history = json.load(f)
            print(f"✅ 加载历史数据: {len(self.history)} 条")
            return True
        except Exception as e:
            print(f"❌ 加载失败: {e}")
            return False
    
    def generate_prediction(self, count: int = 100) -> List[List[int]]:
        """生成预测"""
        if not self.history:
            print("❌ 没有历史数据")
            return []
        
        # 使用最后10期分析趋势
        recent = self.history[-10:]
        
        # 统计频率
        from collections import Counter
        all_nums = []
        for d in recent:
            all_nums.extend([int(n) for n in d['basic_numbers']])
        
        freq = Counter(all_nums)
        hot_nums = [n for n, _ in freq.most_common(15)]
        
        # 遗漏值
        missing = {}
        for num in range(1, 31):
            for i, d in enumerate(reversed(recent)):
                if num in [int(n) for n in d['basic_numbers']]:
                    missing[num] = i
                    break
            else:
                missing[num] = 10
        
        missing_sorted = sorted(missing.keys(), key=lambda x: missing[x], reverse=True)
        
        predictions = []
        attempts = 0
        
        while len(predictions) < count and attempts < 50000:
            attempts += 1
            
            import random
            
            # 策略：混合热号和遗漏
            if random.random() < 0.6:
                candidates = hot_nums[:15].copy()
            else:
                candidates = missing_sorted[:15].copy()
            
            if len(candidates) < 7:
                candidates = list(range(1, 31))
            
            selected = sorted(random.sample(candidates, 7))
            
            # 约束检查（放宽条件）
            if not self.checker.check(selected):
                continue
            
            # 避免重复
            key = tuple(selected)
            if key not in [tuple(p) for p in predictions]:
                predictions.append(selected)
        
        print(f"✅ 生成 {len(predictions)} 组预测 (尝试{attempts}次)")
        return predictions
    
    def save_predictions(self, predictions: List[List[int]], filepath: str = '/home/lang/.openclaw/workspace/caipiao/predictions_v5.csv'):
        """保存预测"""
        try:
            with open(filepath, 'w', encoding='utf-8-sig') as f:
                f.write('序号,号码1,号码2,号码3,号码4,号码5,号码6,号码7\n')
                for i, pred in enumerate(predictions, 1):
                    f.write(f'{i},{",".join(map(str, pred))}\n')
            print(f"✅ 保存预测: {filepath}")
            return True
        except Exception as e:
            print(f"❌ 保存失败: {e}")
            return False

class ConstraintChecker:
    """约束检查器"""
    
    def check(self, numbers: List[int]) -> bool:
        return self.check_parity(numbers) and self.check_size(numbers)
    
    def check_parity(self, numbers: List[int]) -> bool:
        odd = sum(1 for n in numbers if n % 2 == 1)
        return 3 <= odd <= 5
    
    def check_size(self, numbers: List[int]) -> bool:
        small = sum(1 for n in numbers if n <= 10)
        medium = sum(1 for n in numbers if 11 <= n <= 20)
        large = sum(1 for n in numbers if n >= 21)
        return (small, medium, large) in [(2,3,2), (3,2,2), (3,3,1), (2,2,3)]

class ConfidenceScorer:
    """信心评分器"""
    
    def score(self, numbers: List[int], analysis: Dict = None) -> float:
        score = 0.0
        
        # 基础分
        score += 10.0
        
        # 热号加分
        if analysis and 'hot' in analysis:
            hot_count = sum(1 for n in numbers if n in analysis['hot'][:8])
            score += hot_count * 5
        
        return score

def main():
    """主函数"""
    print("=" * 60)
    print("七乐彩预测引擎 V5.0")
    print("=" * 60)
    
    engine = PredictionEngine()
    
    # 加载数据
    if not engine.load_history():
        return
    
    # 生成预测
    predictions = engine.generate_prediction(100)
    
    if predictions:
        # 保存
        engine.save_predictions(predictions)
        
        # 显示前10组
        print("\n前10组预测:")
        for i, pred in enumerate(predictions[:10], 1):
            print(f"  {i:3d}: {pred}")
        
        return True
    
    return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
