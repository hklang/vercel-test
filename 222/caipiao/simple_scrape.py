#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七乐彩数据爬虫 - 简单版
直接获取100期数据，不分页
"""

import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime

async def main():
    print("开始获取七乐彩数据...")
    
    all_data = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto('https://www.zhcw.com/kjxx/qlc/')
        await page.wait_for_load_state('networkidle', timeout=30000)
        print("页面加载完成")
        
        # 点击"近100期"选项
        print("选择近100期...")
        span = await page.query_selector('span.annq[data-z="100"]')
        if span:
            await span.click()
            await page.wait_for_timeout(5000)
        
        # 滚动页面触发懒加载
        print("滚动加载...")
        for i in range(10):
            await page.evaluate(f'window.scrollTo(0, {i * 800})')
            await page.wait_for_timeout(500)
        
        # 获取表格中所有数据
        print("解析数据...")
        rows = await page.query_selector_all('table tr')
        print(f"表格行数: {len(rows)}")
        
        for row in rows[2:]:  # 跳过表头
            cells = await row.query_selector_all('td, th')
            if len(cells) < 4:
                continue
            
            period = (await cells[0].text_content()).strip()
            if not period.isdigit() or len(period) < 7:
                continue
            
            date = (await cells[1].text_content()).strip()
            date = date.split('（')[0].split('(')[0]
            
            # 基本号码
            spans = await cells[2].query_selector_all('span.jqh')
            basic = [await s.text_content() for s in spans]
            
            # 特别号码
            special_spans = await cells[3].query_selector_all('span.jql')
            special = [await s.text_content() for s in special_spans]
            special = special[0] if special else ''
            
            if len(basic) >= 7 and period not in [d.get('period') for d in all_data]:
                all_data.append({
                    'period': period,
                    'date': date,
                    'basic_numbers': sorted(basic[:7]),
                    'special_number': special
                })
        
        await browser.close()
    
    # 排序
    all_data.sort(key=lambda x: x.get('period', ''), reverse=True)
    
    print(f"\n共获取 {len(all_data)} 条数据")
    
    # 保存
    with open('/home/lang/.openclaw/workspace/caipiao/qlc_history.json', 'w') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    with open('/home/lang/.openclaw/workspace/caipiao/qlc_history.txt', 'w') as f:
        f.write("七乐彩历史开奖数据\n")
        f.write(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        for item in all_data:
            basic = ' '.join(item.get('basic_numbers', []))
            special = item.get('special_number', '')
            f.write(f"{item['period']} {item['date']}  {basic} + {special}\n")
    
    print("\n前5条:")
    for item in all_data[:5]:
        print(f"  {item['period']} {item['date']} {' '.join(item['basic_numbers'])} + {item['special_number']}")
    
    print("\n✅ 完成!")

asyncio.run(main())
