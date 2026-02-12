#!/usr/bin/env python3
"""
七乐彩数据同步脚本
尝试多个数据源，获取最新开奖数据
"""

import http.client
import json
import re
import time
from datetime import datetime
from pathlib import Path

DATA_FILE = '/home/lang/.openclaw/workspace/caipiao/qlc_history_full.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    data.sort(key=lambda x: x['period'])
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def try_cwl_gov():
    """尝试官网API"""
    print("  尝试官网...")
    try:
        conn = http.client.HTTPSConnection("www.cwl.gov.cn", timeout=5)
        
        # 尝试多个可能的API路径
        paths = [
            "/cms_home/20108/index/data_json/2026/0211/2026018.json",
            "/tzxx/kjxx/qlc/20260211/2026018.html",
        ]
        
        for path in paths:
            try:
                conn.request("GET", path, headers={'User-Agent': 'Mozilla/5.0'})
                resp = conn.getresponse()
                if resp.status == 200:
                    content = resp.read().decode('utf-8')
                    print(f"    状态: {resp.status}, 长度: {len(content)}")
                    return content
            except:
                pass
        conn.close()
    except Exception as e:
        print(f"    失败: {e}")

def try_17500_cn():
    """尝试17500.cn"""
    print("  尝试17500.cn...")
    try:
        conn = http.client.HTTPSConnection("www.17500.cn", timeout=5)
        conn.request("GET", "/getDetailData.php?issue=2026018&type=qlc", 
                    headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
        resp = conn.getresponse()
        if resp.status == 200:
            content = resp.read().decode('utf-8')
            print(f"    状态: {resp.status}, 长度: {len(content)}")
            return content
        conn.close()
    except Exception as e:
        print(f"    失败: {e}")

def try_caishen():
    """尝试财神网"""
    print("  尝试财神网...")
    try:
        conn = http.client.HTTPSConnection("www.caishen.net", timeout=5)
        conn.request("GET", "/qlc/", headers={'User-Agent': 'Mozilla/5.0'})
        resp = conn.getresponse()
        if resp.status == 200:
            content = resp.read().decode('utf-8')
            print(f"    状态: {resp.status}, 长度: {len(content)}")
            return content
        conn.close()
    except Exception as e:
        print(f"    失败: {e}")

def parse_data(content, source):
    """解析数据"""
    results = []
    
    if not content:
        return results
    
    # 尝试JSON解析
    try:
        if source == 'json':
            data = json.loads(content)
            # 解析JSON格式
            if isinstance(data, dict):
                results.append({
                    'period': data.get('issue', ''),
                    'date': data.get('date', ''),
                    'numbers': data.get('numbers', []),
                    'special': data.get('special', '')
                })
    except:
        pass
    
    return results

def sync_data():
    """同步数据"""
    print("=" * 60)
    print(f"七乐彩数据同步")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    data = load_data()
    current_latest = data[-1]['period'] if data else None
    print(f"\n当前最新: {current_latest}")
    
    # 尝试获取数据
    content = None
    sources_tried = []
    
    sources_tried.append(('官网', try_cwl_gov))
    sources_tried.append(('17500.cn', try_17500_cn))
    
    for name, func in sources_tried:
        content = func()
        if content and len(content) > 50:
            print(f"  ✅ 成功获取数据")
            break
    
    if not content or len(content) < 50:
        print("\n❌ 所有数据源都无法获取数据")
        print("请使用 manual_update.py 手动添加数据")
        return
    
    # 解析数据（简化版）
    print(f"\n获取到 {len(content)} 字节的数据")
    
    # 检查是否包含最新期号
    import re
    match = re.search(r'202601[0-9]+', content)
    if match:
        print(f"  找到期号: {match.group()}")
    else:
        print("  未找到期号")
    
    print("\n" + "=" * 60)
    print("建议:")
    print("1. 如有最新开奖号码，使用 manual_update.py 添加")
    print("2. 如有可用数据源，请告知")
    print("=" * 60)

if __name__ == '__main__':
    sync_data()
