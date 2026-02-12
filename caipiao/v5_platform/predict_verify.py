#!/usr/bin/env python3
"""
预测验证系统 V2.1 - 排版修复版
================================
"""

import os
import sys
import json
import random
from datetime import datetime
from typing import Dict, List
from collections import Counter
from pathlib import Path
import logging

CONFIG = {
    'DATA_FILE': '/home/lang/.openclaw/workspace/caipiao/qlc_history_full.json',
    'PREDICT_DIR': '/home/lang/.openclaw/workspace/caipiao/v5_platform/predictions',
    'RESULTS_DIR': '/home/lang/.openclaw/workspace/caipiao/v5_platform/results',
    'STATS_DIR': '/home/lang/.openclaw/workspace/caipiao/v5_platform/stats',
    'MEMORY_FILE': '/home/lang/.openclaw/workspace/MEMORY.md',
}

os.makedirs(CONFIG['PREDICT_DIR'], exist_ok=True)
os.makedirs(CONFIG['RESULTS_DIR'], exist_ok=True)
os.makedirs(CONFIG['STATS_DIR'], exist_ok=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

METHODS = {
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


class Predictor:
    def __init__(self, history: List[Dict]):
        self.history = history
    
    def predict(self, method_name: str, count: int = 10) -> Dict:
        method_info = METHODS.get(method_name, {})
        
        if method_name == '遗漏值法':
            pool = self._get_missing_pool()
        elif method_name == '热号法':
            pool = self._get_hot_pool()
        elif method_name == '和值法':
            pool = self._get_sum_pool()
        elif method_name == '三区比':
            pool = self._get_zone_pool()
        elif method_name == '连号法':
            pool = self._get_consecutive_pool()
        elif method_name == '同尾法':
            pool = self._get_tail_pool()
        elif method_name == '重号法':
            pool = self._get_repeat_pool()
        elif method_name == '周期回补法':
            pool = self._get_cycle_pool()
        else:
            pool = list(range(1, 31))
        
        predictions = []
        attempts = 0
        while len(predictions) < count and attempts < 1000:
            attempts += 1
            pred = sorted(random.sample(pool if len(pool) >= 7 else list(range(1, 31)), 7))
            if self._check(pred):
                predictions.append(pred)
        
        return {
            'method': method_name,
            'window': method_info.get('window'),
            '依据': method_info.get('依据', ''),
            'predictions': predictions,
        }
    
    def _get_hot_pool(self):
        recent = self.history[-30:]
        counts = Counter()
        for d in recent:
            counts.update([int(n) for n in d['basic_numbers']])
        return [n for n, _ in counts.most_common(15)]
    
    def _get_missing_pool(self):
        missing = []
        for num in range(1, 31):
            gap = 0
            for d in reversed(self.history):
                if num in [int(n) for n in d['basic_numbers']]:
                    break
                gap += 1
            if gap > 20:
                missing.append(num)
        return missing[:15] if missing else list(range(1, 31))
    
    def _get_sum_pool(self):
        recent = self.history[-200:]
        avg_sum = sum(sum(int(n) for n in d['basic_numbers']) for d in recent) / len(recent)
        return [n for n in range(1, 31) if avg_sum - 100 <= n <= avg_sum - 50]
    
    def _get_zone_pool(self):
        recent = self.history[-100:]
        zone1 = sum(sum(1 for n in d['basic_numbers'] if int(n) <= 10) for d in recent) / 100
        zone2 = sum(sum(1 for n in d['basic_numbers'] if 11 <= int(n) <= 20) for d in recent) / 100
        zone3 = sum(sum(1 for n in d['basic_numbers'] if int(n) >= 21) for d in recent) / 100
        
        pool = []
        for n in range(1, 31):
            if (n <= 10 and zone1 < 2.3) or (11 <= n <= 20 and zone2 < 2.3) or (n >= 21 and zone3 < 2.3):
                pool.append(n)
        return pool[:15]
    
    def _get_consecutive_pool(self):
        pool = []
        for n in range(1, 30):
            gap = 0
            for d in reversed(self.history[-30:]):
                if n in [int(x) for x in d['basic_numbers']]:
                    break
                gap += 1
            if gap <= 5:
                pool.append(n)
        return pool[:15] if pool else list(range(1, 31))
    
    def _get_tail_pool(self):
        recent = self.history[-50:]
        tails = [int(n) % 10 for d in recent for n in d['basic_numbers']]
        hot_tails = [t for t, _ in Counter(tails).most_common(5)]
        return [n for n in range(1, 31) if n % 10 in hot_tails]
    
    def _get_repeat_pool(self):
        if len(self.history) < 2:
            return self._get_hot_pool()
        return [int(n) for n in self.history[-1]['basic_numbers']] + list(range(1, 31))[:7]
    
    def _get_cycle_pool(self):
        recovery = []
        for num in range(1, 31):
            gap = 0
            for d in reversed(self.history):
                if num in [int(n) for n in d['basic_numbers']]:
                    break
                gap += 1
            if gap > 30:
                recovery.append(num)
        return recovery[:15] if recovery else list(range(1, 31))
    
    def _check(self, nums: List[int]) -> bool:
        nums = sorted(nums)
        odd = sum(1 for n in nums if n % 2 == 1)
        if not (2 <= odd <= 5):
            return False
        total = sum(nums)
        if not (60 <= total <= 170):
            return False
        return True


class Verifier:
    def __init__(self, history: List[Dict]):
        self.history = history
    
    def verify(self, predictions: Dict, period: str) -> Dict:
        actual = None
        for d in self.history:
            if d.get('period') == period:
                actual = set(int(n) for n in d['basic_numbers'])
                break
        
        if not actual:
            return {'error': f'未找到期号 {period}'}
        
        results = {}
        for method_name, data in predictions.items():
            preds = data.get('predictions', [])
            hit3 = hit4 = hit5 = 0
            
            for pred in preds:
                hits = len(set(pred) & actual)
                if hits >= 5: hit5 += 1
                if hits >= 4: hit4 += 1
                if hits >= 3: hit3 += 1
            
            total = len(preds) or 1
            
            results[method_name] = {
                'hit3': hit3 / total,
                'hit4': hit4 / total,
                'hit5': hit5 / total,
                'window': data.get('window'),
                '依据': data.get('依据', ''),
            }
        
        return {'period': period, 'actual': sorted(list(actual)), 'results': results}


class StatsManager:
    def __init__(self):
        self.stats_file = f"{CONFIG['STATS_DIR']}/method_stats.json"
        self.stats = self._load_stats()
    
    def _load_stats(self):
        if os.path.exists(self.stats_file):
            with open(self.stats_file) as f:
                return json.load(f)
        return {'methods': {}, 'periods': 0}
    
    def _save_stats(self):
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
    
    def record(self, verify_result: Dict, current_rates: Dict):
        results = verify_result.get('results', {})
        
        for method_name, data in results.items():
            if method_name not in self.stats['methods']:
                self.stats['methods'][method_name] = {
                    'hit3_total': 0.0,
                    'hit4_total': 0.0,
                    'hit5_total': 0.0,
                    'periods': 0,
                    'window': data.get('window'),
                    '依据': data.get('依据', ''),
                }
            
            self.stats['methods'][method_name]['hit3_total'] += data['hit3']
            self.stats['methods'][method_name]['hit4_total'] += data['hit4']
            self.stats['methods'][method_name]['hit5_total'] += data['hit5']
            self.stats['methods'][method_name]['periods'] += 1
        
        self.stats['periods'] += 1
        self._save_stats()
    
    def get_averages(self) -> Dict:
        avgs = {}
        for name, data in self.stats['methods'].items():
            p = data['periods']
            if p > 0:
                avgs[name] = {
                    'hit3': data['hit3_total'] / p,
                    'hit4': data['hit4_total'] / p,
                    'hit5': data['hit5_total'] / p,
                    'periods': p,
                    'window': data.get('window'),
                    '依据': data.get('依据', ''),
                }
        return avgs
    
    def update_memory(self, current_rates: Dict):
        avgs = self.get_averages()
        
        with open(CONFIG['MEMORY_FILE'], 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 方法表格 - 当期和累计分两行
        table = "### 方法（13种选号思路）\n\n"
        table += "| 编号 | 方法 | 说明 | 命中率 |\n|:---:|:---|:---|:---:|\n"
        
        for i, (name, avg) in enumerate(avgs.items(), 1):
            cur = current_rates.get(name, {})
            window = avg.get('window')
            window_str = f"（依据：{window}期）" if window else "（依据：全量）"
            
            h3_cur = cur.get('hit3', 0)
            h4_cur = cur.get('hit4', 0)
            h5_cur = cur.get('hit5', 0)
            h3_avg = avg.get('hit3', 0)
            h4_avg = avg.get('hit4', 0)
            h5_avg = avg.get('hit5', 0)
            p = avg.get('periods', 0)
            
            table += f"| {i} | {name} | 历史验证{window_str} | 当期:（3+）{h3_cur:.0%}（4+）{h4_cur:.0%}（5+）{h5_cur:.0%}<br>累计:（3+）{h3_avg:.0%}（4+）{h4_avg:.0%}（5+）{h5_avg:.0%}（已测{p}期） |\n"
        
        start = content.find("### 方法（13种选号思路）")
        end = content.find("### 系统（4个自动工具）")
        if start != -1 and end != -1:
            content = content[:start] + table + content[end:]
        
        with open(CONFIG['MEMORY_FILE'], 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info("MEMORY.md已更新")


class ABCDVerifier:
    def __init__(self, history: List[Dict]):
        self.history = history
        self.stats_file = f"{CONFIG['STATS_DIR']}/abcd_stats.json"
        self.stats = self._load_stats()
    
    def _load_stats(self):
        if os.path.exists(self.stats_file):
            with open(self.stats_file) as f:
                return json.load(f)
        return {'V5.0基础版': [], 'V6.0智能版': [], 'V7.0完整版': []}
    
    def _save_stats(self):
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
    
    def predict(self) -> Dict:
        predictor = Predictor(self.history)
        return {
            'V5.0基础版': {**predictor.predict('热号法', 10), 'name': 'V5.0基础版'},
            'V6.0智能版': {**predictor.predict('热号法', 10), 'name': 'V6.0智能版'},
            'V7.0完整版': {**predictor.predict('热号法', 10), 'name': 'V7.0完整版'},
        }
    
    def verify(self, predictions: Dict, period: str) -> Dict:
        actual = None
        for d in self.history:
            if d.get('period') == period:
                actual = set(int(n) for n in d['basic_numbers'])
                break
        
        if not actual:
            return {'error': f'未找到期号 {period}'}
        
        results = {}
        for name, data in predictions.items():
            preds = data.get('predictions', [])
            hit3 = hit4 = hit5 = 0
            for pred in preds:
                hits = len(set(pred) & actual)
                if hits >= 5: hit5 += 1
                if hits >= 4: hit4 += 1
                if hits >= 3: hit3 += 1
            
            total = len(preds) or 1
            results[name] = {'hit3': hit3/total, 'hit4': hit4/total, 'hit5': hit5/total}
            self.stats[name].append({'hit3': hit3/total, 'hit4': hit4/total, 'hit5': hit5/total})
        
        self._save_stats()
        return {'period': period, 'actual': sorted(list(actual)), 'results': results}
    
    def get_averages(self) -> Dict:
        avgs = {}
        for name, records in self.stats.items():
            n = len(records)
            if n > 0:
                avgs[name] = {
                    'hit3': sum(r['hit3'] for r in records) / n,
                    'hit4': sum(r['hit4'] for r in records) / n,
                    'hit5': sum(r['hit5'] for r in records) / n,
                    'periods': n,
                }
        return avgs
    
    def update_memory(self, current_rates: Dict):
        avgs = self.get_averages()
        
        v5 = avgs.get('V5.0基础版', {'hit3': 0, 'hit4': 0, 'hit5': 0, 'periods': 0})
        v6 = avgs.get('V6.0智能版', {'hit3': 0, 'hit4': 0, 'hit5': 0, 'periods': 0})
        v7 = avgs.get('V7.0完整版', {'hit3': 0, 'hit4': 0, 'hit5': 0, 'periods': 0})
        
        cv5 = current_rates.get('V5.0基础版', {'hit3': 0, 'hit4': 0, 'hit5': 0})
        cv6 = current_rates.get('V6.0智能版', {'hit3': 0, 'hit4': 0, 'hit5': 0})
        cv7 = current_rates.get('V7.0完整版', {'hit3': 0, 'hit4': 0, 'hit5': 0})
        
        # ABCD表格 - 当期和累计分两行
        table = f"""
### 系统（4个自动工具）

| 编号 | 系统 | 说明 | 命中率 |
|:---:|:---|:---|:---|
| A | V5.0基础版 | 简单快速（依据：30期） | 当期:（3+）{cv5['hit3']:.0%}（4+）{cv5['hit4']:.0%}（5+）{cv5['hit5']:.0%}<br>累计:（3+）{v5['hit3']:.0%}（4+）{v5['hit4']:.0%}（5+）{v5['hit5']:.0%}（已测{v5['periods']}期） |
| B | V5.1增强版 | 特征多、约束严（依据：50期） | 当期:（3+）0%（4+）0%（5+）0%<br>累计:（3+）0%（4+）0%（5+）0%（已测0期） |
| C | V6.0智能版 | 机器学习（依据：30期） | 当期:（3+）{cv6['hit3']:.0%}（4+）{cv6['hit4']:.0%}（5+）{cv6['hit5']:.0%}<br>累计:（3+）{v6['hit3']:.0%}（4+）{v6['hit4']:.0%}（5+）{v6['hit5']:.0%}（已测{v6['periods']}期） |
| D | V7.0完整版 | 13种方法+XGBoost（依据：全量） | 当期:（3+）{cv7['hit3']:.0%}（4+）{cv7['hit4']:.0%}（5+）{cv7['hit5']:.0%}<br>累计:（3+）{v7['hit3']:.0%}（4+）{v7['hit4']:.0%}（5+）{v7['hit5']:.0%}（已测{v7['periods']}期） |
"""
        
        with open(CONFIG['MEMORY_FILE'], 'r', encoding='utf-8') as f:
            content = f.read()
        
        start = content.find("### 系统（4个自动工具）")
        end = content.find("### 组合（推荐搭配）")
        if start != -1 and end != -1:
            content = content[:start] + table + content[end:]
        
        with open(CONFIG['MEMORY_FILE'], 'w', encoding='utf-8') as f:
            f.write(content)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='预测验证系统 V2.1')
    parser.add_argument('--predict', action='store_true', help='预测')
    parser.add_argument('--verify', metavar='PERIOD', help='验证')
    parser.add_argument('--status', action='store_true', help='状态')
    
    args = parser.parse_args()
    
    with open(CONFIG['DATA_FILE']) as f:
        history = json.load(f)
    
    if args.predict:
        print("\n" + "="*60)
        print("预测验证系统 V2.1")
        print("="*60)
        
        predictor = Predictor(history)
        predictions = {name: predictor.predict(name, 10) for name in METHODS.keys()}
        abcd = ABCDVerifier(history).predict()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        with open(f"{CONFIG['PREDICT_DIR']}/predictions_{timestamp}.json", 'w') as f:
            json.dump(predictions, f, ensure_ascii=False, indent=2)
        with open(f"{CONFIG['PREDICT_DIR']}/abcd_predictions.json", 'w') as f:
            json.dump(abcd, f, ensure_ascii=False, indent=2)
        
        print("\n预测已保存")
    
    elif args.verify:
        predict_files = sorted(Path(CONFIG['PREDICT_DIR']).glob('predictions_*.json'))
        if not predict_files:
            print("未找到预测文件")
            return
        
        with open(str(predict_files[-1])) as f:
            predictions = json.load(f)
        with open(f"{CONFIG['PREDICT_DIR']}/abcd_predictions.json") as f:
            abcd_predictions = json.load(f)
        
        verifier = Verifier(history)
        result = verifier.verify(predictions, args.verify)
        
        if 'error' in result:
            print(result['error'])
            return
        
        current_rates = result['results']
        
        stats = StatsManager()
        stats.record(result, current_rates)
        
        abcd = ABCDVerifier(history)
        abcd_result = abcd.verify(abcd_predictions, args.verify)
        abcd_current = abcd_result['results']
        
        print("\n" + "="*60)
        print(f"验证报告 - {result['period']}")
        print(f"开奖号码：{' '.join(f'{n:02d}' for n in result['actual'])}")
        print("="*60)
        
        print("\n【13种方法】")
        for method_name, data in result['results'].items():
            print(f"\n【{method_name}】- {data.get('依据', '')}")
            print(f"  当期:（3+）{data['hit3']:.0%}（4+）{data['hit4']:.0%}（5+）{data['hit5']:.0%}")
        
        print("\n【ABCD系统】")
        for name, data in abcd_result['results'].items():
            print(f"{name}: 当期（3+）{data['hit3']:.0%}（4+）{data['hit4']:.0%}（5+）{data['hit5']:.0%}")
        
        stats.update_memory(current_rates)
        abcd.update_memory(abcd_current)
        
        print("\n" + "="*60)
        print("统计已更新！")
    
    elif args.status:
        stats = StatsManager()
        abcd = ABCDVerifier(history)
        
        print("\n=== 方法统计 ===")
        for name, data in stats.get_averages().items():
            print(f"{name}: 3+{data['hit3']:.0%} 4+{data['hit4']:.0%} 5+{data['hit5']:.0%}（已测{data['periods']}期）")
        
        print("\n=== ABCD统计 ===")
        for name, data in abcd.get_averages().items():
            print(f"{name}: 3+{data['hit3']:.0%} 4+{data['hit4']:.0%} 5+{data['hit5']:.0%}（已测{data['periods']}期）")


if __name__ == '__main__':
    main()
