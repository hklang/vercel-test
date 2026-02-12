#!/usr/bin/env python3
"""
新增特征提取器 - 方法6-13的特征
包含：和值、AC值、012路、极距等
"""

from typing import Dict, List, Tuple
from collections import Counter
import math


class NewFeatures:
    """方法6-13的特征提取器"""
    
    def __init__(self, history: List[Dict], windows: List[int] = [10, 20, 30]):
        self.history = history
        self.windows = windows
    
    def extract_all(self) -> Dict[str, float]:
        """提取所有新特征"""
        features = {}
        
        # 方法6: 和值特征
        features.update(self._sum_features())
        
        # 方法7: 三区比特征
        features.update(self._size_ratio_features())
        
        # 方法8: 012路特征
        features.update(self._road_features())
        
        # 方法9: 连号特征
        features.update(self._consecutive_features())
        
        # 方法10: 同尾特征
        features.update(self._tail_features())
        
        # 方法11: 重号特征
        features.update(self._repeat_features())
        
        # 方法12: AC值特征
        features.update(self._ac_features())
        
        # 方法13: 极距特征
        features.update(self._range_features())
        
        return features
    
    def _sum_features(self) -> Dict:
        """和值特征（方法6）"""
        features = {}
        recent = self.history[-20:]
        
        sums = [sum(int(n) for n in d['basic_numbers']) for d in recent]
        
        if sums:
            features['sum_mean'] = sum(sums) / len(sums)
            features['sum_min'] = min(sums)
            features['sum_max'] = max(sums)
            features['sum_std'] = self._std(sums)
            features['sum_latest'] = sums[-1]
            
            # 和值趋势
            if len(sums) >= 5:
                recent_avg = sum(sums[-5:]) / 5
                older_avg = sum(sums[:-5]) / 5 if len(sums) > 5 else sums[0]
                features['sum_trend'] = 1 if recent_avg > older_avg else 0
            else:
                features['sum_trend'] = 0
        
        return features
    
    def _size_ratio_features(self) -> Dict:
        """三区比特征（方法7）"""
        features = {}
        recent = self.history[-20:]
        
        small_counts, medium_counts, large_counts = [], [], []
        
        for d in recent:
            nums = [int(n) for n in d['basic_numbers']]
            small = sum(1 for n in nums if n <= 10)
            medium = sum(1 for n in nums if 11 <= n <= 20)
            large = sum(1 for n in nums if n >= 21)
            small_counts.append(small)
            medium_counts.append(medium)
            large_counts.append(large)
        
        features['size_small_mean'] = sum(small_counts) / len(small_counts)
        features['size_medium_mean'] = sum(medium_counts) / len(medium_counts)
        features['size_large_mean'] = sum(large_counts) / len(large_counts)
        
        # 三区分布趋势
        features['size_small_latest'] = small_counts[-1]
        features['size_medium_latest'] = medium_counts[-1]
        features['size_large_latest'] = large_counts[-1]
        
        return features
    
    def _road_features(self) -> Dict:
        """012路特征（方法8）"""
        features = {}
        recent = self.history[-20:]
        
        road0_count, road1_count, road2_count = 0, 0, 0
        road0_list, road1_list, road2_list = [], [], []
        
        for d in recent:
            road0, road1, road2 = 0, 0, 0
            for n in d['basic_numbers']:
                r = int(n) % 3
                if r == 0:
                    road0 += 1
                    road0_list.append(1)
                elif r == 1:
                    road1 += 1
                    road1_list.append(1)
                else:
                    road2 += 1
                    road2_list.append(1)
            road0_count += road0
            road1_count += road1
            road2_count += road2
        
        total = len(recent) * 7
        features['road0_ratio'] = road0_count / total if total > 0 else 0.33
        features['road1_ratio'] = road1_count / total if total > 0 else 0.33
        features['road2_ratio'] = road2_count / total if total > 0 else 0.33
        
        features['road0_mean'] = road0_count / len(recent) if recent else 2.33
        features['road1_mean'] = road1_count / len(recent) if recent else 2.33
        features['road2_mean'] = road2_count / len(recent) if recent else 2.33
        
        return features
    
    def _consecutive_features(self) -> Dict:
        """连号特征（方法9）"""
        features = {}
        recent = self.history[-20:]
        
        consec_counts = []
        for d in recent:
            nums = sorted([int(n) for n in d['basic_numbers']])
            count = sum(1 for i in range(len(nums) - 1) if nums[i+1] == nums[i] + 1)
            consec_counts.append(count)
        
        features['consecutive_mean'] = sum(consec_counts) / len(consec_counts) if consec_counts else 0
        features['consecutive_latest'] = consec_counts[-1] if consec_counts else 0
        features['has_consecutive'] = 1 if consec_counts and consec_counts[-1] > 0 else 0
        features['consecutive_max'] = max(consec_counts) if consec_counts else 0
        
        return features
    
    def _tail_features(self) -> Dict:
        """同尾特征（方法10）"""
        features = {}
        recent = self.history[-20:]
        
        tail_counts = []
        for d in recent:
            tails = [int(n) % 10 for n in d['basic_numbers']]
            tail_counter = Counter(tails)
            # 同尾号数量
            count = sum(1 for c in tail_counter.values() if c >= 2)
            tail_counts.append(count)
        
        features['tail_mean'] = sum(tail_counts) / len(tail_counts) if tail_counts else 0
        features['tail_latest'] = tail_counts[-1] if tail_counts else 0
        features['has_tail'] = 1 if tail_counts and tail_counts[-1] > 0 else 0
        
        # 最常见尾数
        all_tails = []
        for d in recent:
            all_tails.extend([int(n) % 10 for n in d['basic_numbers']])
        tail_freq = Counter(all_tails)
        features['most_common_tail'] = tail_freq.most_common(1)[0][0] if tail_freq else 0
        
        return features
    
    def _repeat_features(self) -> Dict:
        """重号特征（方法11）"""
        features = {}
        
        if len(self.history) < 2:
            features['repeat_mean'] = 0
            features['repeat_latest'] = 0
            return features
        
        recent = self.history[-21:]  # 多取一期用于比较
        
        repeat_counts = []
        for i in range(1, len(recent)):
            current = set(int(n) for n in recent[i]['basic_numbers'])
            previous = set(int(n) for n in recent[i-1]['basic_numbers'])
            repeat = len(current & previous)
            repeat_counts.append(repeat)
        
        features['repeat_mean'] = sum(repeat_counts) / len(repeat_counts) if repeat_counts else 0
        features['repeat_latest'] = repeat_counts[-1] if repeat_counts else 0
        features['repeat_max'] = max(repeat_counts) if repeat_counts else 0
        
        return features
    
    def _ac_features(self) -> Dict:
        """AC值特征（方法12）"""
        features = {}
        recent = self.history[-20:]
        
        ac_values = []
        for d in recent:
            nums = sorted([int(n) for n in d['basic_numbers']])
            diffs = {nums[j] - nums[i] for i in range(len(nums)) for j in range(i+1, len(nums))}
            ac = len(diffs) - 6
            ac_values.append(max(0, ac))
        
        if ac_values:
            features['ac_mean'] = sum(ac_values) / len(ac_values)
            features['ac_latest'] = ac_values[-1]
            features['ac_std'] = self._std(ac_values)
        else:
            features['ac_mean'] = 10
            features['ac_latest'] = 10
            features['ac_std'] = 0
        
        return features
    
    def _range_features(self) -> Dict:
        """极距特征（方法13）"""
        features = {}
        recent = self.history[-20:]
        
        ranges = []
        for d in recent:
            nums = [int(n) for n in d['basic_numbers']]
            ranges.append(max(nums) - min(nums))
        
        if ranges:
            features['range_mean'] = sum(ranges) / len(ranges)
            features['range_latest'] = ranges[-1]
            features['range_std'] = self._std(ranges)
            features['range_min'] = min(ranges)
            features['range_max'] = max(ranges)
        else:
            features['range_mean'] = 20
            features['range_latest'] = 20
            features['range_std'] = 0
            features['range_min'] = 15
            features['range_max'] = 27
        
        return features
    
    def _std(self, values: List[float]) -> float:
        """计算标准差"""
        if len(values) < 2:
            return 0
        mean = sum(values) / len(values)
        return math.sqrt(sum((v - mean) ** 2 for v in values) / len(values))


