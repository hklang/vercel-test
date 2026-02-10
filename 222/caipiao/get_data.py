#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七乐彩数据爬虫 - 简单稳定版
"""

import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime

async def scrape():
    print("开始...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto('https://www.zhcw.com/kjxx/qlc/')
        await page.wait_for_load_state('networkidle')
        
        # 点击近100期
        span = await page.query_selector('span.annq[data-z="100"]')
        if span:
            await span.click()
            print("已选择近100期")
            await page.wait_for_timeout(3000)
        
        # 获取数据
        rows = await page.query_selector_all('table tr')
        print(f"表格行数: {len(rows)}")
        
        data = []
        for row in rows[2:]:
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
            
            if len(basic) >= 7:
                data.append({
                    'period': period,
                    'date': date,
                    'basic_numbers': sorted(basic[:7]),
                    'special_number': special
                })
        
        await browser.close()
        
        data.sort(key=lambda x: x.get('period', ''), reverse=True)
        
        print(f"获取 {len(data)} 条数据")
        
        # 保存
        with open('/home/lang/.openclaw/workspace/caipiao/qlc_history.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        with open('/home/lang/.openclaw/workspace/caipiao/qlc_history.txt', 'w') as f:
            f.write("七乐彩历史开奖数据\n")
            f.write(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            for item in data:
                basic = ' '.join(item.get('basic_numbers', []))
                special = item.get('special_number', '')
                f.write(f"{item['period']} {item['date']}  {basic} + {special}\n")
        
        print("\n前5条:")
        for item in data[:5]:
            print(f"  {item['period']} {item['date']} {' '.join(item['basic_numbers'])} + {item['special_number']}")
        
        print("\n✅ 完成!")

asyncio.run(scrape())
