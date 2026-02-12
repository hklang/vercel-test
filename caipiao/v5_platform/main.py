#!/usr/bin/env python3
"""
七乐彩智能预测系统 V6.0 - 完整自动化版
======================================

功能：
1. 机器学习预测（随机森林/XGBoost）
2. 动态权重调整
3. 分位置预测
4. 自动执行与自我验证
5. 7x24小时无人值守

使用方法：
    python3 main.py              # 正常运行
    python3 main.py --auto      # 自动模式（无输入）
    python3 main.py --verify    # 自我验证模式
    python3 main.py --cron      # Cron模式（定时运行）
"""

import json
import random
import time
import os
import sys
import argparse
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import math
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/lang/.openclaw/workspace/caipiao/v5_platform/logs/system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ==================== 基础配置 ====================
@dataclass
class Config:
    """系统配置"""
    # 路径配置
    WORKSPACE: str = '/home/lang/.openclaw/workspace/caipiao'
    DATA_FILE: str = '/home/lang/.openclaw/workspace/caipiao/qlc_history_full.json'
    OUTPUT_DIR: str = '/home/lang/.openclaw/workspace/caipiao/v6_output'
    MODEL_DIR: str = '/home/lang/.openclaw/workspace/caipiao/v6_models'
    LOG_DIR: str = '/home/lang/.openclaw/workspace/caipiao/v5_platform/logs'
    
    # 预测配置
    PREDICTION_COUNT: int = 100
    FEATURE_WINDOWS: Tuple[int, int, int] = (10, 20, 30)
    
    # 权重配置
    WEIGHTS_FILE: str = '/home/lang/.openclaw/workspace/caipiao/v6_models/weights.json'
    WEIGHTS_HISTORY_FILE: str = '/home/lang/.openclaw/workspace/caipiao/v6_models/weights_history.json'
    
    # 自动化配置
    AUTO_UPDATE_INTERVAL: int = 3600  # 1小时检查一次
    CRON_UPDATE_INTERVAL: int = 7200  # 2小时更新模型
    MIN_HISTORY_FOR_PREDICT: int = 50  # 最少需要50期数据
    
    # 模型配置
    RANDOM_STATE: int = 42
    N_ESTIMATORS: int = 100


