#!/usr/bin/env python3
"""
七乐彩自动优化系统 V1.0
========================

功能：
1. 每小时自动发现新预测方法
2. 自动验证命中率
3. 淘汰机制（10次后<40%删除）
4. 飞书反馈

运行方式：
    python3 optimizer_auto.py          # 运行一次
    python3 optimizer_auto.py --auto  # 守护进程模式（每小时）
"""

import os
import sys
import json
import random
import time
import argparse
from datetime import datetime
from typing import Dict, List
from collections import Counter
from pathlib import Path

# 配置
CONFIG = {
    'DATA_FILE': '/home/lang/.openclaw/workspace/caipiao/qlc_history_full.json',
    'STATS_DIR': '/home/lang/.openclaw/workspace/caipiao/v5_platform/stats',
    'METHODS_DIR': '/home/lang/.openclaw/workspace/caipiao/v5_platform/methods',
    'LOG_DIR': '/home/lang/.openclaw/workspace/caipiao/v5_platform/logs',
}

os.makedirs(CONFIG['STATS_DIR'], exist_ok=True)
os.makedirs(CONFIG['METHODS_DIR'], exist_ok=True)
os.makedirs(CONFIG['LOG_DIR'], exist_ok=True)


def load_history() -> List[Dict]:
    """加载历史数据"""
    try:
        with open(CONFIG['DATA_FILE'], 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 加载数据失败: {e}")
        return []


# ==================== 基础预测方法 ====================
METHODS_REGISTRY = {
    '遗漏值法': {'window': None, '依据': '遗漏值>20期优先'},
    '热号法': {'window': 30, '依据': '30期内出现≥10次'},
    '大小号法': {'window': 50, '依据': '小:01-10/中:11-20/大:21-30均衡'},
    '奇偶法': {'window': 50, '依据': '奇偶比例3-4个'},
    '和值法': {'window': 200, '依据': '历史平均和值105±20'},
    '三区比': {'window': 100, '依据': '01-10/11-20/21-30分布均衡'},
    '012路法': {'window': 100, '依据': '除3余0/1/2各2-3个'},
    '连号法': {'window': 30, '依据': '每期1-2组连号'},
    '同尾法': {'window': 50, '依据': '尾数重复概率'},
    '重号法': {'window': 30, '依据': '与上期重复2-3个'},
    'AC值法': {'window': 50, '依据': 'AC值10-12为佳'},
    '极距法': {'window': 100, '依据': '极距18-22'},
    '周期回补法': {'window': None, '依据': '周期性遗漏回补'},
}

# ==================== 预测助手已纳入了的方法（不再搜索） ====================
PREDICTOR_METHODS = {
    # 13种基础方法
    '遗漏值法', '热号法', '大小号法', '奇偶法', '和值法', '三区比', 
    '012路法', '连号法', '同尾法', '重号法', 'AC值法', '极距法', '周期回补法',
    # 4个系统版本
    'V5.0基础版', 'V5.1增强版', 'V6.0智能版', 'V7.0完整版',
    # 已发现的变种（如果有的话）
    '遗漏值法_大遗漏', '遗漏值法_回补', '热号法_20期', '热号法_50期', 
    '热号法_加权', '奇偶法_偏奇', '奇偶法_偏偶', '三区比_偏小', '三区比_偏大',
    '012路法_偏0路', '012路法_偏1路', '012路法_偏2路',
}

# 变种方法生成器（只生成预测助手没有的方法）
METHOD_VARIANTS = {
    '遗漏值法': [
        ('遗漏值法_大遗漏', {'window': None, '依据': '遗漏值>25期优先', 'threshold': 25}),
        ('遗漏值法_回补', {'window': None, '依据': '遗漏10-20期即将回补', 'threshold': 15, 'mode': 'recovery'}),
    ],
    '热号法': [
        ('热号法_20期', {'window': 20, '依据': '20期热号'}),
        ('热号法_50期', {'window': 50, '依据': '50期热号'}),
        ('热号法_加权', {'window': 30, '依据': '近期加权热号', 'weighted': True}),
    ],
    '奇偶法': [
        ('奇偶法_偏奇', {'window': 50, '依据': '奇数偏多(4-5个)', 'odd_bias': True}),
        ('奇偶法_偏偶', {'window': 50, '依据': '偶数偏多(4-5个)', 'odd_bias': False}),
    ],
    '三区比': [
        ('三区比_偏小', {'window': 100, '依据': '小区偏多', 'small_bias': True}),
        ('三区比_偏大', {'window': 100, '依据': '大区偏多', 'large_bias': True}),
    ],
    '012路法': [
        ('012路法_偏0路', {'window': 100, '依据': '0路号码偏多', 'road_bias': 0}),
        ('012路法_偏1路', {'window': 100, '依据': '1路号码偏多', 'road_bias': 1}),
        ('012路法_偏2路', {'window': 100, '依据': '2路号码偏多', 'road_bias': 2}),
    ],
}


class Predictor:
    """预测器"""
    
    def __init__(self, history: List[Dict]):
        self.history = history
    
    def generate_pool(self, method_name: str, params: Dict) -> List[int]:
        """生成号码池"""
        recent = self.history[-30:]
        all_nums = []
        for d in recent:
            all_nums.extend([int(n) for n in d['basic_numbers']])
        freq = Counter(all_nums)
        
        # 基础池
        pool = list(range(1, 31))
        
        # 根据方法选择
        if '热号' in method_name:
            window = params.get('window', 30)
            recent = self.history[-window:]
            counts = Counter()
            for d in recent:
                counts.update([int(n) for n in d['basic_numbers']])
            pool = [n for n, _ in counts.most_common(15)]
            
            if params.get('weighted'):
                # 加权热号
                weighted = []
                for n in range(1, 31):
                    count = 0
                    for i, d in enumerate(recent[-10:]):
                        if n in [int(x) for x in d['basic_numbers']]:
                            count += (10 - i)
                    weighted.append((n, count))
                pool = [n for n, _ in sorted(weighted, key=lambda x: x[1], reverse=True)[:15]]
        
        elif '遗漏' in method_name:
            missing = []
            threshold = params.get('threshold', 20)
            mode = params.get('mode', 'high')
            
            for num in range(1, 31):
                gap = 0
                for d in reversed(self.history[-50:]):
                    if num in [int(n) for n in d['basic_numbers']]:
                        break
                    gap += 1
                
                if mode == 'recovery':
                    if 10 <= gap <= threshold:
                        missing.append(num)
                else:
                    if gap >= threshold:
                        missing.append(num)
            
            pool = missing if missing else list(range(1, 31))
        
        elif '奇偶' in method_name:
            odds = [sum(1 for n in d['basic_numbers'] if int(n) % 2 == 1) for d in recent[-20:]]
            avg_odd = sum(odds) / len(odds)
            
            target_odd = 4 if params.get('odd_bias', None) else (3 if avg_odd > 3.5 else 4)
            
            pool = []
            for n in range(1, 31):
                is_odd = n % 2 == 1
                if (target_odd >= 4 and is_odd) or (target_odd < 4 and not is_odd):
                    pool.append(n)
        
        elif '三区' in method_name:
            small, medium, large = [], [], []
            for n in range(1, 31):
                if n <= 10:
                    small.append(n)
                elif n <= 20:
                    medium.append(n)
                else:
                    large.append(n)
            
            if params.get('small_bias'):
                pool = small[:7] + medium[:5] + large[:3]
            elif params.get('large_bias'):
                pool = small[:3] + medium[:5] + large[:7]
            else:
                pool = small[:5] + medium[:5] + large[:5]
        
        elif '012路' in method_name:
            road_bias = params.get('road_bias')
            pool = [n for n in range(1, 31) if n % 3 == road_bias][:10]
            if len(pool) < 7:
                pool = list(range(1, 31))
        
        elif '连号' in method_name:
            pool = []
            for d in recent[-10:]:
                nums = sorted([int(n) for n in d['basic_numbers']])
                for i in range(len(nums)-1):
                    if nums[i+1] - nums[i] == 1:
                        pool.extend([nums[i], nums[i+1]])
            pool = list(set(pool))
            if len(pool) < 7:
                pool = list(range(1, 31))
        
        elif '同尾' in method_name:
            tails = {}
            for n in range(1, 31):
                tail = n % 10
                if tail not in tails:
                    tails[tail] = []
                tails[tail].append(n)
            
            pool = []
            for d in recent[-20:]:
                for n in d['basic_numbers']:
                    t = int(n) % 10
                    pool.extend(tails[t])
            pool = list(set(pool))[:15]
        
        elif '重号' in method_name:
            if self.history:
                last_nums = [int(n) for n in self.history[-1]['basic_numbers']]
                pool = last_nums[:5]
                pool.extend(list(range(1, 31))[:5])
            else:
                pool = list(range(1, 31))
        
        elif '和值' in method_name:
            sums = [sum(int(n) for n in d['basic_numbers']) for d in recent[-20:]]
            avg_sum = sum(sums) / len(sums)
            
            if avg_sum > 120:
                pool = list(range(15, 31))
            elif avg_sum < 90:
                pool = list(range(1, 20))
            else:
                pool = list(range(1, 31))
        
        else:
            pool = list(range(1, 31))
        
        return pool if pool else list(range(1, 31))
    
    def predict(self, method_name: str, params: Dict, count: int = 10) -> List[List[int]]:
        """生成预测"""
        pool = self.generate_pool(method_name, params)
        predictions = []
        attempts = 0
        
        while len(predictions) < count and attempts < 1000:
            attempts += 1
            pred = sorted(random.sample(pool if len(pool) >= 7 else list(range(1, 31)), 7))
            
            # 基础约束
            odd = sum(1 for n in pred if n % 2 == 1)
            small = sum(1 for n in pred if n <= 10)
            large = sum(1 for n in pred if n >= 21)
            total = sum(pred)
            
            if 2 <= odd <= 5 and 1 <= small <= 4 and 1 <= large <= 4 and 60 <= total <= 170:
                predictions.append(pred)
        
        return predictions


class Optimizer:
    """优化器"""
    
    def __init__(self):
        self.history = []
        self.stats_file = f"{CONFIG['STATS_DIR']}/optimizer_stats.json"
        self.methods_file = f"{CONFIG['STATS_DIR']}/methods_registry.json"
        self.load_stats()
    
    def load_stats(self):
        """加载统计数据"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    self.stats = json.load(f)
            except:
                self.stats = {}
        else:
            self.stats = {}
        
        if os.path.exists(self.methods_file):
            try:
                with open(self.methods_file, 'r') as f:
                    self.methods = json.load(f)
            except:
                self.methods = dict(METHODS_REGISTRY)
        else:
            self.methods = dict(METHODS_REGISTRY)
    
    def save_stats(self):
        """保存统计"""
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, ensure_ascii=False, indent=2)
        
        with open(self.methods_file, 'w') as f:
            json.dump(self.methods, f, ensure_ascii=False, indent=2)
    
    def verify_method(self, method_name: str, params: Dict) -> Dict:
        """验证方法命中率"""
        if len(self.history) < 50:
            return {'error': '数据不足'}
        
        predictor = Predictor(self.history)
        
        # 用最近50期数据进行回测
        test_start = len(self.history) - 50
        test_data = self.history[test_start:]
        
        results = []
        for i, data in enumerate(test_data[:10]):  # 测10期
            actual = [int(n) for n in data['basic_numbers']]
            
            # 预测（基于之前的数据）
            pred_data = self.history[test_start + i - 10:test_start + i]
            temp_predictor = Predictor(pred_data)
            predictions = temp_predictor.predict(method_name, params, 10)
            
            # 计算命中率（取最佳预测）
            best_hit = 0
            for pred in predictions:
                hit = len(set(pred) & set(actual))
                if hit > best_hit:
                    best_hit = hit
            
            results.append({
                'issue': data['period'],
                'hit': best_hit,
                'hit3': 1 if best_hit >= 3 else 0,
                'hit4': 1 if best_hit >= 4 else 0,
                'hit5': 1 if best_hit >= 5 else 0,
            })
        
        # 统计
        hit3_rate = sum(r['hit3'] for r in results) / len(results)
        hit4_rate = sum(r['hit4'] for r in results) / len(results)
        hit5_rate = sum(r['hit5'] for r in results) / len(results)
        avg_hit = sum(r['hit'] for r in results) / len(results)
        
        return {
            'method': method_name,
            'periods': 10,
            'avg_hit': round(avg_hit, 2),
            'hit3': round(hit3_rate, 2),
            'hit4': round(hit4_rate, 2),
            'hit5': round(hit5_rate, 2),
            'results': results,
            'timestamp': datetime.now().isoformat(),
        }
    
    def update_method_stats(self, method_name: str, result: Dict):
        """更新方法统计"""
        if method_name not in self.stats:
            self.stats[method_name] = {
                'results': [],
                'hit3_total': 0,
                'hit4_total': 0,
                'hit5_total': 0,
                'periods': 0,
            }
        
        self.stats[method_name]['results'].append(result)
        self.stats[method_name]['results'] = self.stats[method_name]['results'][-10:]  # 保留最近10次
        
        # 累计
        self.stats[method_name]['hit3_total'] = sum(r['hit3'] for r in self.stats[method_name]['results'])
        self.stats[method_name]['hit4_total'] = sum(r['hit4'] for r in self.stats[method_name]['results'])
        self.stats[method_name]['hit5_total'] = sum(r['hit5'] for r in self.stats[method_name]['results'])
        self.stats[method_name]['periods'] = len(self.stats[method_name]['results'])
        
        self.save_stats()
    
    def check_elimination(self, method_name: str) -> str:
        """检查是否需要淘汰/升级"""
        if method_name not in self.stats:
            return 'new'
        
        s = self.stats[method_name]
        if s['periods'] < 10:
            return 'testing'
        
        # 10次后判断
        hit3_rate = s['hit3_total'] / s['periods']
        
        if hit3_rate < 0.40:
            return 'eliminate'  # 淘汰
        elif hit3_rate >= 0.60:
            return 'promote'  # 建议升级到预测助手
        else:
            return 'keep'  # 保留继续测试
    
    def discover_new_method(self) -> tuple:
        """发现新方法（排除预测助手已有的）"""
        # 优先选择待测试的变种方法
        tested = set(self.stats.keys())
        excluded = PREDICTOR_METHODS
        
        for base_method, variants in METHOD_VARIANTS.items():
            for variant_name, params in variants:
                if variant_name not in tested and variant_name not in excluded:
                    return variant_name, params
        
        # 如果都有测试了，返回一个新组合
        return '组合验证法', {'window': 30, '依据': '多方法组合验证'}
    
    def run_one(self) -> Dict:
        """运行一次优化"""
        print("="*60)
        print("🧪 七乐彩自动优化系统 V1.0")
        print("="*60)
        
        self.history = load_history()
        if not self.history:
            return {'error': '无历史数据'}
        
        print(f"📊 数据量: {len(self.history)}期")
        
        # 发现新方法
        method_name, params = self.discover_new_method()
        print(f"\n🔍 发现新方法: {method_name}")
        print(f"   依据: {params.get('依据', '')}")
        
        # 检查是否已纳入预测助手（跳过）
        if method_name in PREDICTOR_METHODS:
            print(f"\n⚠️ 方法已纳入预测助手，跳过验证")
            return {'status': 'skipped', 'method': method_name, 'reason': '已纳入预测助手'}
        
        # 验证
        print(f"\n📈 开始验证...")
        result = self.verify_method(method_name, params)
        
        if 'error' in result:
            print(f"❌ 验证失败: {result['error']}")
            return result
        
        print(f"   10期验证结果:")
        print(f"   3+命中率: {result['hit3']*100:.0f}%")
        print(f"   4+命中率: {result['hit4']*100:.0f}%")
        print(f"   5+命中率: {result['hit5']*100:.0f}%")
        print(f"   平均命中: {result['avg_hit']:.1f}/7")
        
        # 更新统计
        self.update_method_stats(method_name, result)
        
        # 检查状态
        status = self.check_elimination(method_name)
        status_text = {
            'new': '🆕 新发现',
            'testing': '🔄 测试中',
            'keep': '📊 继续测试',
            'promote': '✅ 建议加入预测助手！',
            'eliminate': '❌ 淘汰',
        }
        print(f"\n📌 状态: {status_text[status]}")
        
        # 如果有累计数据，显示
        if method_name in self.stats:
            s = self.stats[method_name]
            if s['periods'] > 1:
                hit3_avg = s['hit3_total'] / s['periods']
                print(f"   累计({s['periods']}次): 3+命中率 {hit3_avg*100:.0f}%")
        
        self.save_stats()
        
        return {
            'method': method_name,
            'params': params,
            'result': result,
            'status': status,
            'stats': self.stats.get(method_name),
        }


def generate_report(optimize_result: Dict) -> str:
    """生成飞书报告"""
    if 'error' in optimize_result:
        return f"❌ 优化失败: {optimize_result['error']}"
    
    # 跳过情况
    if optimize_result.get('status') == 'skipped':
        return f"""**【自动优化】**

⚠️ {optimize_result['method']}
   已纳入预测助手，跳过验证

---
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}"""
    
    method = optimize_result['method']
    result = optimize_result['result']
    status = optimize_result['status']
    stats = optimize_result.get('stats', {})
    
    # 状态emoji
    status_emoji = {
        'new': '🆕',
        'testing': '🔄',
        'keep': '📊',
        'promote': '✅',
        'eliminate': '❌',
    }
    status_text = {
        'new': '新发现',
        'testing': '测试中',
        'keep': '继续测试',
        'promote': '建议加入预测助手！',
        'eliminate': '淘汰',
    }
    
    # 累计统计
    cumulative = ""
    if stats and stats.get('periods', 0) > 1:
        hit3_avg = stats['hit3_total'] / stats['periods']
        hit4_avg = stats['hit4_total'] / stats['periods']
        hit5_avg = stats['hit5_total'] / stats['periods']
        cumulative = f"""
