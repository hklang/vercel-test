#!/usr/bin/env python3
"""
优化任务 - 飞书通知
"""

import os
import sys
import json
from datetime import datetime

# 配置
STATS_FILE = '/home/lang/.openclaw/workspace/caipiao/v5_platform/stats/optimizer_stats.json'
LOG_FILE = '/home/lang/.openclaw/workspace/caipiao/v5_platform/logs/optimizer_cron.log'
FEISHU_WEBHOOK_URL = os.environ.get('FEISHU_WEBHOOK_URL', '')


def get_latest_result():
    """获取最近一次运行结果"""
    if not os.path.exists(LOG_FILE):
        return None
    
    with open(LOG_FILE, 'r') as f:
        lines = f.readlines()
    
    # 找到最近一次运行的开始
    for line in reversed(lines):
        if '开始优化任务' in line:
            timestamp = line.split('[')[1].split(']')[0]
            
            # 收集这次运行的所有输出
            result_lines = []
            for l in lines:
                if timestamp in l:
                    result_lines.append(l)
                elif '开始优化任务' in l and l != line:
                    break
            
            return {
                'timestamp': timestamp,
                'output': ''.join(result_lines)
            }
    
    return None


def parse_result(output: str) -> dict:
    """解析运行结果"""
    result = {
        'method': None,
        'status': None,
        'hit3': None,
        'hit4': None,
        'hit5': None,
        'avg_hit': None,
        'periods': None,
        'hit3_avg': None,
    }
    
    # 检查是否跳过
    if '已纳入预测助手，跳过验证' in output:
        result['status'] = 'skipped'
        for line in output.split('\n'):
            if '发现新方法:' in line:
                result['method'] = line.split('发现新方法:')[1].strip()
                break
        return result
    
    lines = output.split('\n')
    for line in lines:
        if '发现新方法:' in line:
            result['method'] = line.split('发现新方法:')[1].strip()
        elif '状态:' in line:
            result['status'] = line.split('状态:')[1].strip()
        elif '3+命中率:' in line:
            result['hit3'] = line.split('3+命中率:')[1].strip()
        elif '4+命中率:' in line:
            result['hit4'] = line.split('4+命中率:')[1].strip()
        elif '5+命中率:' in line:
            result['hit5'] = line.split('5+命中率:')[1].strip()
        elif '平均命中:' in line:
            result['avg_hit'] = line.split('平均命中:')[1].strip().split('/')[0]
        elif '累计(' in line:
            result['periods'] = line.split('累计(')[1].split('次)')[0]
            if '3+命中率:' in line:
                result['hit3_avg'] = line.split('3+命中率:')[1].strip().replace('%', '')
    
    return result


def generate_message(result: dict) -> str:
    """生成飞书消息"""
    # 跳过情况
    if result.get('status') == 'skipped':
        return f"""**【自动优化】**

⚠️ {result['method']}
   已纳入预测助手，跳过验证

---
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}"""
    
    # 状态emoji
    status_emoji = {
        '新发现': '🆕',
        '测试中': '🔄',
        '继续测试': '📊',
        '建议加入预测助手！': '✅',
        '淘汰': '❌',
    }
    
    emoji = status_emoji.get(result.get('status', ''), '📊')
    
    # 累计信息
    cumulative = ""
    if result.get('periods') and result.get('hit3_avg'):
        cumulative = f"""
📈 累计({result['periods']}次): 3+命中率 {result['hit3_avg']}%"""
    
    message = f"""**【自动优化】{result['method']}**

{emoji} 状态: {result.get('status', '未知')}

📊 本轮验证:
   • 3+命中率: {result.get('hit3', '-')}%
   • 4+命中率: {result.get('hit4', '-')}%
   • 5+命中率: {result.get('hit5', '-')}%
   • 平均命中: {result.get('avg_hit', '-')}/7{cumulative}

---
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}"""
    
    return message


def send_feishu(message: str):
    """发送到飞书"""
    if not FEISHU_WEBHOOK_URL or FEISHU_WEBHOOK_URL == 'YOUR_WEBHOOK_URL_HERE':
        print("⚠️ 未配置FEISHU_WEBHOOK_URL")
        print("\n消息预览:")
        print(message)
        return False
    
    import requests
    try:
        response = requests.post(
            FEISHU_WEBHOOK_URL,
            json={
                'msg_type': 'text',
                'content': {'text': message}
            },
            timeout=10
        )
        if response.status_code == 200:
            print("✅ 发送成功")
            return True
        else:
            print(f"❌ 发送失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 发送出错: {e}")
        return False


def main():
    print("="*60)
    print("优化任务 - 飞书通知")
    print("="*60)
    
    latest = get_latest_result()
    if not latest:
        print("❌ 无运行记录")
        return
    
    result = parse_result(latest['output'])
    if not result['method']:
        print("❌ 无法解析结果")
        return
    
    message = generate_message(result)
    
    print("\n消息预览:")
    print("-"*60)
    print(message)
    print("-"*60)
    
    send_feishu(message)


if __name__ == '__main__':
    main()
