#!/usr/bin/env python3
"""
生成预测帮助文档
包含每个方法的当前预测情况、命中率统计
"""

import json
import os
from datetime import datetime

# 配置
STATS_FILE = '/home/lang/.openclaw/workspace/caipiao/v5_platform/stats/method_stats.json'
PRED_FILE = '/home/lang/.openclaw/workspace/caipiao/v5_platform/output/predictions_latest.csv'
OUTPUT_FILE = '/home/lang/.openclaw/workspace/caipiao/v5_platform/预测帮助.md'

# 13种预测方法详情
METHODS_DETAIL = {
    '遗漏值法': {
        '依据': '遗漏值>20期优先',
        '说明': '号码遗漏超过20期未出时，优先选入',
        '窗口': '全量数据'
    },
    '热号法': {
        '依据': '30期内出现≥10次',
        '说明': '统计最近30期出现次数，热号优先',
        '窗口': '30期'
    },
    '大小号法': {
        '依据': '小区:01-10 / 中区:11-20 / 大区:21-30',
        '说明': '三个区间号码分布均衡',
        '窗口': '50期'
    },
    '奇偶法': {
        '依据': '奇偶比例3-4个',
        '说明': '奇数控制在3-4个',
        '窗口': '50期'
    },
    '和值法': {
        '依据': '历史平均和值105±20',
        '说明': '7个号码之和在85-125之间',
        '窗口': '200期'
    },
    '三区比': {
        '依据': '01-10 / 11-20 / 21-30分布均衡',
        '说明': '三个小区各出2-3个',
        '窗口': '100期'
    },
    '012路法': {
        '依据': '除3余0/1/2各2-3个',
        '说明': '0路、1路、2路号码各2-3个',
        '窗口': '100期'
    },
    '连号法': {
        '依据': '每期1-2组连号',
        '说明': '预测包含1-2组连续号码',
        '窗口': '30期'
    },
    '同尾法': {
        '依据': '尾数重复概率',
        '说明': '2-3个号码尾数相同',
        '窗口': '50期'
    },
    '重号法': {
        '依据': '与上期重复2-3个',
        '说明': '与上一期号码重复2-3个',
        '窗口': '30期'
    },
    'AC值法': {
        '依据': 'AC值10-12为佳',
        '说明': '号码组合复杂度适中',
        '窗口': '50期'
    },
    '极距法': {
        '依据': '极距18-22',
        '说明': '最大号-最小号=18-22',
        '窗口': '100期'
    },
    '周期回补法': {
        '依据': '周期性遗漏回补',
        '说明': '遗漏到均值的号码优先',
        '窗口': '全量'
    }
}


def load_stats():
    """加载统计数据"""
    try:
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {'methods': {}}


def load_predictions():
    """加载预测结果"""
    try:
        with open(PRED_FILE, 'r') as f:
            lines = f.readlines()
            predictions = []
            for line in lines[1:11]:  # 前10组
                parts = line.strip().split(',')
                if len(parts) >= 8:
                    nums = [int(x) for x in parts[1:8]]
                    predictions.append(nums)
            return predictions
    except:
        return []


def calculate_hit_rate(total, periods):
    """计算命中率"""
    if periods == 0:
        return 0
    return total / periods


