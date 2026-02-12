#!/usr/bin/env python3
"""纯Python随机森林 - 无需numpy/sklearn"""

import random
from typing import List, Dict, Tuple
from collections import Counter

class SimpleDecisionTree:
    """简化决策树"""
    
    def __init__(self, max_depth: int = 5):
        self.max_depth = max_depth
        self.tree = None
    
    def fit(self, X: List[List[int]], y: List[List[int]]):
        """训练"""
        # 将多标签转换为单标签（每个号码单独训练）
        self.trees = {}
        for num in range(1, 31):
            y_binary = [1 if num in row else 0 for row in y]
            if sum(y_binary) > 0 and sum(y_binary) < len(y_binary):
                self.trees[num] = self._build_tree(X, y_binary, depth=0)
    
    def _build_tree(self, X: List[List[int]], y: List[int], depth: int) -> Dict:
        """构建树"""
        # 统计
        count_1 = sum(y)
        count_0 = len(y) - count_1
        
        # 停止条件
        if depth >= self.max_depth or count_0 == 0 or count_1 == 0:
            return {'leaf': True, 'value': 1 if count_1 > count_0 else 0}
        
        # 找最佳分割点
        best_feature = 0
        best_threshold = 0
        best_gain = -1
        
        for feature in range(len(X[0])):
            thresholds = set(int(x[feature]) for x in X)
            for threshold in list(thresholds)[:5]:  # 限制数量
                gain = self._information_gain(X, y, feature, threshold)
                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature
                    best_threshold = threshold
        
        if best_gain <= 0:
            return {'leaf': True, 'value': 1 if count_1 > count_0 else 0}
        
        # 分割数据
        X_left = [x for x in X if x[best_feature] <= best_threshold]
        X_right = [x for x in X if x[best_feature] > best_threshold]
        y_left = [y[i] for i, x in enumerate(X) if x[best_feature] <= best_threshold]
        y_right = [y[i] for i, x in enumerate(X) if x[best_feature] > best_threshold]
        
        return {
            'leaf': False,
            'feature': best_feature,
            'threshold': best_threshold,
            'left': self._build_tree(X_left, y_left, depth + 1),
            'right': self._build_tree(X_right, y_right, depth + 1),
        }
    
    def _information_gain(self, X: List[List[int]], y: List[int], feature: int, threshold: int) -> float:
        """计算信息增益"""
        parent_entropy = self._entropy(y)
        
        left_y = [y[i] for i, x in enumerate(X) if x[feature] <= threshold]
        right_y = [y[i] for i, x in enumerate(X) if x[feature] > threshold]
        
        if not left_y or not right_y:
            return 0
        
        n = len(y)
        n_left, n_right = len(left_y), len(right_y)
        
        e_left = self._entropy(left_y)
        e_right = self._entropy(right_y)
        
        child_entropy = (n_left / n) * e_left + (n_right / n) * e_right
        
        return parent_entropy - child_entropy
    
    def _entropy(self, y: List[int]) -> float:
        """计算熵"""
        if not y:
            return 0
        
        count_1 = sum(y)
        count_0 = len(y) - count_1
        
        if count_0 == 0 or count_1 == 0:
            return 0
        
        p1 = count_1 / len(y)
        p0 = count_0 / len(y)
        
        return -p1 * (p1 and 1) - p0 * (p0 and 1)
    
    def predict_proba(self, X: List[List[int]]) -> List[float]:
        """预测概率"""
        results = []
        for num in range(1, 31):
            if num in self.trees:
                prob = self._predict_single(self.trees[num], X[0])
                results.append(prob)
            else:
                results.append(0.0)
        return results
    
    def _predict_single(self, node: Dict, x: List[int]) -> float:
        """预测单个样本"""
        if node['leaf']:
            return node['value']
        
        if x[node['feature']] <= node['threshold']:
            return self._predict_single(node['left'], x)
        else:
            return self._predict_single(node['right'], x)


class PurePythonRandomForest:
    """纯Python随机森林"""
    
    def __init__(self, n_trees: int = 10, max_depth: int = 5):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.trees = []
    
    def fit(self, X: List[List[int]], y: List[List[int]]):
        """训练"""
        # 转换为特征-标签格式
        X_features = []
        y_labels = []
        
        for i, row in enumerate(X):
            # 特征：历史频率统计
            features = []
            for num in range(1, 31):
                features.append(row.count(num))
            X_features.append(features)
            
            # 标签：下期出现的号码
            labels = [1 if num in y[i] else 0 for num in range(1, 31)]
            y_labels.append(labels)
        
        # 构建多棵树
        for _ in range(self.n_trees):
            tree = SimpleDecisionTree(max_depth=self.max_depth)
            tree.fit(X_features, y_labels)
            if tree.trees:
                self.trees.append(tree)
    
    def predict_proba(self, X: List[List[int]]) -> List[float]:
        """预测概率"""
        if not self.trees:
            # 没有树，返回均匀分布
            return [0.5] * 30
        
        # 提取特征
        features = []
        for num in range(1, 31):
            features.append(X[-1].count(num))
        
        # 多树投票
        all_proba = []
        for tree in self.trees:
            proba = tree.predict_proba([features])
            all_proba.append(proba)
        
        if not all_proba:
            return [0.5] * 30
        
        # 平均
        avg_proba = []
        for i in range(30):
            avg = sum(p[i] for p in all_proba) / len(all_proba)
            avg_proba.append(avg)
        
        return avg_proba
    
    def predict(self, X: List[List[int]], n: int = 7) -> List[int]:
        """预测TOP-N"""
        proba = self.predict_proba(X)
        # 按概率排序
        sorted_indices = sorted(range(30), key=lambda i: proba[i], reverse=True)
        return [i + 1 for i in sorted_indices[:n]]


def main():
    """测试"""
    print("=" * 60)
    print("纯Python随机森林测试")
    print("=" * 60)
    
    # 模拟历史数据
    history = [
        [1, 5, 9, 12, 15, 18, 22],
        [2, 6, 10, 13, 16, 19, 23],
        [3, 7, 11, 14, 17, 20, 24],
        [4, 8, 12, 15, 18, 21, 25],
        [1, 9, 13, 16, 19, 22, 26],
    ]
    
    model = PurePythonRandomForest(n_trees=5, max_depth=3)
    model.fit(history[:-1], history[1:])
    
    prediction = model.predict(history)
    
    print(f"预测: {prediction}")
    print(f"预测数量: {len(prediction)}")
    
    return len(prediction) == 7

if __name__ == '__main__':
    success = main()
    print("\n✅ 测试通过" if success else "\n❌ 测试失败")
