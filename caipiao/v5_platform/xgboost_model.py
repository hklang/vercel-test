#!/usr/bin/env python3
"""
XGBoost模型 - V7.0步骤3
包含降级策略（纯Python备用方案）
"""

import json
import random
import math
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from pathlib import Path


class PurePythonForest:
    """纯Python决策树森林（备用方案）"""
    
    def __init__(self, n_trees: int = 50, max_depth: int = 5):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.trees = []
        self.feature_names = []
    
    def train(self, X: List[Dict], y: List[int]) -> bool:
        """训练"""
        if not X or len(X) < 10:
            return False
        
        self.feature_names = sorted(X[0].keys()) if X else []
        X_matrix = [[row.get(f, 0) for f in self.feature_names] for row in X]
        
        self.trees = []
        for _ in range(self.n_trees):
            # 随机采样（Bootstrap）
            indices = [random.randint(0, len(X_matrix)-1) for _ in range(len(X_matrix))]
            sampled = [(X_matrix[i], y[i]) for i in indices]
            
            tree = self._build_tree(sampled, 0)
            if tree:
                self.trees.append(tree)
        
        return len(self.trees) > 0
    
    def _build_tree(self, data: List[Tuple], depth: int) -> Optional[Dict]:
        if not data or depth >= self.max_depth:
            return {'leaf': sum(y for _, y in data) / len(data) if data else 0.5}
        
        feature_idx = random.randint(0, len(self.feature_names) - 1)
        values = [x[feature_idx] for x, _ in data]
        threshold = sum(values) / len(values) if values else 0.5
        
        left = [(x, y) for x, y in data if x[feature_idx] <= threshold]
        right = [(x, y) for x, y in data if x[feature_idx] > threshold]
        
        left_tree = self._build_tree(left, depth + 1) if len(left) > 1 else {'leaf': sum(y for _, y in left) / len(left) if left else 0.5}
        right_tree = self._build_tree(right, depth + 1) if len(right) > 1 else {'leaf': sum(y for _, y in right) / len(right) if right else 0.5}
        
        return {'feature_idx': feature_idx, 'threshold': threshold, 'left': left_tree, 'right': right_tree}
    
    def predict(self, features: Dict[str, float]) -> float:
        if not self.trees:
            return 0.5
        
        predictions = []
        for tree in self.trees:
            pred = self._predict_tree(tree, features)
            predictions.append(pred)
        
        return sum(predictions) / len(predictions) if predictions else 0.5
    
    def _predict_tree(self, tree: Dict, features: Dict) -> float:
        if 'leaf' in tree:
            return tree['leaf']
        
        feature_idx = tree['feature_idx']
        if feature_idx < len(self.feature_names):
            value = features.get(self.feature_names[feature_idx], 0)
            if value <= tree['threshold']:
                return self._predict_tree(tree['left'], features)
            else:
                return self._predict_tree(tree['right'], features)
        return 0.5


class XGBoostModel:
    """XGBoost模型（带降级到纯Python）"""
    
    def __init__(self):
        self.model = None
        self.use_xgboost = False
        self.xgb = None
        self.pure_forest = None
        
        # 尝试导入XGBoost
        try:
            import xgboost as xgb
            self.xgb = xgb
            self.use_xgboost = True
            print("✅ XGBoost模块可用")
        except ImportError:
            self.xgb = None
            self.use_xgboost = False
            print("⚠️ XGBoost不可用，将使用纯Python备用方案")
            self.pure_forest = PurePythonForest()
    
    def train(self, X: List[Dict], y: List[int]) -> bool:
        """训练模型"""
        if not X or len(X) < 10:
            print("❌ 训练数据不足")
            return False
        
        if self.use_xgboost and self.xgb:
            return self._train_xgboost(X, y)
        else:
            return self._train_pure_python(X, y)
    
    def _train_xgboost(self, X: List[Dict], y: List[int]) -> bool:
        """XGBoost训练"""
        try:
            feature_names = sorted(X[0].keys()) if X else []
            X_matrix = [[row.get(f, 0) for f in feature_names] for row in X]
            
            params = {
                'objective': 'reg:squarederror',
                'max_depth': 5,
                'learning_rate': 0.1,
                'n_estimators': 100,
                'random_state': 42,
            }
            
            self.model = self.xgb.XGBRegressor(**params)
            self.model.fit(X_matrix, y)
            
            print(f"✅ XGBoost训练完成，{len(feature_names)}个特征")
            return True
            
        except Exception as e:
            print(f"❌ XGBoost训练失败: {e}")
            return self._train_pure_python(X, y)
    
    def _train_pure_python(self, X: List[Dict], y: List[int]) -> bool:
        """纯Python训练"""
        print("🌲 使用纯Python决策树森林...")
        self.model = PurePythonForest()
        success = self.model.train(X, y)
        if success:
            print(f"✅ 纯Python森林训练完成，{len(self.model.trees)}棵树")
        return success
    
    def predict(self, features: Dict[str, float]) -> float:
        """预测"""
        if not self.model:
            return 0.5
        
        if self.use_xgboost and hasattr(self.model, 'predict'):
            return self._predict_xgboost(features)
        else:
            return self.model.predict(features)
    
    def _predict_xgboost(self, features: Dict[str, float]) -> float:
        feature_names = self.model.feature_names_in_
        X = [[features.get(f, 0) for f in feature_names]]
        return self.model.predict(X)[0]


class EnsemblePredictor:
    """集成预测器（随机森林 + XGBoost）"""
    
    def __init__(self):
        self.rf = PurePythonForest(n_trees=50, max_depth=5)
        self.xgb = XGBoostModel()
        self.weights = {'rf': 0.5, 'xgb': 0.5}
    
    def train(self, X: List[Dict], y: List[int]) -> bool:
        """训练两个模型"""
        print("=== 训练集成模型 ===")
        
        # 训练随机森林
        print("1. 训练随机森林...")
        rf_success = self.rf.train(X, y)
        
        # 训练XGBoost
        print("2. 训练XGBoost...")
        xgb_success = self.xgb.train(X, y)
        
        # 调整权重
        if xgb_success and self.xgb.use_xgboost:
            self.weights = {'rf': 0.4, 'xgb': 0.6}
            print("\n✅ 集成模型就绪，权重: RF=40%, XGB=60%")
        else:
            self.weights = {'rf': 1.0, 'xgb': 0.0}
            print("\n✅ 纯随机森林模式，权重: RF=100%")
        
        return rf_success
    
    def predict(self, features: Dict[str, float]) -> float:
        """集成预测"""
        rf_pred = self.rf.predict(features)
        xgb_pred = self.xgb.predict(features)
        
        return self.weights['rf'] * rf_pred + self.weights['xgb'] * xgb_pred


def main():
    """测试"""
    print("=== XGBoost模型测试 ===\n")
    
    # 模拟训练数据
    print("生成模拟数据...")
    X = [{f'f{i}': random.random() for i in range(20)} for _ in range(200)]
    y = [random.randint(0, 7) for _ in range(200)]
    
    # 测试集成模型
    print("\n测试集成模型...")
    ensemble = EnsemblePredictor()
    ensemble.train(X, y)
    
    # 预测
    test_features = {f'f{i}': random.random() for i in range(20)}
    pred = ensemble.predict(test_features)
    print(f"预测结果: {pred:.3f}")
    
    # 测试纯Python森林
    print("\n测试纯Python森林...")
    rf = PurePythonForest(n_trees=30)
    rf.train(X, y)
    pred2 = rf.predict(test_features)
    print(f"随机森林预测: {pred2:.3f}")


if __name__ == '__main__':
    main()
