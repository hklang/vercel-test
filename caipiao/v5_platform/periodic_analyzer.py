#!/usr/bin/env python3
"""
周期性分析器 - V7.1新增算法
分析号码的周期性规律
"""

from collections import Counter
from typing import Dict, List, Tuple


class PeriodicAnalyzer:
    """周期性分析器 - 分析号码的周期性规律"""
    
    def __init__(self, history: List[Dict]):
        self.history = history
        self.periodicity = {}  # 号码的周期
    
    def analyze(self) -> Dict:
        """分析周期性"""
        results = {}
        
        # 1. 星期规律分析
        results['weekday'] = self._analyze_weekday()
        
        # 2. 周期性分析（每N期出现一次）
        results['cycle'] = self._analyze_cycle()
        
        # 3. 奇偶交替规律
        results['odd_even_alternate'] = self._analyze_odd_even_alternate()
        
        # 4. 大小交替规律
        results['size_alternate'] = self._analyze_size_alternate()
        
        # 5. 位置周期性
        results['position_cycle'] = self._analyze_position_cycle()
        
        return results
    
    def _analyze_weekday(self) -> Dict:
        """分析星期规律"""
        weekday_counts = {i: Counter() for i in range(7)}  # 0=周一
        
        for i, d in enumerate(self.history):
            weekday = i % 7
            for n in d['basic_numbers']:
                weekday_counts[weekday][int(n)] += 1
        
        # 找出每个星期最常出现的号码
        result = {}
        for wd in range(7):
            if weekday_counts[wd]:
                top = weekday_counts[wd].most_common(5)
                result[f'weekday_{wd}'] = [n for n, c in top]
        
        return result
    
    def _analyze_cycle(self) -> Dict:
        """分析周期性（每N期出现一次）"""
        results = {}
        
        for num in range(1, 31):
            appearances = []
            for i, d in enumerate(reversed(self.history)):
                if num in [int(n) for n in d['basic_numbers']]:
                    appearances.append(i)
            
            if len(appearances) >= 3:
                # 计算间隔
                intervals = [appearances[i+1] - appearances[i] for i in range(len(appearances)-1)]
                avg_interval = sum(intervals) / len(intervals)
                results[f'num_{num}'] = {
                    'appearances': len(appearances),
                    'avg_interval': avg_interval,
                    'next_expected': avg_interval - appearances[0] if appearances else None,
                }
        
        return results
    
    def _analyze_odd_even_alternate(self) -> Dict:
        """分析奇偶交替规律"""
        patterns = []
        
        for i in range(1, len(self.history)):
            current = [int(n) for n in self.history[-i]['basic_numbers']]
            previous = [int(n) for n in self.history[-i-1]['basic_numbers']]
            
            current_odd = sum(1 for n in current if n % 2 == 1)
            previous_odd = sum(1 for n in previous if n % 2 == 1)
            
            patterns.append(('odd' if current_odd > previous_odd else 'even', current_odd))
        
        return {'patterns': patterns[-20:]}
    
    def _analyze_size_alternate(self) -> Dict:
        """分析大小交替规律"""
        patterns = []
        
        for i in range(1, min(50, len(self.history))):
            current = [int(n) for n in self.history[-i]['basic_numbers']]
            previous = [int(n) for n in self.history[-i-1]['basic_numbers']]
            
            current_large = sum(1 for n in current if n >= 21)
            previous_large = sum(1 for n in previous if n >= 21)
            
            patterns.append(('large' if current_large > previous_large else 'small', current_large))
        
        return {'patterns': patterns[-20:]}
    
    def _analyze_position_cycle(self) -> Dict:
        """分析位置周期性"""
        results = {}
        
        # 分析首位号码的周期
        first_nums = []
        for d in self.history[-100:]:
            nums = sorted([int(n) for n in d['basic_numbers']])
            first_nums.append(nums[0])
        
        # 分析末位号码的周期
        last_nums = []
        for d in self.history[-100:]:
            nums = sorted([int(n) for n in d['basic_numbers']])
            last_nums.append(nums[-1])
        
        results['first_cycle'] = self._find_cycle(first_nums)
        results['last_cycle'] = self._find_cycle(last_nums)
        
        return results
    
    def _find_cycle(self, nums: List[int]) -> Dict:
        """找出号码的周期性"""
        if len(nums) < 5:
            return {'cycle': None, 'pattern': nums}
        
        # 简化：返回最近出现的模式
        return {'cycle': None, 'pattern': nums[-10:]}
    
    def predict_with_periodicity(self) -> Dict:
        """基于周期性预测"""
        predictions = {
            'weekday_hot': [],  # 按星期预测的热号
            'cycle_numbers': [],  # 周期性号码
            'alternating': {},   # 交替规律
            'position_hints': {}, # 位置提示
        }
        
        # 1. 根据星期规律推荐
        current_weekday = len(self.history) % 7
        weekday_analysis = self._analyze_weekday()
        if f'weekday_{current_weekday}' in weekday_analysis:
            predictions['weekday_hot'] = weekday_analysis[f'weekday_{current_weekday}']
        
        # 2. 推荐即将回补的周期性号码
        cycle_analysis = self._analyze_cycle()
        for num in range(1, 31):
            if f'num_{num}' in cycle_analysis:
                data = cycle_analysis[f'num_{num}']
                if data['next_expected'] is not None and data['next_expected'] <= 3:
                    predictions['cycle_numbers'].append(num)
        
        return predictions


def main():
    """测试"""
    history = [
        {'period': '2026001', 'basic_numbers': ['01', '05', '09', '12', '15', '18', '22']},
        {'period': '2026002', 'basic_numbers': ['02', '06', '10', '13', '16', '19', '23']},
        {'period': '2026003', 'basic_numbers': ['03', '07', '11', '14', '17', '20', '24']},
    ]
    
    analyzer = PeriodicAnalyzer(history)
    results = analyzer.analyze()
    
    print("=== 周期性分析结果 ===")
    print(f"星期规律: {results.get('weekday', {})}")
    print(f"周期性号码: {results.get('cycle', {})}")
    
    predictions = analyzer.predict_with_periodicity()
    print(f"\n=== 预测建议 ===")
    print(f"星期热号: {predictions['weekday_hot']}")
    print(f"周期回补: {predictions['cycle_numbers']}")


if __name__ == '__main__':
    main()