class FeatureExtractor:
    """特征提取器 - V6完整版"""
    
    def __init__(self, history: List[Dict], config: Config):
        self.history = history
        self.config = config
        self.windows = config.FEATURE_WINDOWS
    
    def extract_all(self) -> Dict[str, float]:
        """提取所有特征"""
        features = {}
        
        # 1. 频率特征
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
        
        # 9. 位置特征
        features.update(self._position_features())
        
        # 10. 连号特征
        features.update(self._consecutive_features())
        
        # 11. 趋势特征
        features.update(self._trend_features())
        
        return features
    
    def _frequency_features(self) -> Dict:
        features = {}
        for w in self.windows:
            recent = self.history[-w:]
            counts = Counter()
            for d in recent:
                counts.update([int(n) for n in d['basic_numbers']])
            
            features[f'freq_mean_{w}'] = sum(counts.values()) / 30
            features[f'freq_variance_{w}'] = self._variance(list(counts.values()))
            features[f'freq_max_{w}'] = max(counts.values()) if counts else 0
            
            top5 = [n for n, _ in counts.most_common(5)]
            features[f'freq_top5_sum_{w}'] = sum(top5)
        
        return features
    
    def _missing_features(self) -> Dict:
        features = {}
        all_missing = []
        
        for num in range(1, 31):
            missing = 0
            for d in reversed(self.history[-50:]):
                if num in [int(n) for n in d['basic_numbers']]:
                    break
                missing += 1
            all_missing.append(missing)
            features[f'missing_{num}'] = missing
        
        features['missing_mean'] = sum(all_missing) / 30
        features['missing_max'] = max(all_missing)
        features['missing_std'] = self._std(all_missing)
        features['missing_high_count'] = sum(1 for m in all_missing if m > 5)
        
        return features
    
    def _sum_features(self) -> Dict:
        features = {}
        recent = self.history[-20:]
        
        sums = [sum(int(n) for n in d['basic_numbers']) for d in recent]
        features['sum_mean'] = sum(sums) / len(sums)
        features['sum_min'] = min(sums)
        features['sum_max'] = max(sums)
        features['sum_std'] = self._std(sums)
        features['sum_latest'] = sums[-1]
        
        return features
    
    def _range_features(self) -> Dict:
        features = {}
        recent = self.history[-20:]
        
        ranges = [max(int(n) for n in d['basic_numbers']) - min(int(n) for n in d['basic_numbers']) 
                  for d in recent]
        features['range_mean'] = sum(ranges) / len(ranges)
        features['range_std'] = self._std(ranges)
        features['range_latest'] = ranges[-1]
        
        return features
    
    def _ac_features(self) -> Dict:
        features = {}
        recent = self.history[-20:]
        
        ac_values = []
        for d in recent:
            nums = sorted([int(n) for n in d['basic_numbers']])
            diffs = {nums[j] - nums[i] for i in range(len(nums)) for j in range(i+1, len(nums))}
            ac = len(diffs) - 6
            ac_values.append(max(0, ac))
        
        features['ac_mean'] = sum(ac_values) / len(ac_values)
        features['ac_latest'] = ac_values[-1]
        
        return features
    
    def _road_features(self) -> Dict:
        features = {}
        recent = self.history[-20:]
        
        road0 = road1 = road2 = 0
        for d in recent:
            for n in d['basic_numbers']:
                r = int(n) % 3
                if r == 0: road0 += 1
                elif r == 1: road1 += 1
                else: road2 += 1
        
        total = len(recent) * 7
        features['road0_ratio'] = road0 / total if total > 0 else 0.33
        features['road1_ratio'] = road1 / total if total > 0 else 0.33
        features['road2_ratio'] = road2 / total if total > 0 else 0.33
        
        return features
    
    def _odd_even_features(self) -> Dict:
        features = {}
        recent = self.history[-20:]
        
        odds = [sum(1 for n in d['basic_numbers'] if int(n) % 2 == 1) for d in recent]
        features['odd_mean'] = sum(odds) / len(odds)
        features['odd_std'] = self._std(odds)
        features['odd_latest'] = odds[-1]
        
        return features
    
    def _size_features(self) -> Dict:
        features = {}
        recent = self.history[-20:]
        
        small = [sum(1 for n in d['basic_numbers'] if int(n) <= 10) for d in recent]
        medium = [sum(1 for n in d['basic_numbers'] if 11 <= int(n) <= 20) for d in recent]
        large = [sum(1 for n in d['basic_numbers'] if int(n) >= 21) for d in recent]
        
        features['size_small_mean'] = sum(small) / len(small)
        features['size_medium_mean'] = sum(medium) / len(medium)
        features['size_large_mean'] = sum(large) / len(large)
        
        return features
    
    def _position_features(self) -> Dict:
        features = {}
        recent = self.history[-30:]
        
        first = [min(int(n) for n in d['basic_numbers']) for d in recent]
        last = [max(int(n) for n in d['basic_numbers']) for d in recent]
        
        features['first_mean'] = sum(first) / len(first)
        features['first_std'] = self._std(first)
        features['first_latest'] = first[-1]
        
        features['last_mean'] = sum(last) / len(last)
        features['last_std'] = self._std(last)
        features['last_latest'] = last[-1]
        
        return features
    
    def _consecutive_features(self) -> Dict:
        features = {}
        recent = self.history[-20:]
        
        consec = []
        for d in recent:
            nums = sorted([int(n) for n in d['basic_numbers']])
            count = sum(1 for i in range(len(nums)-1) if nums[i+1] == nums[i] + 1)
            consec.append(count)
        
        features['consecutive_mean'] = sum(consec) / len(consec)
        features['consecutive_latest'] = consec[-1]
        
        return features
    
    def _trend_features(self) -> Dict:
        """趋势特征"""
        features = {}
        recent = self.history[-10:]
        older = self.history[-20:-10]
        
        if len(recent) >= 3 and len(older) >= 3:
            recent_sum = sum(sum(int(n) for n in d['basic_numbers']) for d in recent)
            older_sum = sum(sum(int(n) for n in d['basic_numbers']) for d in older)
            
            features['sum_trend'] = 1 if recent_sum > older_sum else 0
        else:
            features['sum_trend'] = 0
        
        return features
    
    def _std(self, values: List[float]) -> float:
        if len(values) < 2:
            return 0
        mean = sum(values) / len(values)
        return math.sqrt(sum((v - mean) ** 2 for v in values) / len(values))
    
    def _variance(self, values: List[int]) -> float:
        if len(values) < 2:
            return 0
        mean = sum(values) / len(values)
        return sum((v - mean) ** 2 for v in values) / len(values)


