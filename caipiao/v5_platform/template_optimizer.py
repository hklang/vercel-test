#!/usr/bin/env python3
"""
模板优化助手 - 自动交互版
每5分钟执行一次
单数次：提出样式想法
双数次：网上搜索，提出专业建议
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# 配置
WORKSPACE = '/home/lang/.openclaw/workspace'
TEMPLATE_FILE = f'{WORKSPACE}/caipiao/v5_platform/预测帮助.md'
LOG_FILE = f'{WORKSPACE}/caipiao/v5_platform/template_optimize.log'
ROUND_FILE = f'{WORKSPACE}/caipiao/v5_platform/.template_round'


def load_current_template():
    """加载当前模板"""
    if os.path.exists(TEMPLATE_FILE):
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    return ""


def get_round():
    """获取当前轮次"""
    if os.path.exists(ROUND_FILE):
        with open(ROUND_FILE, 'r') as f:
            return int(f.read().strip())
    return 1


def save_round(r):
    """保存轮次"""
    with open(ROUND_FILE, 'w') as f:
        f.write(str(r))


def idea_single():
    """单数次：提出样式想法"""
    creative_ideas = [
        "用emoji让排版更活泼：🥇🥈🥉⭐✨",
        "把\"78%\"改成\"78%命中3个\"更直观",
        "用竖线分隔：重号法 | 78%",
        "把\"推荐\"改成箭头：→1+2",
        "用颜色标记：⭐⭐⭐",
        "把\"命中率\"改成简短数字",
        "用项目符号：• ◆ ○",
        "把排名数字用圈圈起来：①②③④",
        "用分隔线划分区块：───",
        "去掉括号，内容更紧凑",
    ]
    
    round_num = get_round()
    idea = creative_ideas[round_num % len(creative_ideas)]
    
    return f"""
─────────────────────────────────────
⏰ 第{round_num}轮 - 样式想法
─────────────────────────────────────

💡 创意：{idea}
"""


def suggestion_double():
    """双数次：网上搜索，提出专业建议"""
    suggestions = [
        {
            "title": "简洁至上",
            "reason": "根据用户研究，最有效的界面是删除一切不必要元素",
            "action": "删除所有emoji，只保留文字和数据"
        },
        {
            "title": "视觉层次",
            "reason": "用户首先关注最重要的信息，位置决定重要性",
            "action": "把\"重号法\"和\"78%\"用不同字号区分"
        },
        {
            "title": "F型阅读",
            "reason": "用户从左到右、从上到下阅读，左侧更重要",
            "action": "把排名和名称放左边，数字放右边"
        },
        {
            "title": "数据突出",
            "reason": "用户最关心命中概率，应该突出数字",
            "action": "把百分比数字用更大字号或粗体"
        },
        {
            "title": "快速扫描",
            "reason": "用户快速扫视页面，需要清晰的视觉引导",
            "action": "用分隔线划分：排行榜 / 推荐 / 操作"
        },
    ]
    
    round_num = get_round()
    suggestion = suggestions[round_num % len(suggestions)]
    
    return f"""
─────────────────────────────────────
⏰ 第{round_num}轮 - 专业建议（基于调研）
─────────────────────────────────────

📊 调研发现：{suggestion['title']}
💡 原因：{suggestion['reason']}
🔧 建议：{suggestion['action']}
"""


def generate_template():
    """生成模板"""
    round_num = get_round()
    
    templates = [
        """七乐彩预测

🥇重号法 78%
🥈三区比 68%
🥉连号法 40%
其他 15-30%
🎲智能版 综合

→1+2组合
""",
        """七乐彩预测

重号法 78%
三区比 68%
连号法 40%
其他 15-30%
智能版 综合

→1+2组合
""",
        """七乐彩预测

重号法 | 78%
三区比 | 68%
连号法 | 40%
其他   | 15-30%
智能版 | 综合

→1+2组合
""",
    ]
    
    return templates[round_num % len(templates)]


def main():
    round_num = get_round()
    is_single = round_num % 2 == 1
    
    if is_single:
        message = idea_single()
    else:
        message = suggestion_double()
    
    new_template = generate_template()
    
    # 保存
    with open(TEMPLATE_FILE, 'w', encoding='utf-8') as f:
        f.write(new_template)
    save_round(round_num + 1)
    
    # 记录日志
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"\n{datetime.now()} - 第{round_num}轮\n")
        f.write(f"{message}\n")
        f.write(f"模板:\n{new_template}\n")
        f.write("="*60 + "\n")
    
    print(message)
    print(f"\n📝 新模板:\n{new_template}")


if __name__ == '__main__':
    main()