def check_constraints(numbers: List[int]) -> Tuple[bool, str]:
    """检查约束条件（方法6-13的约束）"""
    nums = sorted(numbers)
    
    # 和值范围（60-170）
    total = sum(numbers)
    if not (60 <= total <= 170):
        return False, f"和值异常（{total}）"
    
    # AC值范围（8-15）
    diffs = {nums[j] - nums[i] for i in range(len(nums)) for j in range(i+1, len(nums))}
    ac = len(diffs) - 6
    if not (8 <= ac <= 15):
        return False, f"AC值异常（{ac}）"
    
    # 极距范围（15-27）
    range_val = max(nums) - min(nums)
    if not (15 <= range_val <= 27):
        return False, f"极距异常（{range_val}）"
    
    # 连号限制（最多2组）
    consecutive = sum(1 for i in range(len(nums) - 1) if nums[i+1] == nums[i] + 1)
    if consecutive > 2:
        return False, f"连号过多（{consecutive}组）"
    
    # 同尾号限制（最多2组）
    tails = [n % 10 for n in numbers]
    tail_counter = Counter(tails)
    if sum(1 for c in tail_counter.values() if c >= 2) > 2:
        return False, "同尾号过多"
    
    # 012路分布（每路1-4个）
    road0 = sum(1 for n in numbers if n % 3 == 0)
    road1 = sum(1 for n in numbers if n % 3 == 1)
    road2 = sum(1 for n in numbers if n % 3 == 2)
    if not (1 <= road0 <= 4 and 1 <= road1 <= 4 and 1 <= road2 <= 4):
        return False, f"012路分布异常（{road0}-{road1}-{road2}）"
    
    return True, "OK"


def main():
    """测试"""
    history = [
        {'period': '2026001', 'basic_numbers': ['01', '05', '09', '12', '15', '18', '22']},
        {'period': '2026002', 'basic_numbers': ['02', '06', '10', '13', '16', '19', '23']},
        {'period': '2026003', 'basic_numbers': ['03', '07', '11', '14', '17', '20', '24']},
    ]
    
    f = NewFeatures(history).extract_all()
    print(f"✅ 提取了 {len(f)} 个新特征")
    print(f"  和值: {f.get('sum_latest', 'N/A')}")
    print(f"  AC值: {f.get('ac_latest', 'N/A')}")
    print(f"  极距: {f.get('range_latest', 'N/A')}")
    print(f"  连号: {f.get('consecutive_latest', 'N/A')}")
    print(f"  012路: {f.get('road0_ratio', 'N/A'):.2f}-{f.get('road1_ratio', 'N/A'):.2f}-{f.get('road2_ratio', 'N/A'):.2f}")
    
    # 测试约束
    test_nums = [1, 5, 9, 12, 15, 18, 22]
    valid, msg = check_constraints(test_nums)
    print(f"\n约束测试: {msg}")
    
    return len(f) > 20


if __name__ == '__main__':
    success = main()
    print("✅ 测试通过" if success else "❌ 测试失败")
    exit(0 if success else 1)