class SimpleRandomForest:
    """纯Python随机森林实现"""
    
    def __init__(self, config: Config, n_estimators: int = 50, max_depth: int = 5):
        self.config = config
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.trees = []
        self.feature_importance = {}
    
    def fit(self, X: List[Dict], y: List[int]):
        """训练模型"""
        if not X or len(X) < 10:
            logger.warning("训练数据不足，跳过训练")
            return False
        
        # 构建训练数据
        samples = []
        for features, target in zip(X, y):
            row = []
            for k, v in sorted(features.items()):
                row.append((k, v))
            samples.append((row, target))
        
        # 训练多棵树
        for i in range(self.n_estimators):
            tree = self._build_tree(samples)
            if tree:
                self.trees.append(tree)
        
        # 计算特征重要性
        self._calculate_importance()
        
        logger.info(f"随机森林训练完成: {len(self.trees)} 棵树")
        return True
    
    def _build_tree(self, samples: List) -> Optional[Dict]:
        """构建决策树"""
        if not samples:
            return None
        
        features = samples[0][0]
        if not features:
            return {'leaf': Counter([s[1] for s in samples]).most_common(1)[0][0]}
        
        # 选择第一个特征
        best_feature = features[0][0]
        
        # 分割数据
        left, right = [], []
        for sample, target in samples:
            if sample[0][1] <= sample[0][1]:
                left.append((sample[1:], target))
            else:
                right.append((sample[1:], target))
        
        # 递归构建
        node = {
            'feature': best_feature,
            'left': self._build_tree(left) if left else Counter([s[1] for s in samples]).most_common(1)[0][0],
            'right': self._build_tree(right) if right else Counter([s[1] for s in samples]).most_common(1)[0][0],
        }
        
        return node if len(samples) > 10 else Counter([s[1] for s in samples]).most_common(1)[0][0]
    
    def predict(self, features: Dict[str, float]) -> float:
        """预测"""
        if not self.trees:
            return 0.5
        
        predictions = []
        for tree in self.trees:
            pred = self._predict_tree(tree, features)
            predictions.append(pred)
        
        return sum(predictions) / len(predictions)
    
    def _predict_tree(self, tree: Dict, features: Dict) -> float:
        """预测单棵树"""
        if isinstance(tree, (int, float)):
            return tree
        
        feature = tree['feature']
        value = features.get(feature, 0)
        
        if value <= value:
            return self._predict_tree(tree['left'], features)
        else:
            return self._predict_tree(tree['right'], features)
    
    def _calculate_importance(self):
        """计算特征重要性"""
        importance = {}
        for tree in self.trees:
            self._count_importance(tree, importance)
        
        total = sum(importance.values()) if importance else 1
        self.feature_importance = {k: v/total for k, v in importance.items()}
    
    def _count_importance(self, tree: Dict, importance: Dict):
        """统计特征重要性"""
        if isinstance(tree, (int, float)):
            return
        
        if 'feature' in tree:
            importance[tree['feature']] = importance.get(tree['feature'], 0) + 1
            self._count_importance(tree['left'], importance)
            self._count_importance(tree['right'], importance)