📈 累计统计({stats['periods']}次):
   • 3+命中率: {hit3_avg*100:.0f}%
   • 4+命中率: {hit4_avg*100:.0f}%
   • 5+命中率: {hit5_avg*100:.0f}%"""
    
    message = f"""**【自动优化】{method}**

{status_emoji[status]} 状态: {status_text[status]}

📋 依据: {result.get('依据', '')}

📊 本轮验证(10期):
   • 3+命中率: {result['hit3']*100:.0f}%
   • 4+命中率: {result['hit4']*100:.0f}%
   • 5+命中率: {result['hit5']*100:.0f}%
   • 平均命中: {result['avg_hit']:.1f}/7{cumulative}

---
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}"""
    
    return message


def main():
    parser = argparse.ArgumentParser(description='七乐彩自动优化系统')
    parser.add_argument('--auto', action='store_true', help='守护进程模式（每小时）')
    parser.add_argument('--once', action='store_true', help='运行一次')
    
    args = parser.parse_args()
    
    optimizer = Optimizer()
    
    if args.auto:
        print("🚀 启动自动优化守护进程（每小时）")
        while True:
            try:
                result = optimizer.run_one()
                print("\n⏰ 等待1小时...")
                time.sleep(3600)
            except KeyboardInterrupt:
                print("\n👋 停止")
                break
            except Exception as e:
                print(f"❌ 出错: {e}")
                time.sleep(60)
    else:
        result = optimizer.run_one()
        
        # 生成报告
        if result.get('status') == 'skipped':
            print(f"\n⚠️ {result['method']} 已纳入预测助手，跳过本次")
            print(f"   原因: {result.get('reason', '')}")
            return result
        
        report = generate_report(result)
        print("\n" + "="*60)
        print("飞书消息预览:")
        print("="*60)
        print(report)
        
        return report


if __name__ == '__main__':
    main()
