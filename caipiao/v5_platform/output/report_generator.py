#!/usr/bin/env python3
"""报告生成器"""

import json
from datetime import datetime
from typing import Dict, List

class ReportGenerator:
    """报告生成器"""
    
    def __init__(self):
        self.history = []
    
    def load_history(self, filepath: str = '/home/lang/.openclaw/workspace/caipiao/qlc_history_full.json'):
        """加载历史数据"""
        try:
            with open(filepath, 'r') as f:
                self.history = json.load(f)
            return True
        except:
            return False
    
    def generate_daily_report(self) -> str:
        """生成每日报告"""
        if not self.history:
            return "❌ 没有历史数据"
        
        recent = self.history[-10:]
        
        # 统计数据
        from collections import Counter
        all_nums = []
        for d in recent:
            all_nums.extend([int(n) for n in d['basic_numbers']])
        
        freq = Counter(all_nums)
        hot = freq.most_common(10)
        cold = [n for n in range(1, 31) if n not in dict(freq)]
        
        # 遗漏值
        missing = {}
        for num in range(1, 31):
            for i, d in enumerate(reversed(recent)):
                if num in [int(n) for n in d['basic_numbers']]:
                    missing[num] = i
                    break
            else:
                missing[num] = 10
        
        high_missing = sorted(missing.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # 生成报告
        report = f"""
七乐彩每日分析报告
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
最新期号: {recent[0]['period']} ({recent[0]['date']})

一、基础统计
━━━━━━━━━━━━━━
分析期数: {len(recent)}期
数据总量: {len(self.history)}条

二、热号TOP10
━━━━━━━━━━━━━━
"""
        
        for i, (num, count) in enumerate(hot, 1):
            report += f"{i:2d}. {num:02d}号: 出现{count}次\n"
        
        report += f"""
三、高遗漏号码
━━━━━━━━━━━━━━
"""
        
        for num, gap in high_missing:
            report += f"  {num:02d}号: 已遗漏{gap}期\n"
        
        report += """
四、分布规律
━━━━━━━━━━━━━━
"""
        
        # 奇偶分布
        odd_counts = [sum(1 for n in d['basic_numbers'] if int(n) % 2 == 1) for d in recent]
        most_common_odd = Counter(odd_counts).most_common(1)[0][0]
        report += f"奇偶分布: {most_common_odd}奇{7-most_common_odd}偶\n"
        
        # 大小分布
        small_counts = [sum(1 for n in d['basic_numbers'] if int(n) <= 10) for d in recent]
        most_common_small = Counter(small_counts).most_common(1)[0][0]
        medium_counts = [sum(1 for n in d['basic_numbers'] if 11 <= int(n) <= 20) for d in recent]
        most_common_medium = Counter(medium_counts).most_common(1)[0][0]
        large_counts = [sum(1 for n in d['basic_numbers'] if int(n) >= 21) for d in recent]
        most_common_large = Counter(large_counts).most_common(1)[0][0]
        report += f"大小分布: {most_common_small}-{most_common_medium}-{most_common_large}\n"
        
        report += """
五、策略建议
━━━━━━━━━━━━━━
1. 关注热号: 优先选择近期频繁出现的号码
2. 留意回补: 高遗漏号码可能有回补趋势
3. 分布均衡: 遵循奇偶和大小分布规律
4. 组合策略: 参考常见组合提高命中概率

---
七乐彩预测平台 V5.0
"""
        
        return report
    
    def save_report(self, report: str, filepath: str = None):
        """保存报告"""
        if not filepath:
            filepath = f"/home/lang/.openclaw/workspace/caipiao/v5_platform/logs/report_{datetime.now().strftime('%Y%m%d')}.txt"
        
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
    print("报告生成器测试")
    print("=" * 60)
    
    generator = ReportGenerator()
    
    if not generator.load_history():
        print("❌ 加载历史数据失败")
        return False
    
    report = generator.generate_daily_report()
    
    print(report)
    
    return generator.save_report(report)

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
