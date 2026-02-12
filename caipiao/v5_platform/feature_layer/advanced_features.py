#!/usr/bin/env python3
"""高级特征提取器 - V5.1增强版"""

from collections import Counter
from typing import Dict, List, Tuple
import math


class AdvancedFeatures:
    """高级特征提取器"""
    
    def __init__(self, history: List[Dict], windows: List[int] = [10, 20, 30]):
        self.history = history
        self.windows = windows
    
    def extract(self) -> Dict:
        """提取所有特征"""
        features = {}
        
        # 1. 频率特征（多窗口）
        features.update(self._frequency_features())
        
        # 2. 遗漏特征
        features.update(self._missing_features())
        
        # 3. 和值特征
        features.update(self._sum_features())
        
        # 4. 跨度特征
        features.update(self._range_features())
        
        # 5. AC值特征
        features.update(self._ac_features())
        
        # 6. 012路特征
        features.update(self._road_features())
        
        # 7. 奇偶特征
        features.update(self._odd_even_features())
        
        # 8. 大小特征
        features.update(self._size_features())
        
        # 9. 位置特征（首位、末位）
        features.update(self._position_features())
        
        # 10. 连号特征
        features.update(self._consecutive_features())
        
        return features
    
    def _frequency_features(self) -> Dict:
        """频率特征"""
        features = {}
        for w in self.windows:
            recent = self.history[-w:]
            counts = Counter()
            for d in recent:
                counts.update([int(n) for n in d['basic_numbers']])
            
            # 平均频率
            features[f'freq_mean_{w}'] = sum(counts.values()) / 30
            
            # 高频号码TOP5
            top5 = [n for n, _ in counts.most_common(5)]
            features[f'freq_top5_{w}'] = sum(top5)
            
            # 低频号码
            low5 = [n for n, _ in counts.most_common()[-5:]]
            features[f'freq_low5_{w}'] = sum(low5)
            
            # 频率方差
            if len(counts) > 1:
                values = list(counts.values())
                mean_val = sum(values) / len(values)
                variance = sum((v - mean_val) ** 2 for v in values) / len(values)
                features[f'freq_variance_{w}'] = variance
            else:
                features[f'freq_variance_{w}'] = 0
        
        return features
    
    def _missing_features(self) -> Dict:
        """遗漏特征"""
        features = {}
        
        # 整体遗漏统计
        all_missing = []
        for num in range(1, 31):
            missing = 0
            for d in reversed(self.history):
                if num in [int(n) for n in d['basic_numbers']]:
                    break
                missing += 1
            all_missing.append(missing)
            features[f'missing_{num}'] = missing
        
        # 遗漏统计
        features['missing_max'] = max(all_missing)
        features['missing_min'] = min(all_missing)
        features['missing_mean'] = sum(all_missing) / 30
        features['missing_std'] = self._std(all_missing)
        
        # 高遗漏号码数量（遗漏>5期）
        features['missing_high_count'] = sum(1 for m in all_missing if m > 5)
        
        # 遗漏回补潜力
        features['missing_recovery_score'] = sum(all_missing) / 30
        
        return features
    
    def _sum_features(self) -> Dict:
        """和值特征"""
        features = {}
        recent = self.history[-20:]
        
        sums = []
        for d in recent:
            nums = [int(n) for n in d['basic_numbers']]
            sums.append(sum(nums))
        
        if sums:
            features['sum_mean'] = sum(sums) / len(sums)
            features['sum_min'] = min(sums)
            features['sum_max'] = max(sums)
            features['sum_std'] = self._std(sums)
            
            # 最近一期和值
            features['sum_latest'] = sums[-1]
        else:
            features['sum_mean'] = 105  # 理论平均值
            features['sum_min'] = 28
            features['sum_max'] = 189
            features['sum_std'] = 30
            features['sum_latest'] = 105
        
        return features
    
    def _range_features(self) -> Dict:
        """跨度特征（最大-最小）"""
        features = {}
        recent = self.history[-20:]
        
        ranges = []
        for d in recent:
            nums = [int(n) for n in d['basic_numbers']]
            ranges.append(max(nums) - min(nums))
        
        if ranges:
            features['range_mean'] = sum(ranges) / len(ranges)
            features['range_std'] = self._std(ranges)
            features['range_latest'] = ranges[-1]
        else:
            features['range_mean'] = 20
            features['range_std'] = 5
            features['range_latest'] = 20
        
        return features
    
    def _ac_features(self) -> Dict:
        """AC值特征（不同值数量-7）"""
        features = {}
        recent = self.history[-20:]
        
        ac_values = []
        for d in recent:
            nums = sorted([int(n) for n in d['basic_numbers']])
            diffs = set()
            for i in range(len(nums)):
                for j in range(i + 1, len(nums)):
                    diffs.add(nums[j] - nums[i])
            ac = len(diffs) - 6  # AC值计算
            ac_values.append(ac)
        
        if ac_values:
            features['ac_mean'] = sum(ac_values) / len(ac_values)
            features['ac_latest'] = ac_values[-1]
        else:
            features['ac_mean'] = 10
            features['ac_latest'] = 10
        
        return features
    
    def _road_features(self) -> Dict:
        """012路特征（除3余0/1/2）"""
        features = {}
        recent = self.history[-20:]
        
        road0_count, road1_count, road2_count = 0, 0, 0
        
        for d in recent:
            for n in d['basic_numbers']:
                r = int(n) % 3
                if r == 0:
                    road0_count += 1
                elif r == 1:
                    road1_count += 1
                else:
                    road2_count += 1
        
        total = len(recent) * 7
        features['road0_ratio'] = road0_count / total if total > 0 else 0.33
        features['road1_ratio'] = road1_count / total if total > 0 else 0.33
        features['road2_ratio'] = road2_count / total if total > 0 else 0.33
        
        return features
    
    def _odd_even_features(self) -> Dict:
        """奇偶特征"""
        features = {}
        recent = self.history[-20:]
        
        odd_counts, even_counts = [], []
        for d in recent:
            nums = [int(n) for n in d['basic_numbers']]
            odd = sum(1 for n in nums if n % 2 == 1)
            odd_counts.append(odd)
            even_counts.append(7 - odd)
        
        features['odd_mean'] = sum(odd_counts) / len(odd_counts)
        features['odd_std'] = self._std(odd_counts)
        features['odd_latest'] = odd_counts[-1]
        
        return features
    
    def _size_features(self) -> Dict:
        """大小特征（1-10小，11-20中，21-30大）"""
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
        features['size_small_latest'] = small_counts[-1]
        features['size_medium_latest'] = medium_counts[-1]
        features['size_large_latest'] = large_counts[-1]
        
        return features
    
    def _position_features(self) -> Dict:
        """位置特征（首位、末位）"""
        features = {}
        recent = self.history[-20:]
        
        first_nums, last_nums = [], []
        for d in recent:
            nums = sorted([int(n) for n in d['basic_numbers']])
            first_nums.append(nums[0])
            last_nums.append(nums[-1])
        
        features['first_mean'] = sum(first_nums) / len(first_nums)
        features['first_std'] = self._std(first_nums)
        features['first_latest'] = first_nums[-1]
        
        features['last_mean'] = sum(last_nums) / len(last_nums)
        features['last_std'] = self._std(last_nums)
        features['last_latest'] = last_nums[-1]
        
        return features
    
    def _consecutive_features(self) -> Dict:
        """连号特征"""
        features = {}
        recent = self.history[-20:]
        
        consec_counts = []
        for d in recent:
            nums = sorted([int(n) for n in d['basic_numbers']])
            count = 0
            for i in range(len(nums) - 1):
                if nums[i + 1] == nums[i] + 1:
                    count += 1
            consec_counts.append(count)
        
        features['consecutive_mean'] = sum(consec_counts) / len(consec_counts)
        features['consecutive_latest'] = consec_counts[-1]
        features['has_consecutive'] = 1 if consec_counts[-1] > 0 else 0
        
        return features
    
    def _std(self, values: List[float]) -> float:
        """计算标准差"""
        if len(values) < 2:
            return 0
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        return math.sqrt(variance)


def main():
    """测试"""
    history = [
        {'period': '2026001', 'basic_numbers': ['01', '05', '09', '12', '15', '18', '22']},
        {'period': '2026002', 'basic_numbers': ['02', '06', '10', '13', '16', '19', '23']},
        {'period': '2026003', 'basic_numbers': ['03', '07', '11', '14', '17', '20', '24']},
    ]
    
    f = AdvancedFeatures(history).extract()
    print(f"✅ 提取了 {len(f)} 个特征")
    print(f"  和值: {f.get('sum_latest', 'N/A')}")
    print(f"  跨度: {f.get('range_latest', 'N/A')}")
    print(f"  AC值: {f.get('ac_latest', 'N/A')}")
    print(f"  奇偶比: {f.get('odd_mean', 'N/A'):.2f}")
    
    return len(f) > 20


if __name__ == '__main__':
    success = main()
    print("✅ 高级特征测试通过" if success else "❌ 测试失败")
    exit(0 if success else 1)
