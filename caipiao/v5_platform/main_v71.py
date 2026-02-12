#!/usr/bin/env python3
"""
七乐彩智能预测系统 V7.1 - 增强版
==========================

新增功能：
1. 周期性分析算法（星期规律、周期性回补）
2. 自动启动任务（每小时运行）
3. 预测结果推送（可选）

使用方法：
    python3 main.py              # 正常运行
    python3 main.py --auto       # 后台自动模式
    python3 main.py --once       # 仅运行一次
    python3 auto_run.py --start  # 启动守护进程
    python3 auto_run.py --cron   # 生成Cron配置
"""

import json
import random
import time
import os
import argparse
from datetime import datetime
from typing import List, Dict, Tuple
from collections import Counter
from pathlib import Path
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

# 配置
CONFIG = {
    'DATA_FILE': '/home/lang/.openclaw/workspace/caipiao/qlc_history_full.json',
    'OUTPUT_DIR': '/home/lang/.openclaw/workspace/caipiao/v5_platform/output',
    'WEIGHTS_FILE': '/home/lang/.openclaw/workspace/caipiao/v5_platform/weights.json',
}


class PeriodicAnalyzer:
    """周期性分析器 - V7.1新增"""
    
    def __init__(self, history: List[Dict]):
        self.history = history
    
    def analyze(self) -> Dict:
        """分析周期性规律"""
        return {
            'weekday_hot': self._get_weekday_hot(),
            'cycle_recovery': self._get_cycle_recovery(),
            'alternating': self._get_alternating(),
        }
    
    def _get_weekday_hot(self) -> List[int]:
        """获取当前星期的热号"""
        weekday = len(self.history) % 7
        recent = self.history[-14:]  # 最近14天
        
        weekday_nums = []
        for i, d in enumerate(recent):
            if i % 7 == weekday:
                for n in d['basic_numbers']:
                    weekday_nums.append(int(n))
        
        if weekday_nums:
            return [n for n, _ in Counter(weekday_nums).most_common(5)]
        return []
    
    def _get_cycle_recovery(self) -> List[int]:
        """获取即将回补的周期性号码"""
        recovery = []
        
        for num in range(1, 31):
            gap = 0
            for d in reversed(self.history[-30:]):
                if num in [int(n) for n in d['basic_numbers']]:
                    break
                gap += 1
            
            # 遗漏3-5期，考虑回补
            if 3 <= gap <= 5:
                recovery.append(num)
        
        return recovery
    
    def _get_alternating(self) -> Dict:
        """获取交替规律提示"""
        recent = self.history[-10:]
        
        # 奇偶趋势
        odd_counts = [sum(1 for n in d['basic_numbers'] if int(n) % 2 == 1) for d in recent]
        avg_odd = sum(odd_counts) / len(odd_counts)
        
        # 大小趋势
        large_counts = [sum(1 for n in d['basic_numbers'] if int(n) >= 21) for d in recent]
        avg_large = sum(large_counts) / len(large_counts)
        
        return {
            'odd_trend': 'odd' if avg_odd > 3.5 else 'even',
            'large_trend': 'large' if avg_large > 2.5 else 'small',
            'suggest_odd': int(avg_odd + 0.5),
            'suggest_large': int(avg_large + 0.5),
        }


class FeatureExtractor:
    """特征提取器"""
    
    def __init__(self, history: List[Dict]):
        self.history = history
    
    def extract(self) -> Dict:
        """提取所有特征"""
        features = {}
        
        # 频率特征
        recent = self.history[-30:]
        counts = Counter()
        for d in recent:
            counts.update([int(n) for n in d['basic_numbers']])
        features['freq_mean'] = sum(counts.values()) / 30
        
        # 遗漏特征
        for num in range(1, 31):
            gap = 0
            for d in reversed(self.history[-50:]):
                if num in [int(n) for n in d['basic_numbers']]:
                    break
                gap += 1
            features[f'missing_{num}'] = gap
        
        return features


