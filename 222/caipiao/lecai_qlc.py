#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七乐彩数据爬虫 - 乐彩网版本
从乐彩网获取历史数据
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import time
from datetime import datetime

def scrape_qlc():
    all_data = []
    
    print("初始化Chrome浏览器...")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = '/usr/bin/chromium-browser'
    
    driver = webdriver.Chrome(options=options)
    
    try:
        print("访问乐彩网七乐彩页面...")
        driver.get('https://www.17500.cn/widget/qlc/survey/issue/0.html')
        time.sleep(5)
        
        # 滚动页面加载更多数据
        print("滚动加载数据...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        for i in range(20):  # 最多滚动20次
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print(f"第 {i+1} 次滚动，高度未变化，可能已加载全部数据")
                break
            last_height = new_height
            print(f"第 {i+1} 次滚动...")
        
        # 查找数据表格
        print("查找数据表格...")
        try:
            # 尝试查找各种可能的数据容器
            tables = driver.find_elements(By.TAG_NAME, "table")
            print(f"找到 {len(tables)} 个表格")
            
            for idx, table in enumerate(tables):
                rows = table.find_elements(By.TAG_NAME, "tr")
                print(f"表格 {idx+1}: {len(rows)} 行")
                
                for row in rows[:5]:  # 只打印前5行看看结构
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if cells:
                        print(f"  细胞: {[c.text[:20] for c in cells]}")
        except Exception as e:
            print(f"查找表格失败: {e}")
        
        # 查找包含期号的元素
        print("\n查找期号数据...")
        try:
            # 查找所有包含数字的元素
            all_text = driver.find_elements(By.XPATH, "//*[contains(text(), '20')]")
            periods = []
            for el in all_text[:50]:  # 只检查前50个
                text = el.text.strip()
                if text.isdigit() and len(text) == 7:
                    periods.append(text)
            
            unique_periods = list(set(periods))
            print(f"找到 {len(unique_periods)} 个期号")
            if unique_periods:
                print(f"示例期号: {unique_periods[:10]}")
        except Exception as e:
            print(f"查找期号失败: {e}")
        
    finally:
        driver.quit()
    
    return all_data


def main():
    print("=" * 60)
    print("七乐彩历史数据爬虫 (乐彩网版)")
    print("目标: 从乐彩网获取全部历史开奖数据")
    print("=" * 60)
    
    data = scrape_qlc()
    
    if data:
        print(f"\n🎉 共获取 {len(data)} 条历史数据!")
    else:
        print("\n❌ 未获取到数据")
        print("\n尝试手动访问: https://www.17500.cn/widget/qlc/survey/issue/0.html")


if __name__ == '__main__':
    main()