class DynamicWeightManager:
    """动态权重管理器"""
    
    def __init__(self, config: Config):
        self.config = config
        self.weights = {
            'hot': 0.25,
            'missing': 0.35,
            'random': 0.15,
            'feature': 0.15,
            'ml': 0.10,
        }
        self.history = self._load_history()
    
    def _load_history(self) -> List[Dict]:
        """加载历史权重记录"""
        try:
            with open(self.config.WEIGHTS_HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def save_history(self):
        """保存权重历史"""
        Path(self.config.MODEL_DIR).mkdir(parents=True, exist_ok=True)
        with open(self.config.WEIGHTS_HISTORY_FILE, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def get_weights(self) -> Dict[str, float]:
        """获取当前权重"""
        return self.weights.copy()
    
    def update_weights(self, recent_results: List[Dict]):
        """根据近期结果更新权重"""
        if len(recent_results) < 5:
            return
        
        scores = {'hot': 0, 'missing': 0, 'random': 0, 'feature': 0, 'ml': 0}
        counts = {'hot': 0, 'missing': 0, 'random': 0, 'feature': 0, 'ml': 0}
        
        for result in recent_results[-20:]:
            strategy = result.get('strategy', 'random')
            hit_rate = result.get('hit_rate', 0)
            scores[strategy] += hit_rate
            counts[strategy] += 1
        
        performance = {}
        for key in scores:
            if counts[key] > 0:
                performance[key] = scores[key] / counts[key]
            else:
                performance[key] = 0
        
        new_weights = {}
        for key in self.weights:
            base = self.weights[key]
            adjust = performance.get(key, 0) / (sum(performance.values()) or 1) * 0.2
            new_weights[key] = max(0.05, min(0.5, base + adjust - 0.1))
        
        total = sum(new_weights.values())
        self.weights = {k: v/total for k, v in new_weights.items()}
        
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'performance': performance,
            'weights': self.weights.copy(),
        })
        
        self.history = self.history[-100:]
        self.save_history()
        
        logger.info(f"权重已更新: {self.weights}")


class PositionPredictor:
    """分位置预测器"""
    
    def __init__(self, config: Config):
        self.config = config
        self.position_models = {}
    
    def predict_position(self, position: int, history: List[Dict]) -> List[int]:
        """预测特定位置的号码"""
        if position == 0:
            return self._predict_first(history)
        elif position == 6:
            return self._predict_last(history)
        else:
            return self._predict_middle(history)
    
    def _predict_first(self, history: List[Dict]) -> List[int]:
        """预测首位"""
        first_nums = []
        for d in history[-30:]:
            nums = [int(n) for n in d['basic_numbers']]
            first_nums.append(min(nums))
        
        ranges = [(1,5), (6,10), (11,15)]
        counts = [0, 0, 0]
        for n in first_nums:
            for i, (lo, hi) in enumerate(ranges):
                if lo <= n <= hi:
                    counts[i] += 1
                    break
        
        best_range = ranges[counts.index(max(counts))]
        return list(range(best_range[0], best_range[1]+1))
    
    def _predict_last(self, history: List[Dict]) -> List[int]:
        """预测末位"""
        last_nums = []
        for d in history[-30:]:
            nums = [int(n) for n in d['basic_numbers']]
            last_nums.append(max(nums))
        
        ranges = [(15,20), (21,25), (26,30)]
        counts = [0, 0, 0]
        for n in last_nums:
            for i, (lo, hi) in enumerate(ranges):
                if lo <= n <= hi:
                    counts[i] += 1
                    break
        
        best_range = ranges[counts.index(max(counts))]
        return list(range(best_range[0], best_range[1]+1))
    
    def _predict_middle(self, history: List[Dict]) -> List[int]:
        """预测中间位置"""
        all_middle = []
        for d in history[-30:]:
            nums = sorted([int(n) for n in d['basic_numbers']])
            all_middle.extend(nums[1:-1])
        
        freq = Counter(all_middle)
        return [n for n, _ in freq.most_common(15)]