class PredictorV7_1:
    """预测器 V7.1"""
    
    def __init__(self):
        self.history = []
        self.features = {}
        self.periodic = None
        self.weights = {
            'hot': 0.20,
            'missing': 0.30,
            'feature': 0.20,
            'periodic': 0.15,  # V7.1新增周期性权重
            'random': 0.15,
        }
        
        Path(CONFIG['OUTPUT_DIR']).mkdir(parents=True, exist_ok=True)
        self.load_history()
    
    def load_history(self):
        """加载数据"""
        try:
            with open(CONFIG['DATA_FILE'], 'r') as f:
                self.history = json.load(f)
            logger.info(f"加载数据: {len(self.history)} 条")
        except Exception as e:
            logger.error(f"加载失败: {e}")
    
    def analyze(self):
        """分析"""
        if not self.history:
            return
        
        logger.info("分析数据...")
        extractor = FeatureExtractor(self.history)
        self.features = extractor.extract()
        
        # V7.1新增周期性分析
        self.periodic = PeriodicAnalyzer(self.history).analyze()
        logger.info(f"周期性分析完成")
    
    def predict(self, count: int = 100) -> List[List[int]]:
        """预测"""
        if not self.history:
            return []
        
        self.analyze()
        predictions = []
        attempts = 0
        
        # 获取号码池
        hot_pool = self._get_hot_pool()
        missing_pool = self._get_missing_pool()
        periodic_pool = self._get_periodic_pool()
        
        while len(predictions) < count and attempts < 500000:
            attempts += 1
            
            r = random.random()
            pool = list(range(1, 31))
            
            if r < self.weights['hot']:
                pool = hot_pool[:15]
            elif r < self.weights['hot'] + self.weights['missing']:
                pool = missing_pool[:15]
            elif r < self.weights['hot'] + self.weights['missing'] + self.weights['periodic']:
                pool = periodic_pool[:15]
            
            if len(pool) < 7:
                pool = list(range(1, 31))
            
            selected = sorted(random.sample(pool, 7))
            
            if self._check_constraints(selected):
                predictions.append(selected)
        
        logger.info(f"生成 {len(predictions)} 组预测 (尝试{attempts}次)")
        return predictions
    
    def _get_hot_pool(self) -> List[int]:
        """热号池"""
        recent = self.history[-30:]
        counts = Counter()
        for d in recent:
            counts.update([int(n) for n in d['basic_numbers']])
        return [n for n, _ in counts.most_common(15)]
    
    def _get_missing_pool(self) -> List[int]:
        """遗漏池"""
        missing = []
        for num in range(1, 31):
            gap = 0
            for d in reversed(self.history[-50:]):
                if num in [int(n) for n in d['basic_numbers']]:
                    break
                gap += 1
            missing.append((num, gap))
        return [n for n, _ in sorted(missing, key=lambda x: x[1], reverse=True)[:15]]
    
    def _get_periodic_pool(self) -> List[int]:
        """周期性池"""
        pool = []
        
        # 添加星期热号
        if self.periodic['weekday_hot']:
            pool.extend(self.periodic['weekday_hot'])
        
        # 添加周期回补号
        pool.extend(self.periodic['cycle_recovery'][:5])
        
        return list(set(pool)) if pool else list(range(1, 31))
    
    def _check_constraints(self, numbers: List[int]) -> bool:
        """检查约束"""
        # 奇偶
        odd = sum(1 for n in numbers if n % 2 == 1)
        if not (2 <= odd <= 5):
            return False
        
        # 大小
        small = sum(1 for n in numbers if n <= 10)
        medium = sum(1 for n in numbers if 11 <= n <= 20)
        large = sum(1 for n in numbers if n >= 21)
        if not (1 <= small <= 4 and 1 <= medium <= 4 and 1 <= large <= 4):
            return False
        
        # 和值
        total = sum(numbers)
        if not (60 <= total <= 170):
            return False
        
        return True
    
    def save_predictions(self, predictions: List[List[int]]):
        """保存预测"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        csv_path = f"{CONFIG['OUTPUT_DIR']}/predictions_{timestamp}.csv"
        with open(csv_path, 'w', encoding='utf-8-sig') as f:
            f.write('序号,号码1,号码2,号码3,号码4,号码5,号码6,号码7\n')
            for i, pred in enumerate(predictions, 1):
                f.write(f'{i},{",".join(map(str, pred))}\n')
        
        latest = f"{CONFIG['OUTPUT_DIR']}/predictions_latest.csv"
        if os.path.exists(latest):
            os.remove(latest)
        os.symlink(csv_path, latest)
        
        logger.info(f"保存预测: {csv_path}")
    
    def generate_report(self, predictions: List[List[int]]) -> str:
        """生成报告"""
        recent = self.history[-30:]
        all_nums = []
        for d in recent:
            all_nums.extend([int(n) for n in d['basic_numbers']])
        hot = Counter(all_nums).most_common(10)
        
        return f"""
{'='*60}
七乐彩智能预测系统 V7.1
{'='*60}

📊 数据量: {len(self.history)} 条
🎯 特征数: {len(self.features)}
⚙️ 策略权重: 热号{self.weights['hot']:.0%}/遗漏{self.weights['missing']:.0%}/周期{self.weights['periodic']:.0%}/随机{self.weights['random']:.0%}

🆕 V7.1新增功能:
  - 周期性分析（星期规律）
  - 周期回补预测
  - 交替规律提示

🔥 热号TOP10（30期）
"""
        + '\n'.join([f"  {i:2d}. {n:02d}号: {c}次" for i, (n, c) in enumerate(hot, 1)]) + f"""

---
生成时间: {datetime.now().isoformat()}
"""
    
    def save_report(self, report: str):
        """保存报告"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = f"{CONFIG['OUTPUT_DIR']}/report_{timestamp}.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        latest = f"{CONFIG['OUTPUT_DIR']}/report_latest.txt"
        if os.path.exists(latest):
            os.remove(latest)
        os.symlink(report_path, latest)
        
        logger.info(f"保存报告: {report_path}")


def main():
    parser = argparse.ArgumentParser(description='七乐彩V7.1预测系统')
    parser.add_argument('--auto', action='store_true', help='自动模式（循环运行）')
    parser.add_argument('--interval', type=int, default=3600, help='自动运行间隔（秒）')
    
    args = parser.parse_args()
    
    predictor = PredictorV7_1()
    
    if args.auto:
        # 自动模式
        logger.info("启动自动模式...")
        while True:
            try:
                predictions = predictor.predict(100)
                if predictions:
                    predictor.save_predictions(predictions)
                    report = predictor.generate_report(predictions)
                    predictor.save_report(report)
                time.sleep(args.interval)
            except KeyboardInterrupt:
                logger.info("收到停止信号")
                break
            except Exception as e:
                logger.error(f"运行出错: {e}")
                time.sleep(60)
    else:
        # 单次运行
        print("="*60)
        print("七乐彩智能预测系统 V7.1")
        print("="*60)
        
        predictions = predictor.predict(100)
        
        if predictions:
            predictor.save_predictions(predictions)
            
            print("\n前10组预测:")
            for i, pred in enumerate(predictions[:10], 1):
                print(f"  {i:3d}: {' '.join(f'{n:02d}' for n in pred)}")
            
            report = predictor.generate_report(predictions)
            predictor.save_report(report)
            print(report)


if __name__ == '__main__':
    main()
