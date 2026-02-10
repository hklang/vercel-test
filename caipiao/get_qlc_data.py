#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七乐彩历史数据爬取脚本
从乐彩网获取所有七乐彩历史开奖数据
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time

def get_qlc_data():
    """获取七乐彩历史数据"""
    
    # 尝试从多个数据源获取
    sources = [
        {
            "name": "乐彩网七乐彩",
            "url": "https://www.17500.cn/getData/qlc.txt",
            "encoding": "utf-8"
        },
        {
            "name": "中彩网七乐彩历史",
            "url": "https://www.zhcw.com/kjxx/qlc/",
            "encoding": "utf-8"
        }
    ]
    
    all_data = []
    
    for source in sources:
        try:
            print(f"尝试从 {source['name']} 获取数据...")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            }
            
            response = requests.get(source['url'], headers=headers, timeout=30)
            response.encoding = source['encoding']
            
            if response.status_code == 200:
                print(f"成功连接到 {source['name']}")
                
                # 尝试解析数据
                if '17500.cn' in source['url']:
                    data = parse_17500_data(response.text)
                else:
                    data = parse_zhcw_data(response.text)
                
                if data:
                    all_data.extend(data)
                    print(f"成功解析 {len(data)} 条记录")
            else:
                print(f"请求失败: {response.status_code}")
                
        except Exception as e:
            print(f"获取数据失败: {e}")
            continue
    
    return all_data

def parse_17500_data(text):
    """解析乐彩网数据"""
    data = []
    try:
        # 尝试解析JSON格式
        lines = text.strip().split('\n')
        for line in lines:
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    # 格式: 期号 开奖号码
                    period = parts[0]
                    numbers = parts[1] if len(parts) > 1 else ""
                    
                    # 提取号码
                    number_list = re.findall(r'\d+', numbers)
                    if len(number_list) >= 7:
                        basic_numbers = number_list[:7]
                        special_number = number_list[7] if len(number_list) > 7 else ""
                        
                        record = {
                            "period": period,
                            "basic_numbers": basic_numbers,
                            "special_number": special_number,
                            "date": "",
                        }
                        data.append(record)
    except Exception as e:
        print(f"解析乐彩网数据失败: {e}")
    return data

def parse_zhcw_data(html):
    """解析中彩网数据"""
    data = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # 查找开奖记录表格
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 3:
                    # 尝试提取期号和号码
                    period_text = cells[0].get_text().strip()
                    if re.match(r'^\d{7,8}$', period_text):
                        date_text = cells[1].get_text().strip()
                        numbers_text = cells[2].get_text().strip()
                        
                        # 提取基本号码和特别号码
                        numbers = re.findall(r'\d+', numbers_text)
                        if len(numbers) >= 7:
                            basic_numbers = numbers[:7]
                            special_number = numbers[7] if len(numbers) > 7 else ""
                            
                            record = {
                                "period": period_text,
                                "date": date_text,
                                "basic_numbers": basic_numbers,
                                "special_number": special_number,
                            }
                            data.append(record)
    except Exception as e:
        print(f"解析中彩网数据失败: {e}")
    return data

def save_data(data, filename):
    """保存数据到文件"""
    if not data:
        print("没有数据可保存")
        return False
    
    # 保存为JSON格式
    json_file = f"/home/lang/.openclaw/workspace/caipiao/{filename}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"JSON数据已保存到: {json_file}")
    
    # 保存为TXT格式
    txt_file = f"/home/lang/.openclaw/workspace/caipiao/{filename}.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("七乐彩历史开奖数据\n")
        f.write("=" * 60 + "\n\n")
        for item in data:
            period = item.get('period', '')
            date = item.get('date', '')
            basic = ' '.join(item.get('basic_numbers', []))
            special = item.get('special_number', '')
            
            if special:
                f.write(f"{period} {date}  {basic} + {special}\n")
            else:
                f.write(f"{period} {date}  {basic}\n")
    print(f"TXT数据已保存到: {txt_file}")
    
    return True

def main():
    print("开始获取七乐彩历史数据...")
    print("=" * 60)
    
    data = get_qlc_data()
    
    if data:
        print(f"\n共获取 {len(data)} 条开奖记录")
        
        # 按期号排序
        data.sort(key=lambda x: x.get('period', ''), reverse=True)
        
        # 保存数据
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        save_data(data, f'qlc_history_{timestamp}')
        
        print("\n数据获取完成!")
    else:
        print("\n未能获取到数据，请稍后重试")

if __name__ == '__main__':
    main()
