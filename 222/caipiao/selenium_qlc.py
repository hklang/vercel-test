#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七乐彩数据爬虫 - 批量查询版本
分批次查询不同年份的数据
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

def query_period_range(driver, start_period, end_period):
    """查询指定期号范围的数据"""
    all_data = []
    
    try:
        # 点击"自定义查询"
        try:
            custom_link = driver.find_element(By.XPATH, "//*[contains(text(), '自定义查询')]")
            custom_link.click()
            time.sleep(2)
        except:
            pass
        
        # 点击"按期号"标签
        try:
            period_tab = driver.find_element(By.XPATH, "//*[contains(text(), '按期号')]")
            period_tab.click()
            time.sleep(1)
        except:
            pass
        
        # 找到起始期号输入框
        try:
            # 查找包含"第"字的输入框
            inputs = driver.find_elements(By.XPATH, "//input[@type='text' or @type='number']")
            for inp in inputs:
                placeholder = inp.get_attribute('placeholder') or ''
                if '第' in placeholder:
                    inp.clear()
                    inp.send_keys(start_period)
                    break
            else:
                # 尝试查找所有输入框
                for i, inp in enumerate(inputs):
                    if i == 0:  # 假设第一个是起始期号
                        inp.clear()
                        inp.send_keys(start_period)
                        break
        except Exception as e:
            print(f"  输入起始期号失败: {e}")
            return []
        
        # 找到结束期号输入框
        try:
            inputs = driver.find_elements(By.XPATH, "//input[@type='text' or @type='number']")
            for inp in inputs:
                placeholder = inp.get_attribute('placeholder') or ''
                if '至' in placeholder or '至' in inp.get_attribute('name') or '至' in inp.get_attribute('id'):
                    inp.clear()
                    inp.send_keys(end_period)
                    break
            else:
                # 尝试第二个输入框
                if len(inputs) >= 2:
                    inputs[1].clear()
                    inputs[1].send_keys(end_period)
        except Exception as e:
            print(f"  输入结束期号失败: {e}")
            return []
        
        # 点击查询按钮
        try:
            query_btn = driver.find_element(By.XPATH, "//button[contains(text(), '查询')]")
            query_btn.click()
            time.sleep(5)
        except Exception as e:
            print(f"  点击查询按钮失败: {e}")
            return []
        
        # 解析数据
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
        except TimeoutException:
            print(f"  等待表格超时 ({start_period}-{end_period})")
            return []
        
        rows = driver.find_elements(By.CSS_SELECTOR, "table tr")
        for row in rows[2:]:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) < 4:
                continue
            
            try:
                period = cells[0].text.strip()
                if not period.isdigit() or len(period) < 7:
                    continue
                
                date = cells[1].text.strip()
                date = date.split('（')[0].split('(')[0]
                
                basic_text = cells[2].text.strip()
                basic = basic_text.split()
                
                special = cells[3].text.strip()
                
                if len(basic) >= 7:
                    all_data.append({
                        'period': period,
                        'date': date,
                        'basic_numbers': sorted(basic[:7]),
                        'special_number': special
                    })
            except Exception:
                continue
        
    except Exception as e:
        print(f"  查询失败: {e}")
    
    return all_data


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
        print("访问中彩网七乐彩页面...")
        driver.get('https://www.zhcw.com/kjxx/qlc/')
        time.sleep(5)
        
        # 分批查询不同年份的数据
        # 七乐彩从2007年开始，每年约150期
        year_ranges = [
            ('2024001', '2026016'),  # 2024-2026
            ('2022001', '2023150'),  # 2022-2023
            ('2020001', '2021150'),  # 2020-2021
            ('2018001', '2019150'),  # 2018-2019
            ('2016001', '2017150'),  # 2016-2017
            ('2014001', '2015150'),  # 2014-2015
            ('2013001', '2013150'),  # 2013
            ('2011001', '2012150'),  # 2011-2012
            ('2009001', '2010150'),  # 2009-2010
            ('2007001', '2008150'),  # 2007-2008
        ]
        
        for start, end in year_ranges:
            print(f"\n查询 {start} - {end}...")
            data = query_period_range(driver, start, end)
            if data:
                print(f"  获取 {len(data)} 条数据")
                # 合并数据
                existing_periods = set(d['period'] for d in all_data)
                for item in data:
                    if item['period'] not in existing_periods:
                        all_data.append(item)
                        existing_periods.add(item['period'])
            else:
                print(f"  未获取到数据")
            
            time.sleep(2)
        
        print(f"\n总计获取 {len(all_data)} 条数据")
        
    finally:
        driver.quit()
    
    return all_data


def main():
    print("=" * 60)
    print("七乐彩历史数据爬虫 (批量查询版)")
    print("目标: 获取全部历史开奖数据")
    print("=" * 60)
    
    data = scrape_qlc()
    
    if data:
        data.sort(key=lambda x: x.get('period', ''), reverse=True)
        
        print(f"\n🎉 共获取 {len(data)} 条历史数据!")
        
        json_file = '/home/lang/.openclaw/workspace/caipiao/qlc_history.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        txt_file = '/home/lang/.openclaw/workspace/caipiao/qlc_history.txt'
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("七乐彩历史开奖数据\n")
            f.write(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"总数据量: {len(data)} 条\n")
            f.write("=" * 60 + "\n\n")
            for item in data:
                basic = ' '.join(item.get('basic_numbers', []))
                special = item.get('special_number', '')
                f.write(f"{item['period']} {item['date']}  {basic} + {special}\n")
        
        print(f"\n✅ 完成! 数据已保存:")
        print(f"   {json_file} ({len(data)} 条)")
        print(f"   {txt_file}")
    else:
        print("❌ 未能获取数据")


if __name__ == '__main__':
    main()