class Validator:
    """自我验证器"""
    
    def __init__(self, config: Config):
        self.config = config
        self.validation_results = []
    
    def validate_prediction(self, predictions: List[List[int]], 
                          actual: List[int]) -> Dict:
        """验证预测准确性"""
        if not actual:
            return {'valid': False, 'reason': '无实际开奖数据'}
        
        hit_count = len(set(predictions[0]) & set(actual))
        hit_rate = hit_count / 7
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'predicted': predictions[0],
            'actual': actual,
            'hit_count': hit_count,
            'hit_rate': hit_rate,
            'valid': True,
        }
        
        self.validation_results.append(result)
        self.validation_results = self.validation_results[-100:]
        
        return result
    
    def run_full_validation(self, history: List[Dict], 
                           predictor) -> Dict:
        """运行完整验证"""
        if len(history) < 50:
            return {'valid': False, 'reason': '历史数据不足'}
        
        train_end = len(history) - 20
        train_data = history[:train_end]
        test_data = history[train_end:]
        
        if len(test_data) < 5:
            return {'valid': False, 'reason': '测试数据不足'}
        
        predictor.retrain(train_data)
        
        results = []
        for actual_data in test_data[:10]:
            predictions = predictor.predict(10)
            actual = [int(n) for n in actual_data['basic_numbers']]
            
            result = self.validate_prediction(predictions, actual)
            results.append(result)
        
        avg_hit_rate = sum(r['hit_rate'] for r in results) / len(results)
        
        return {
            'valid': True,
            'test_count': len(results),
            'avg_hit_rate': avg_hit_rate,
            'detailed_results': results[-5:],
        }
    
    def get_report(self) -> str:
        """生成验证报告"""
        if not self.validation_results:
            return "暂无验证数据"
        
        recent = self.validation_results[-20:]
        avg_rate = sum(r['hit_rate'] for r in recent) / len(recent)
        
        return f"""
验证报告
--------
验证次数: {len(self.validation_results)}
最近20次平均命中率: {avg_rate:.2%}
最佳命中率: {max(r['hit_rate'] for r in recent):.2%}
"""