def generate_help():
    """生成帮助文档"""
    stats = load_stats()
    predictions = load_predictions()
    methods_data = stats.get('methods', {})
    periods = stats.get('periods', 0)
    
    doc = []
    doc.append("# 七乐彩预测帮助\n")
    doc.append(f"---\n")
    doc.append(f"**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    doc.append(f"**数据依据**: 全量2898期\n")
    doc.append(f"**验证期数**: 最近{periods}期\n")
    doc.append(f"\n---\n")
    
    # 总体说明
    doc.append("## 📖 使用说明\n")
    doc.append("""
1. 每种方法独立预测，各给出10组号码
2. 选择方法时，建议组合使用（1+2或1+2+3）
3. 历史命中率越高，可信度越高
4. 当前预测结果仅供参考，理性购彩

---
""")
    
    # 预测结果
    if predictions:
        doc.append("## 🎯 当前预测（V7.1智能版）\n")
        doc.append(f"**期号**: 第2026018期\n")
        doc.append(f"**预测时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        doc.append(f"**预测组数**: 100组\n\n")
        doc.append("**精选5组**:\n")
        for i, pred in enumerate(predictions[:5], 1):
            doc.append(f"  {i}. {' '.join(f'{n:02d}' for n in pred)}\n")
        doc.append("\n---\n")
    
    # 方法列表
    doc.append("## 🔧 预测方法详解\n\n")
    
    # 按命中率排序
    sorted_methods = []
    for name, detail in METHODS_DETAIL.items():
        method_stats = methods_data.get(name, {})
        hit3_total = method_stats.get('hit3_total', 0)
        method_periods = method_stats.get('periods', 0)
        hit3_rate = calculate_hit_rate(hit3_total, method_periods) if method_periods > 0 else 0
        sorted_methods.append((name, detail, hit3_rate, method_periods))
    
    sorted_methods.sort(key=lambda x: x[2], reverse=True)
    
    for name, detail, hit3_rate, method_periods in sorted_methods:
        method_stats = methods_data.get(name, {})
        
        doc.append(f"### {name}\n\n")
        doc.append(f"- **依据**: {detail['依据']}\n")
        doc.append(f"- **说明**: {detail['说明']}\n")
        doc.append(f"- **数据窗口**: {detail['窗口']}\n\n")
        
        doc.append("**命中率统计**:\n")
        hit3 = calculate_hit_rate(method_stats.get('hit3_total', 0), method_periods) * 100
        hit4 = calculate_hit_rate(method_stats.get('hit4_total', 0), method_periods) * 100
        hit5 = calculate_hit_rate(method_stats.get('hit5_total', 0), method_periods) * 100
        
        doc.append(f"| 指标 | 数值 |\n")
        doc.append(f"|:---:|:---:|\n")
        doc.append(f"| 已测期数 | {method_periods}期 |\n")
        doc.append(f"| **3+命中率** | **{hit3:.0f}%** |\n")
        doc.append(f"| 4+命中率 | {hit4:.0f}% |\n")
        doc.append(f"| 5+命中率 | {hit5:.0f}% |\n\n")
        
        # 如果有预测，显示
        if predictions:
            doc.append("**当前预测示例**:\n")
            doc.append("```\n")
            doc.append("  (每次预测不同，请运行获取)\n")
            doc.append("```\n")
        
        doc.append("---\n\n")
    
    # 推荐组合
    doc.append("## 💡 推荐组合\n\n")
    doc.append("""
| 组合 | 说明 | 适用场景 |
|:---|:---|:---|
| 1+2 | 遗漏+热号 | 日常预测 |
| 1+2+3 | 综合预测 | 追求稳定性 |
| 6+10 | 三区比+重号 | 高命中率 |
| 全部组合 | 多方法交叉 | 综合分析 |

---
""")
    
    # 命中率排名
    doc.append("## 📊 命中率排名\n\n")
    doc.append("| 排名 | 方法 | 3+命中 | 4+命中 | 5+命中 |\n")
    doc.append("|:---:|:---|:---:|:---:|:---:|\n")
    
    for i, (name, _, hit3_rate, periods) in enumerate(sorted_methods[:10], 1):
        method_stats = methods_data.get(name, {})
        hit3 = calculate_hit_rate(method_stats.get('hit3_total', 0), periods) * 100
        hit4 = calculate_hit_rate(method_stats.get('hit4_total', 0), periods) * 100
        hit5 = calculate_hit_rate(method_stats.get('hit5_total', 0), periods) * 100
        
        emoji = '🥇' if i == 1 else ('🥈' if i == 2 else ('🥉' if i == 3 else f'{i}.'))
        doc.append(f"| {emoji} | {name} | {hit3:.0f}% | {hit4:.0f}% | {hit5:.0f}% |\n")
    
    doc.append("\n---\n")
    doc.append("*以上数据仅供参考，请理性购彩*\n")
    
    # 写入文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(''.join(doc))
    
    print(f"✅ 帮助文档已生成: {OUTPUT_FILE}")
    return ''.join(doc)


if __name__ == '__main__':
    generate_help()
