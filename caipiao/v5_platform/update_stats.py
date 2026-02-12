#!/usr/bin/env python3
"""
预测验证系统 - 统计修复版
=========================
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
import logging

CONFIG = {
    'DATA_FILE': '/home/lang/.openclaw/workspace/caipiao/qlc_history_full.json',
    'PREDICT_DIR': '/home/lang/.openclaw/workspace/caipiao/v5_platform/predictions',
    'RESULTS_DIR': '/home/lang/.openclaw/workspace/caipiao/v5_platform/results',
    'STATS_DIR': '/home/lang/.openclaw/workspace/caipiao/v5_platform/stats',
    'MEMORY_FILE': '/home/lang/.openclaw/workspace/MEMORY.md',
}

os.makedirs(CONFIG['STATS_DIR'], exist_ok=True)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class StatsManager:
    """统计管理器"""
    
    def __init__(self):
        self.method_stats_file = f"{CONFIG['STATS_DIR']}/method_stats.json"
        self.abcd_stats_file = f"{CONFIG['STATS_DIR']}/abcd_stats.json"
        self.load_stats()
    
    def load_stats(self):
        if os.path.exists(self.method_stats_file):
            with open(self.method_stats_file) as f:
                self.method_stats = json.load(f)
        else:
            self.method_stats = {'methods': {}, 'total_periods': 0}
        
        if os.path.exists(self.abcd_stats_file):
            with open(self.abcd_stats_file) as f:
                self.abcd_stats = json.load(f)
        else:
            self.abcd_stats = {'V5.0基础版': [], 'V6.0智能版': [], 'V7.0完整版': []}
    
    def save_stats(self):
        with open(self.method_stats_file, 'w') as f:
            json.dump(self.method_stats, f, indent=2)
        with open(self.abcd_stats_file, 'w') as f:
            json.dump(self.abcd_stats, f, indent=2)
    
    def record_method_result(self, results: Dict):
        """记录方法结果（按期数）"""
        for method_name, data in results.items():
            if method_name not in self.method_stats['methods']:
                self.method_stats['methods'][method_name] = {
                    'hit3_total': 0, 'hit4_total': 0, 'hit5_total': 0,
                    'periods': 0, '依据': data.get('依据', ''),
                }
            
            self.method_stats['methods'][method_name]['hit3_total'] += data['hit3'] * data['total']
            self.method_stats['methods'][method_name]['hit4_total'] += data['hit4'] * data['total']
            self.method_stats['methods'][method_name]['hit5_total'] += data['hit5'] * data['total']
            self.method_stats['methods'][method_name]['periods'] += 1
        
        self.method_stats['total_periods'] += 1
        self.save_stats()
    
    def record_abcd_result(self, results: Dict):
        """记录ABCD结果（按期数）"""
        for name, data in results.items():
            self.abcd_stats[name].append({
                'hit3': data['hit3'],
                'hit4': data['hit4'],
                'hit5': data['hit5'],
            })
        self.save_stats()
    
    def get_method_averages(self) -> Dict:
        """计算方法平均命中率"""
        averages = {}
        for name, data in self.method_stats['methods'].items():
            periods = data['periods']
            if periods > 0:
                averages[name] = {
                    'hit3': data['hit3_total'] / periods,
                    'hit4': data['hit4_total'] / periods,
                    'hit5': data['hit5_total'] / periods,
                    'periods': periods,
                    '依据': data.get('依据', ''),
                }
        return averages
    
    def get_abcd_averages(self) -> Dict:
        """计算ABCD平均命中率"""
        averages = {}
        for name, records in self.abcd_stats.items():
            n = len(records)
            if n > 0:
                averages[name] = {
                    'hit3': sum(r['hit3'] for r in records) / n,
                    'hit4': sum(r['hit4'] for r in records) / n,
                    'hit5': sum(r['hit5'] for r in records) / n,
                    'periods': n,
                }
        return averages
    
    def update_memory(self):
        """更新MEMORY.md"""
        method_avgs = self.get_method_averages()
        abcd_avgs = self.get_abcd_averages()
        
        with open(CONFIG['MEMORY_FILE'], 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 方法表格
        methods_table = "### 方法（13种选号思路）\n\n| 编号 | 方法 | 说明 | 命中率 |\n|:---:|:---|:---|:---:|\n"
        
        for i, (name, data) in enumerate(method_avgs.items(), 1):
            h3 = data['hit3']
            h4 = data['hit4']
            h5 = data['hit5']
            p = data['periods']
            methods_table += f"| {i} | {name} | 历史验证 | （3+）{h3:.0%}（4+）{h4:.0%}（5+）{h5:.0%}（已测{p}期） |\n"
        
        # 替换方法表格
        start = content.find("### 方法（13种选号思路）")
        end = content.find("### 系统（4个自动工具）")
        if start != -1 and end != -1:
            content = content[:start] + methods_table + content[end:]
        
        # ABCD表格
        v5 = abcd_avgs.get('V5.0基础版', {'hit3': 0, 'hit4': 0, 'hit5': 0, 'periods': 0})
        v6 = abcd_avgs.get('V6.0智能版', {'hit3': 0, 'hit4': 0, 'hit5': 0, 'periods': 0})
        v7 = abcd_avgs.get('V7.0完整版', {'hit3': 0, 'hit4': 0, 'hit5': 0, 'periods': 0})
        
        abcd_table = f"""
### 系统（4个自动工具）

| 编号 | 系统 | 说明 | 命中率 |
|:---:|:---|:---|:---|
| A | V5.0基础版 | 简单快速 | （3+）{v5['hit3']:.0%}（4+）{v5['hit4']:.0%}（5+）{v5['hit5']:.0%}（已测{v5['periods']}期） |
| B | V5.1增强版 | 特征多、约束严 | （3+）0%（4+）0%（5+）0%（已测0期） |
| C | V6.0智能版 | 机器学习 | （3+）{v6['hit3']:.0%}（4+）{v6['hit4']:.0%}（5+）{v6['hit5']:.0%}（已测{v6['periods']}期） |
| D | V7.0完整版 | 13种方法+XGBoost | （3+）{v7['hit3']:.0%}（4+）{v7['hit4']:.0%}（5+）{v7['hit5']:.0%}（已测{v7['periods']}期） |
"""
        
        # 替换ABCD表格
        start = content.find("### 系统（4个自动工具）")
        end = content.find("### 组合（推荐搭配）")
        if start != -1 and end != -1:
            content = content[:start] + abcd_table + content[end:]
        
        with open(CONFIG['MEMORY_FILE'], 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("MEMORY.md已更新")


def main():
    stats = StatsManager()
    stats.update_memory()
    
    print("\n=== 方法统计 ===")
    for name, data in stats.get_method_averages().items():
        print(f"{name}: 3+{data['hit3']:.0%} 4+{data['hit4']:.0%} 5+{data['hit5']:.0%}（已测{data['periods']}期）")
    
    print("\n=== ABCD统计 ===")
    for name, data in stats.get_abcd_averages().items():
        print(f"{name}: 3+{data['hit3']:.0%} 4+{data['hit4']:.0%} 5+{data['hit5']:.0%}（已测{data['periods']}期）")


if __name__ == '__main__':
    main()