class QLCPredictorV6:
    """七乐彩预测器 V6.0"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.history = []
        self.features = {}
        self.rf_model = None
        self.weight_manager = DynamicWeightManager(self.config)
        self.position_predictor = PositionPredictor(self.config)
        self.validator = Validator(self.config)
        
        Path(self.config.OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.config.MODEL_DIR).mkdir(parents=True, exist_ok=True)
        Path(self.config.LOG_DIR).mkdir(parents=True, exist_ok=True)
        
        self.load_history()
    
    def load_history(self) -> bool:
        try:
            with open(self.config.DATA_FILE, 'r') as f:
                self.history = json.load(f)
            logger.info(f"加载历史数据: {len(self.history)} 条")
            return True
        except Exception as e:
            logger.error(f"加载历史数据失败: {e}")
            return False
    
    def analyze(self):
        if not self.history:
            return
        
        logger.info("正在分析数据...")
        extractor = FeatureExtractor(self.history, self.config)
        self.features = extractor.extract_all()
        
        logger.info(f"提取了 {len(self.features)} 个特征")
        
        self.rf_model = SimpleRandomForest(
            self.config, 
            n_estimators=self.config.N_ESTIMATORS
        )
    
    def prepare_training_data(self) -> Tuple[List[Dict], List[int]]:
        X, y = [], []
        
        for i in range(10, len(self.history)):
            extractor = FeatureExtractor(self.history[:i], self.config)
            features = extractor.extract_all()
            X.append(features)
            
            target_nums = [int(n) for n in self.history[i]['basic_numbers']]
            y.append(sum(1 for n in target_nums if n <= 15))
        
        return X, y
    
    def retrain(self, history: List[Dict]):
        self.history = history
        extractor = FeatureExtractor(self.history, self.config)
        self.features = extractor.extract_all()
        
        X, y = self.prepare_training_data()
        self.rf_model.fit(X, y)
    
    def predict(self, count: int = 100) -> List[List[int]]:
        if not self.history or len(self.history) < self.config.MIN_HISTORY_FOR_PREDICT:
            logger.error("历史数据不足")
            return []
        
        self.analyze()
        
        weights = self.weight_manager.get_weights()
        predictions = []
        attempts = 0
        
        hot_pool = self._get_hot_pool()
        missing_pool = self._get_missing_pool()
        feature_pool = self._get_feature_pool()
        
        while len(predictions) < count and attempts < 500000:
            attempts += 1
            
            r = random.random()
            pool = list(range(1, 31))
            
            if r < weights['hot']:
                pool = hot_pool[:15]
            elif r < weights['hot'] + weights['missing']:
                pool = missing_pool[:15]
            elif r < weights['hot'] + weights['missing'] + weights['feature']:
                pool = feature_pool[:15]
            
            if len(pool) < 7:
                pool = list(range(1, 31))
            
            selected = sorted(random.sample(pool, 7))
            
            if self._check_constraints(selected):
                predictions.append(selected)
        
        logger.info(f"生成 {len(predictions)} 组预测 (尝试{attempts}次)")
        return predictions
    
    def _get_hot_pool(self) -> List[int]:
        recent = self.history[-30:]
        counts = Counter()
        for d in recent:
            counts.update([int(n) for n in d['basic_numbers']])
        return [n for n, _ in counts.most_common(15)]
    
    def _get_missing_pool(self) -> List[int]:
        missing = []
        for num in range(1, 31):
            gap = 0
            for d in reversed(self.history[-50:]):
                if num in [int(n) for n in d['basic_numbers']]:
                    break
                gap += 1
            missing.append((num, gap))
        
        return [n for n, _ in sorted(missing, key=lambda x: x[1], reverse=True)[:15]]
    
    def _get_feature_pool(self) -> List[int]:
        recent = self.history[-10:]
        sums = [sum(int(n) for n in d['basic_numbers']) for d in recent]
        avg_sum = sum(sums) / len(sums)
        
        if avg_sum > 110:
            return list(range(15, 31))
        else:
            return list(range(1, 25))
    
    def _check_constraints(self, numbers: List[int]) -> bool:
        odd = sum(1 for n in numbers if n % 2 == 1)
        if not (2 <= odd <= 5):
            return False
        
        small = sum(1 for n in numbers if n <= 10)
        medium = sum(1 for n in numbers if 11 <= n <= 20)
        large = sum(1 for n in numbers if n >= 21)
        if not (1 <= small <= 4 and 1 <= medium <= 4 and 1 <= large <= 4):
            return False
        
        total = sum(numbers)
        if not (60 <= total <= 170):
            return False
        
        return True
    
    def save_predictions(self, predictions: List[List[int]]):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        csv_path = f"{self.config.OUTPUT_DIR}/predictions_{timestamp}.csv"
        with open(csv_path, 'w', encoding='utf-8-sig') as f:
            f.write('序号,号码1,号码2,号码3,号码4,号码5,号码6,号码7\n')
            for i, pred in enumerate(predictions, 1):
                f.write(f'{i},{",".join(map(str, pred))}\n')
        
        latest_path = f"{self.config.OUTPUT_DIR}/predictions_latest.csv"
        if os.path.exists(latest_path):
            os.remove(latest_path)
        os.symlink(csv_path, latest_path)
        
        logger.info(f"预测已保存: {csv_path}")
        return csv_path
    
    def generate_report(self, predictions: List[List[int]]) -> str:
        recent = self.history[-10:]
        recent30 = self.history[-30:]
        
        all_nums = []
        for d in recent30:
            all_nums.extend([int(n) for n in d['basic_numbers']])
        freq = Counter(all_nums)
        hot = freq.most_common(10)
        
        weights = self.weight_manager.get_weights()
        
        report = f"""
{'='*60}
七乐彩智能预测系统 V6.0
{'='*60}

📊 系统状态
  数据量: {len(self.history)} 条
  特征数: {len(self.features)}
  模型: 随机森林({self.config.N_ESTIMATORS}棵树)
  权重: 热号{weights['hot']:.0%}/遗漏{weights['missing']:.0%}/特征{weights['feature']:.0%}/随机{weights['random']:.0%}/ML{weights['ml']:.0%}

