#!/usr/bin/env python3
"""七乐彩预测引擎 V5.0 - 完整版"""

import json
import random
from typing import List, Dict
from collections import Counter

class PredictionEngineV5:
    """预测引擎 V5.0"""
    
    def __init__(self, history_file: str = '/home/lang/.openclaw/workspace/caipiao/qlc_history_full.json'):
        self.history = []
        self.history_file = history_file
        self.hot_numbers = []
        self.cold_numbers = []
        self.missing_values = {}
        
        # 加载数据
        self.load_history()
        
        # 分析数据
        self.analyze()
    
    def load_history(self) -> bool:
        """加载历史数据"""
        try:
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
            print(f"✅ 加载历史数据: {len(self.history)} 条")
            return True
        except Exception as e:
            print(f"❌ 加载失败: {e}")
            return False
    
    def analyze(self):
        """分析数据"""
        if not self.history:
            return
        
        recent = self.history[-10:]
        
        # 统计所有号码出现次数
        all_numbers = []
        for d in recent:
            all_numbers.extend([int(n) for n in d['basic_numbers']])
        
        freq = Counter(all_numbers)
        
        # 热号TOP10
        self.hot_numbers = [n for n, _ in freq.most_common(15)]
        
        # 冷号
        all_set = set(range(1, 31))
        recent_set = set(all_numbers)
        self.cold_numbers = sorted(all_set - recent_set, key=lambda x: freq.get(x, 0))
        
        # 遗漏值
        self.missing_values = {}
        for num in range(1, 31):
            for i, d in enumerate(reversed(recent)):
                if num in [int(n) for n in d['basic_numbers']]:
                    self.missing_values[num] = i
                    break
            else:
                self.missing_values[num] = 10
    
    def check_constraints(self, numbers: List[int]) -> bool:
        """检查约束"""
        # 奇偶分布
        odd_count = sum(1 for n in numbers if n % 2 == 1)
        if not (2 <= odd_count <= 5):
            return False
        
        # 大小分布
        small = sum(1 for n in numbers if n <= 10)
        medium = sum(1 for n in numbers if 11 <= n <= 20)
        large = sum(1 for n in numbers if n >= 21)
        
        if not (small <= 4 and medium <= 4 and large <= 4):
            return False
        
        return True
    
    def generate_predictions(self, count: int = 100) -> List[List[int]]:
        """生成预测"""
        if not self.history:
            print("❌ 没有历史数据")
            return []
        
        predictions = []
        attempts = 0
        
        # 按概率混合策略
        strategies = [
            ('hot', 0.4, self.hot_numbers[:15]),  # 40%热号为主
            ('missing', 0.3, sorted(self.missing_values.keys(), 
                                    key=lambda x: self.missing_values[x], reverse=True)[:15]),  # 30%遗漏为主
            ('random', 0.3, list(range(1, 31))),  # 30%随机
        ]
        
        while len(predictions) < count and attempts < 100000:
            attempts += 1
            
            # 选择策略
            r = random.random()
            cumulative = 0
            candidates = list(range(1, 31))
            
            for name, weight, pool in strategies:
                cumulative += weight
                if r <= cumulative:
                    candidates = pool.copy()
                    break
            
            # 随机选择7个号码
            selected = sorted(random.sample(candidates, 7))
            
            # 检查约束
            if not self.check_constraints(selected):
                continue
            
            # 避免重复
            if selected not in predictions:
                predictions.append(selected)
        
        print(f"✅ 生成 {len(predictions)} 组预测 (尝试{attempts}次)")
        return predictions
    
    def save_predictions(self, predictions: List[List[int]], 
                        filepath: str = '/home/lang/.openclaw/workspace/caipiao/predictions_v5.csv'):
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
    
    def generate_report(self) -> str:
        """生成分析报告"""
        if not self.history:
            return "❌ 没有历史数据"
        
        recent = self.history[-10:]
        all_numbers = []
        for d in recent:
            all_numbers.extend([int(n) for n in d['basic_numbers']])
        
        freq = Counter(all_numbers)
        hot = freq.most_common(10)
        
        report = f"""
七乐
分析彩预测分析报告期数: {len(recent)}期
数据总量: {len(self.history)}条
最新期号: {recent[0]['period']}

一、热号TOP10
"""
        
        for i, (num, count) in enumerate(hot, 1):
            report += f"{i:2d}. {num:02d}号: 出现{count}次\n"
        
        report += """
二、高遗漏号码
"""
        
        high_missing = sorted(self.missing_values.items(), 
                           key=lambda x: x[1], reverse=True)[:5]
        for num, gap in high_missing:
            report += f"  {num:02d}号: 已遗漏{gap}期\n"
        
        report += """
三、策略建议
1. 关注热号: 优先选择近期频繁出现的号码
2. 留意回补: 高遗漏号码可能有回补趋势
3. 分布均衡: 遵循奇偶和大小分布规律

---
七乐彩预测平台 V5.0
"""
        
        return report
    
    def save_report(self, report: str, 
                   filepath: str = '/home/lang/.openclaw/workspace/caipiao/v5_platform/logs/report_v5.txt'):
        """保存报告"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ 报告已保存: {filepath}")
            return True
        except Exception as e:
            print(f"❌ 保存失败: {e}")
            return False


def main():
    """主函数"""
    print("=" * 60)
    print("七乐彩预测引擎 V5.0")
    print("=" * 60)
    
    # 创建引擎
    engine = PredictionEngineV5()
    
    # 生成预测
    predictions = engine.generate_predictions(100)
    
    if predictions:
        # 保存预测
        engine.save_predictions(predictions)
        
        # 显示前10组
        print("\n前10组预测:")
        for i, pred in enumerate(predictions[:10], 1):
            print(f"  {i:3d}: {' '.join(f'{n:02d}' for n in pred)}")
        
        # 生成报告
        report = engine.generate_report()
        engine.save_report(report)
        print(f"\n{report}")
        
        return True
    
    return False


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
