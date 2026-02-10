#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七乐彩历史数据爬虫 - 分页版本
使用方法：
1. 有Selenium环境: pip install selenium, 下载chromedriver
2. 无Selenium: 手动下载数据后运行
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from datetime import datetime

class QLCScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        self.data = []
    
    def scrape_with_selenium(self):
        """使用Selenium分页爬取（推荐）"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
        except ImportError:
            print("Selenium未安装，请运行: pip install selenium")
            return []
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        
        driver = webdriver.Chrome(options=options)
        
        try:
            # 访问中彩网
            driver.get('https://www.zhcw.com/kjxx/qlc/')
            time.sleep(3)
            
            all_data = []
            page = 1
            
            while True:
                # 等待页面加载
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "table"))
                    )
                except:
                    break
                
                # 解析当前页
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                page_data = self.parse_table(soup)
                
                if not page_data:
                    break
                
                all_data.extend(page_data)
                print(f"第{page}页: 获取{len(page_data)}条数据")
                
                # 点击下一页
                try:
                    next_btn = driver.find_element(By.CLASS_NAME, "next")
                    if "disabled" in next_btn.get_attribute("class"):
                        break
                    next_btn.click()
                    time.sleep(2)
                    page += 1
                except:
                    break
            
            return all_data
            
        finally:
            driver.quit()
    
    def parse_table(self, soup):
        """解析表格数据"""
        data = []
        tables = soup.find_all('table')
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 3:
                    # 提取期号
                    period = ""
                    date = ""
                    numbers = ""
                    
                    for cell in cells:
                        text = cell.get_text().strip()
                        if re.match(r'^\d{7,8}$', text):
                            period = text
                        elif re.search(r'\d{4}-\d{2}-\d{2}', text):
                            date = re.search(r'(\d{4}-\d{2}-\d{2})', text).group(1)
                        elif re.search(r'\d{2}', text) and len(text) > 10:
                            numbers = text
                    
                    if period and numbers:
                        nums = re.findall(r'\d+', numbers)
                        if len(nums) >= 7:
                            data.append({
                                'period': period,
                                'date': date,
                                'basic_numbers': [n.zfill(2) for n in nums[:7]],
                                'special_number': nums[7].zfill(2) if len(nums) > 7 else ""
                            })
        
        return data
    
    def scrape_manual(self, max_pages=100):
        """手动分页爬取（无Selenium时使用）"""
        print("由于网络限制，使用备用方案...")
        
        # 这里可以添加手动解析逻辑
        # 或者使用其他可访问的API
        
        return []
    
    def save_data(self, data=None, filename="qlc_history"):
        """保存数据"""
        if data is None:
            data = self.data
        
        if not data:
            print("没有数据可保存")
            return False
        
        # 排序
        data.sort(key=lambda x: x.get('period', ''), reverse=True)
        self.data = data
        
        # JSON
        json_file = f"/home/lang/.openclaw/workspace/caipiao/{filename}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON: {json_file} ({len(data)} 条)")
        
        # TXT
        txt_file = f"/home/lang/.openclaw/workspace/caipiao/{filename}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("七乐彩历史开奖数据\n")
            f.write(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
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
        print(f"✅ TXT: {txt_file}")
        
        return True


def main():
    scraper = QLCScraper()
    
    print("=" * 60)
    print("七乐彩历史数据爬虫 - 分页版")
    print("=" * 60)
    
    print("\n选择爬取方式:")
    print("1. Selenium (需要安装chromedriver)")
    print("2. 手动模式 (备用)")
    
    choice = input("请选择 (1/2): ").strip()
    
    if choice == "1":
        data = scraper.scrape_with_selenium()
    else:
        data = scraper.scrape_manual()
    
    if data:
        scraper.save_data(data)
        print(f"\n✅ 成功获取 {len(data)} 条数据!")
    else:
        print("\n未能获取数据")
        print("\n安装Selenium后运行:")
        print("  pip install selenium")
        print("  下载对应版本的chromedriver")


if __name__ == '__main__':
    main()