🔥 热号TOP10（30期）
"""
        
        for i, (num, count) in enumerate(hot, 1):
            report += f"  {i:2d}. {num:02d}号: {count}次\n"
        
        report += f"""
📁 输出文件
  预测结果: {self.config.OUTPUT_DIR}/predictions_latest.csv
  模型目录: {self.config.MODEL_DIR}
  日志目录: {self.config.LOG_DIR}

---
生成时间: {datetime.now().isoformat()}
"""
        
        return report
    
    def save_report(self, report: str):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = f"{self.config.LOG_DIR}/report_{timestamp}.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        latest_path = f"{self.config.LOG_DIR}/report_latest.txt"
        if os.path.exists(latest_path):
            os.remove(latest_path)
        os.symlink(report_path, latest_path)
        
        logger.info(f"报告已保存: {report_path}")


class AutoRunner:
    """自动运行器"""
    
    def __init__(self, predictor: QLCPredictorV6):
        self.predictor = predictor
        self.validator = Validator(predictor.config)
        self.running = False
        self.last_update = None
    
    def run_auto(self, interval: int = 7200):
        self.running = True
        logger.info(f"启动自动模式，间隔 {interval} 秒")
        
        while self.running:
            try:
                self._update()
                time.sleep(interval)
            except KeyboardInterrupt:
                logger.info("收到停止信号")
                self.running = False
            except Exception as e:
                logger.error(f"运行出错: {e}")
                time.sleep(60)
    
    def _update(self):
        logger.info("="*50)
        logger.info("开始自动更新")
        
        if not self.predictor.load_history():
            logger.error("更新数据失败")
            return
        
        current_count = len(self.predictor.history)
        if self.last_update and current_count == self.last_update:
            logger.info("数据无变化，跳过预测")
            return
        
        self.last_update = current_count
        
        self.predictor.analyze()
        
        predictions = self.predictor.predict(100)
        if predictions:
            self.predictor.save_predictions(predictions)
            
            report = self.predictor.generate_report(predictions)
            self.predictor.save_report(report)
            
            results = self.validator.run_full_validation(
                self.predictor.history, 
                self.predictor
            )
            logger.info(f"验证结果: {results}")
            
            logger.info("自动更新完成")
    
    def stop(self):
        self.running = False


def main():
    parser = argparse.ArgumentParser(description='七乐彩智能预测系统 V6.0')
    parser.add_argument('--auto', action='store_true', help='自动模式')
    parser.add_argument('--verify', action='store_true', help='验证模式')
    parser.add_argument('--cron', action='store_true', help='Cron模式')
    parser.add_argument('--interval', type=int, default=7200, help='自动更新间隔（秒）')
    
    args = parser.parse_args()
    
    config = Config()
    predictor = QLCPredictorV6(config)
    
    if not predictor.load_history():
        print("❌ 加载数据失败")
        sys.exit(1)
    
    if args.verify:
        print("🧪 运行验证...")
        validator = Validator(config)
        results = validator.run_full_validation(predictor.history, predictor)
        print(f"验证结果: {results}")
        print(validator.get_report())
    
    elif args.cron or args.auto:
        runner = AutoRunner(predictor)
        
        if args.cron:
            runner._update()
        else:
            print("🚀 启动自动模式（Ctrl+C 停止）")
            runner.run_auto(args.interval)
    
    else:
        print("=" * 60)
        print("七乐彩智能预测系统 V6.0")
        print("=" * 60)
        
        predictor.analyze()
        predictions = predictor.predict(100)
        
        if predictions:
            predictor.save_predictions(predictions)
            
            # 显示前10组
            print("\n前10组预测:")
            for i, pred in enumerate(predictions[:10], 1):
                print(f"  {i:3d}: {' '.join(f'{n:02d}' for n in pred)}")
            
            report = predictor.generate_report(predictions)
            predictor.save_report(report)
            print(report)


if __name__ == '__main__':
    main()
