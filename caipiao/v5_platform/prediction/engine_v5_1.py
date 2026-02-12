#!/usr/bin/env python3
"""七乐彩预测引擎 V5.1 - 优化版"""

import json
import random
from typing import List, Dict, Tuple
from collections import Counter

from feature_layer.frequency_features import FrequencyFeatures
from feature_layer.missing_features import MissingFeatures
from feature_layer.advanced_features import AdvancedFeatures


class PredictionEngineV5_1:
    """预测引擎 V5.1 - 优化版"""
    
    def __init__(self, history_file: str = '/home/lang/.openclaw/workspace/caipiao/qlc_history_full.json'):
        self.history = []
        self.history_file = history_file
        self.features = {}
        self.weights = {
            'hot': 0.30,      # 热号权重（降低）
            'missing': 0.40,  # 遗漏权重（提高）
            'random': 0.15,   # 随机权重（降低）
            'feature': 0.15,   # 新增：特征推荐
        }
        
        # 加载数据
        self.load_history()
        
        # 分析数据
        if self.history:
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
        """全面分析数据"""
        print("🔍 正在分析数据...")
        
        # 提取特征
        freq_feat = FrequencyFeatures(self.history, windows=[10, 20, 30])
        miss_feat = MissingFeatures(self.history)
        adv_feat = AdvancedFeatures(self.history, windows=[10, 20, 30])
        
        self.features = {
            **freq_feat.extract(),
            **miss_feat.extract(),
            **adv_feat.extract(),
        }
        
        print(f"✅ 提取了 {len(self.features)} 个特征")
        
        # 提取策略所需数据
        self._analyze_hot_cold()
        self._analyze_missing()
        self._analyze_patterns()
    
    def _analyze_hot_cold(self):
        """分析冷热号（扩大窗口）"""
        recent = self.history[-30:]  # 扩大到30期
        all_numbers = []
        for d in recent:
            all_numbers.extend([int(n) for n in d['basic_numbers']])
        
        freq = Counter(all_numbers)
        
        # 热号TOP10
        self.hot_numbers = [n for n, _ in freq.most_common(10)]
        
        # 冷号
        all_set = set(range(1, 31))
        recent_set = set(all_numbers)
        self.cold_numbers = sorted(all_set - recent_set, key=lambda x: freq.get(x, 0))
        
        # 温号（出现1-2次的）
        self.warm_numbers = [n for n, c in freq.items() if 1 <= c <= 2]
        
        print(f"  热号: {self.hot_numbers[:5]}...")
        print(f"  冷号: {self.cold_numbers[:5]}...")
    
    def _analyze_missing(self):
        """分析遗漏值"""
        # 使用更大的窗口计算遗漏
        all_missing = []
        for num in range(1, 31):
            missing = 0
            for d in reversed(self.history[-50:]):  # 50期窗口
                if num in [int(n) for n in d['basic_numbers']]:
                    break
                missing += 1
            all_missing.append((num, missing))
        
        # 高遗漏号码（回补潜力大）
        self.high_missing = sorted(all_missing, key=lambda x: x[1], reverse=True)[:10]
        
        # 中等遗漏（平衡选择）
        self.medium_missing = sorted(all_missing, key=lambda x: x[1])[10:20]
        
        # 低遗漏（可能过热）
        self.low_missing = [n for n, m in all_missing if m <= 2]
        
        self.missing_dict = dict(all_missing)
    
    def _analyze_patterns(self):
        """分析模式特征"""
        recent = self.history[-30:]
        
        # 和值趋势
        sums = [sum(int(n) for n in d['basic_numbers']) for d in recent]
        self.sum_trend = 'up' if sums[-1] > sums[0] else 'down' if sums[-1] < sums[0] else 'stable'
        
        # 奇偶趋势
        odds = [sum(1 for n in d['basic_numbers'] if int(n) % 2 == 1) for d in recent]
        self.odd_trend = 'up' if sum(odds[-3:]) > sum(odds[:3]) else 'down'
        
        # 大小趋势
        larges = [sum(1 for n in d['basic_numbers'] if int(n) >= 21) for d in recent]
        self.large_trend = 'up' if sum(larges[-3:]) > sum(larges[:3]) else 'down'
    
    def get_strategy_pool(self) -> Dict[str, List[int]]:
        """获取各策略的号码池"""
        return {
            'hot': self.hot_numbers,
            'missing': [n for n, _ in self.high_missing],
            'random': list(range(1, 31)),
            'feature_recommend': self._feature_based_selection(),
        }
    
    def _feature_based_selection(self) -> List[int]:
        """基于特征推荐号码"""
        candidates = []
        
        # 1. 优先选择中等遗漏号码（遗漏值3-6）
        for n, m in self.high_missing[:10]:
            if 3 <= m <= 6:
                candidates.append(n)
        
        # 2. 补充热号（选择非最高频的）
        for n in self.hot_numbers[5:10]:
            if n not in candidates:
                candidates.append(n)
        
        # 3. 确保分布均衡
        if len(candidates) < 10:
            candidates.extend(list(range(1, 31)))
        
        return list(set(candidates))[:15]
    
    def check_constraints(self, numbers: List[int]) -> Tuple[bool, str]:
        """增强的约束检查"""
        # 奇偶分布（2-5个奇数）
        odd_count = sum(1 for n in numbers if n % 2 == 1)
        if not (2 <= odd_count <= 5):
            return False, f"奇偶分布不均（奇数:{odd_count}）"
        
        # 大小分布
        small = sum(1 for n in numbers if n <= 10)
        medium = sum(1 for n in numbers if 11 <= n <= 20)
        large = sum(1 for n in numbers if n >= 21)
        
        if not (1 <= small <= 4 and 1 <= medium <= 4 and 1 <= large <= 4):
            return False, f"大小分布不均（{small}-{medium}-{large}）"
        
        # 和值范围（理论范围28-189，正常范围70-140）
        total = sum(numbers)
        if not (60 <= total <= 170):
            return False, f"和值异常（{total}）"
        
        # 跨度（最大-最小）
        span = max(numbers) - min(numbers)
        if not (15 <= span <= 27):
            return False, f"跨度异常（{span}）"
        
        # AC值
        nums = sorted(numbers)
        diffs = set()
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                diffs.add(nums[j] - nums[i])
        ac = len(diffs) - 6
        if not (8 <= ac <= 15):
            return False, f"AC值异常（{ac}）"
        
        # 连号限制（最多2组）
        consecutive = 0
        for i in range(len(nums) - 1):
            if nums[i + 1] == nums[i] + 1:
                consecutive += 1
        if consecutive > 2:
            return False, f"连号过多（{consecutive}组）"
        
        return True, "OK"
    
    def generate_predictions(self, count: int = 100) -> List[List[int]]:
        """生成预测"""
        if not self.history:
            print("❌ 没有历史数据")
            return []
        
        print("🎲 正在生成预测...")
        
        predictions = []
        attempts = 0
        max_attempts = 200000
        
        # 各策略的号码池
        pools = self.get_strategy_pool()
        
        while len(predictions) < count and attempts < max_attempts:
            attempts += 1
            
            # 动态选择策略
            r = random.random()
            cumulative = 0
            selected_pool = list(range(1, 31))
            
            for name, weight in self.weights.items():
                cumulative += weight
                if r <= cumulative:
                    selected_pool = pools.get(name, list(range(1, 31)))
                    break
            
            # 确保池子足够大
            if len(selected_pool) < 15:
                selected_pool = list(range(1, 31))
            
            # 随机选择7个号码
            selected = sorted(random.sample(selected_pool, 7))
            
            # 检查约束
            valid, reason = self.check_constraints(selected)
            if not valid:
                continue
            
            # 避免重复
            if selected not in predictions:
                predictions.append(selected)
                
                # 进度显示
                if len(predictions) % 20 == 0:
                    print(f"  已生成 {len(predictions)}/{count}...")
        
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
        recent30 = self.history[-30:]
        
        # 频率统计
        all_numbers = []
        for d in recent30:
            all_numbers.extend([int(n) for n in d['basic_numbers']])
        freq = Counter(all_numbers)
        hot = freq.most_common(10)
        
        # 遗漏统计
        high_missing = sorted(self.missing_dict.items(), key=lambda x: x[1], reverse=True)[:5]
        
        report = f"""
{'='*60}
七乐彩预测分析报告 V5.1
{'='*60}

📊 数据概况
  数据量: {len(self.history)} 条
  分析窗口: 10/20/30期
  特征数: {len(self.features)}
  策略权重: 热号{self.weights['hot']:.0%}/遗漏{self.weights['missing']:.0%}/特征{self.weights['feature']:.0%}/随机{self.weights['random']:.0%}

🔥 热号TOP10（30期）
"""
        
        for i, (num, count) in enumerate(hot, 1):
            report += f"  {i:2d}. {num:02d}号: {count}次\n"
        
        report += """
📈 高遗漏号码
"""
        
        for num, gap in high_missing:
            report += f"  {num:02d}号: 已遗漏{gap}期\n"
        
        report += f"""
📐 模式分析
  和值趋势: {self.sum_trend} ({sum(int(n) for n in recent[0]['basic_numbers'])} → {sum(int(n) for n in recent[-1]['basic_numbers'])})
  奇偶趋势: {self.odd_trend}
  大小趋势: {self.large_trend}

✅ 约束条件
  奇偶分布: 2-5个奇数
  大小分布: 1-4个小/中/大
  和值范围: 60-170
  跨度范围: 15-27
  AC值范围: 8-15
  连号限制: 最多2组

---
七乐彩预测平台 V5.1
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
    print("七乐彩预测引擎 V5.1 - 优化版")
    print("=" * 60)
    
    # 创建引擎
    engine = PredictionEngineV5_1()
    
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
