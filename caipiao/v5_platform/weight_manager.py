#!/usr/bin/env python3
"""
动态权重管理器 - V7.0步骤2
根据近期表现自动调整各策略权重
"""

import json
import os
from typing import Dict, List, Tuple
from datetime import datetime
from pathlib import Path


class DynamicWeightManager:
    """动态权重管理器"""
    
    def __init__(self, config):
        self.config = config
        self.weights_file = config.WEIGHTS_FILE
        self.history_file = config.WEIGHTS_HISTORY_FILE
        
        # 默认权重
        self.weights = {
            'hot': 0.20,       # 热号策略
            'missing': 0.30,   # 遗漏策略
            'feature': 0.20,   # 特征策略
            'random': 0.15,    # 随机策略
            'ml': 0.15,        # ML策略
        }
        
        # 权重历史记录
        self.history = []
        
        # 加载历史
        self.load()
    
    def load(self):
        """加载权重"""
        # 加载当前权重
        if os.path.exists(self.weights_file):
            try:
                with open(self.weights_file, 'r') as f:
                    data = json.load(f)
                    self.weights = data.get('weights', self.weights)
            except:
                pass
        
        # 加载历史
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
            except:
                self.history = []
    
    def save(self):
        """保存权重"""
        # 保存当前权重
        Path(self.weights_file).parent.mkdir(parents=True, exist_ok=True)
        with open(self.weights_file, 'w') as f:
            json.dump({
                'weights': self.weights,
                'updated': datetime.now().isoformat()
            }, f, indent=2)
        
        # 保存历史
        with open(self.history_file, 'w') as f:
            json.dump(self.history[-100:], f, indent=2)  # 只保留最近100条
    
    def get_weights(self) -> Dict[str, float]:
        """获取当前权重"""
        return self.weights.copy()
    
    def update_weights(self, recent_results: List[Dict]):
        """根据近期结果更新权重
        
        Args:
            recent_results: 近期预测结果列表
                [{
                    'strategy': 'hot',  # 使用的策略
                    'hit_rate': 0.25,   # 命中率
                    'timestamp': '2026-02-12T10:00:00'
                }, ...]
        """
        if len(recent_results) < 5:
            return  # 数据不足，不更新
        
        # 统计各策略表现
        strategy_scores = {}
        strategy_counts = {}
        
        for result in recent_results:
            strategy = result.get('strategy', 'random')
            hit_rate = result.get('hit_rate', 0)
            
            if strategy not in strategy_scores:
                strategy_scores[strategy] = 0
                strategy_counts[strategy] = 0
            
            strategy_scores[strategy] += hit_rate
            strategy_counts[strategy] += 1
        
        # 计算平均表现
        strategy_performance = {}
        for s in self.weights.keys():
            if s in strategy_counts and strategy_counts[s] > 0:
                strategy_performance[s] = strategy_scores[s] / strategy_counts[s]
            else:
                strategy_performance[s] = 0.5  # 默认50%
        
        # 计算新权重
        total_performance = sum(strategy_performance.values()) or 1
        
        new_weights = {}
        for s in self.weights.keys():
            # 基于表现的权重调整
            base_weight = self.weights[s]
            performance_ratio = strategy_performance[s] / total_performance
            target_weight = 0.3 + performance_ratio * 0.4  # 目标权重30%-70%
            
            # 逐步调整（避免突变）
            new_weights[s] = base_weight * 0.7 + target_weight * 0.3
        
        # 归一化
        total = sum(new_weights.values()) or 1
        self.weights = {k: v/total for k, v in new_weights.items()}
        
        # 记录
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'performance': strategy_performance,
            'weights': self.weights.copy(),
            'results_count': len(recent_results),
        })
        
        # 保存
        self.save()
        
        return self.weights
    
    def get_weights_report(self) -> str:
        """生成权重报告"""
        report = f"""
=== 动态权重报告 ===

更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

当前权重:
"""
        for s, w in sorted(self.weights.items()):
            bar = '█' * int(w * 20)
            report += f"  {s:10s}: {w:.1%} {bar}\n"
        
        if self.history:
            last = self.history[-1]
            report += f"\n历史记录: {len(self.history)} 条\n"
            report += f"最近更新: {last['timestamp']}\n"
        
        return report


class WeightValidator:
    """权重验证器"""
    
    def __init__(self, weight_manager: DynamicWeightManager):
        self.wm = weight_manager
        self.validation_results = []
    
    def validate_prediction(self, strategy: str, prediction: List[int], actual: List[int]) -> Dict:
        """验证单次预测"""
        if not actual:
            return {'valid': False, 'reason': '无实际开奖数据'}
        
        hit_count = len(set(prediction) & set(actual))
        hit_rate = hit_count / 7
        
        return {
            'timestamp': datetime.now().isoformat(),
            'strategy': strategy,
            'predicted': prediction,
            'actual': actual,
            'hit_count': hit_count,
            'hit_rate': hit_rate,
        }
    
    def run_validation(self, history: List[Dict], predictor) -> Dict:
        """运行完整验证"""
        if len(history) < 50:
            return {'valid': False, 'reason': '历史数据不足'}
        
        # 用前N期预测后M期
        train_end = len(history) - 20
        train_data = history[:train_end]
        test_data = history[train_end:]
        
        results = []
        for actual_data in test_data[:20]:
            predictions = predictor.predict(5, train_data)
            actual = [int(n) for n in actual_data['basic_numbers']]
            
            result = self.validate_prediction('ensemble', predictions[0], actual)
            results.append(result)
        
        avg_hit_rate = sum(r['hit_rate'] for r in results) / len(results)
        
        # 更新权重
        self.wm.update_weights(results)
        
        return {
            'valid': True,
            'test_count': len(results),
            'avg_hit_rate': avg_hit_rate,
            'weights': self.wm.get_weights(),
        }


def main():
    """测试"""
    class Config:
        WEIGHTS_FILE = '/tmp/test_weights.json'
        WEIGHTS_HISTORY_FILE = '/tmp/test_weights_history.json'
    
    wm = DynamicWeightManager(Config())
    
    print("=== 动态权重管理器测试 ===\n")
    
    # 显示当前权重
    print("当前权重:")
    for s, w in wm.get_weights().items():
        print(f"  {s}: {w:.1%}")
    
    # 模拟更新
    print("\n模拟更新权重...")
    test_results = [
        {'strategy': 'hot', 'hit_rate': 0.25, 'timestamp': '2026-02-12T10:00:00'},
        {'strategy': 'missing', 'hit_rate': 0.35, 'timestamp': '2026-02-12T10:01:00'},
        {'strategy': 'feature', 'hit_rate': 0.28, 'timestamp': '2026-02-12T10:02:00'},
        {'strategy': 'random', 'hit_rate': 0.15, 'timestamp': '2026-02-12T10:03:00'},
        {'strategy': 'ml', 'hit_rate': 0.30, 'timestamp': '2026-02-12T10:04:00'},
    ]
    
    wm.update_weights(test_results)
    
    print("\n更新后权重:")
    for s, w in wm.get_weights().items():
        print(f"  {s}: {w:.1%}")
    
    # 报告
    print(wm.get_weights_report())
    
    # 清理
    import os
    os.remove(Config.WEIGHTS_FILE) if os.path.exists(Config.WEIGHTS_FILE) else None
    os.remove(Config.WEIGHTS_HISTORY_FILE) if os.path.exists(Config.WEIGHTS_HISTORY_FILE) else None


if __name__ == '__main__':
    main()
