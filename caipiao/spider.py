#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七乐彩历史数据爬虫
需要手动配置浏览器驱动或API
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from datetime import datetime

class QLCSpider:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        self.data = []
    
    def from_zhcw(self):
        """从中彩网获取数据（需要selenium）"""
        # 中彩网使用动态加载，需要selenium
        print("需要使用selenium: https://www.zhcw.com/kjxx/qlc/")
        pass
    
    def from_17500(self):
        """从乐彩网获取数据"""
        # 乐彩网有历史调查页面，可能需要特殊处理
        url = "https://www.17500.cn/widget/qlc/survey/type/new.html"
        try:
            r = requests.get(url, headers=self.headers, timeout=30)
            if r.status_code == 200:
                print(f"获取到乐彩网数据，长度: {len(r.text)}")
                return self.parse_17500(r.text)
        except Exception as e:
            print(f"获取失败: {e}")
        return []
    
    def parse_17500(self, html):
        """解析乐彩网数据"""
        # 这里需要根据实际页面结构调整解析逻辑
        return []
    
    def from_api(self, api_url):
        """从API获取数据"""
        try:
            r = requests.get(api_url, headers=self.headers, timeout=30)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"API请求失败: {e}")
        return None
    
    def save_data(self, filename="qlc_history"):
        """保存数据"""
        if self.data:
            # 按期号排序
            self.data.sort(key=lambda x: x.get('period', ''), reverse=True)
            
            # JSON
            json_file = f"/home/lang/.openclaw/workspace/caipiao/{filename}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            print(f"已保存: {json_file} ({len(self.data)} 条)")
            
            # TXT
            txt_file = f"/home/lang/.openclaw/workspace/caipiao/{filename}.txt"
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write("七乐彩历史开奖数据\n")
                f.write(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                for item in self.data:
                    period = item.get('period', '')
                    date = item.get('date', '')
                    basic = ' '.join(item.get('basic_numbers', []))
                    special = item.get('special_number', '')
                    f.write(f"{period} {date}  {basic} + {special}\n")
            print(f"已保存: {txt_file}")
        else:
            print("没有数据可保存")


def main():
    spider = QLCSpider()
    
    print("七乐彩数据爬虫")
    print("=" * 60)
    
    # 尝试从乐彩网获取
    print("\n尝试从乐彩网获取...")
    data = spider.from_17500()
    
    if data:
        spider.data = data
        spider.save_data()
        print("\n完成!")
    else:
        print("\n未能获取数据。")
        print("\n使用说明:")
        print("1. 访问 https://www.zhcw.com/kjxx/qlc/")
        print("2. 选择查询范围（近100期或全部）")
        print("3. 复制数据保存到 caipiao/ 目录")
        print("\n或配置selenium后运行:")
        print("  pip install selenium")
        print("  下载chromedriver")


if __name__ == '__main__':
    main()
