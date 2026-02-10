#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七乐彩数据爬虫 - 获取当前页面数据
"""

import asyncio
import json
from playwright.async_api import async_playwright
from datetime import datetime

async def get_current_data():
    all_data = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=['--no-sandbox']
        )
        
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 900},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        page = await context.new_page()
        
        print("🚀 访问页面...")
        await page.goto('https://www.zhcw.com/kjxx/qlc/')
        await page.wait_for_load_state('networkidle', timeout=60000)
        print("✅ 页面加载完成")
        
        # 获取当前表格中的所有数据
        print("\n📊 获取当前表格数据...")
        
        rows = await page.query_selector_all('table tr')
        print(f"表格共有 {len(rows)} 行")
        
        for row in rows[2:]:  # 跳过表头
            cells = await row.query_selector_all('td, th')
            if len(cells) < 4:
                continue
            
            period = (await cells[0].text_content()).strip()
            if not period.isdigit() or len(period) < 7:
                continue
            
            if any(d['period'] == period for d in all_data):
                continue
            
            date = (await cells[1].text_content()).strip()
            date = date.split('（')[0].split('(')[0]
            
            basic_text = await cells[2].text_content()
            basic = basic_text.strip().split()
            
            special_text = await cells[3].text_content()
            special = special_text.strip()
            
            if len(basic) >= 7:
                all_data.append({
                    'period': period,
                    'date': date,
                    'basic_numbers': sorted(basic[:7]),
                    'special_number': special
                })
        
        print(f"\n📈 当前页面获取 {len(all_data)} 条数据")
        
        if all_data:
            all_data.sort(key=lambda x: x.get('period', ''), reverse=True)
            
            # 保存数据
            json_file = '/home/lang/.openclaw/workspace/caipiao/qlc_history.json'
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, ensure_ascii=False, indent=2)
            
            txt_file = '/home/lang/.openclaw/workspace/caipiao/qlc_history.txt'
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write("七乐彩历史开奖数据\n")
                f.write(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"总数据量: {len(all_data)} 条\n")
                f.write("=" * 60 + "\n\n")
                for item in all_data:
                    basic = ' '.join(item.get('basic_numbers', []))
                    special = item.get('special_number', '')
                    f.write(f"{item['period']} {item['date']}  {basic} + {special}\n")
            
            print(f"\n✅ 数据已保存:")
            print(f"   {json_file} ({len(all_data)} 条)")
            print(f"   {txt_file}")
            
            print(f"\n📋 数据范围:")
            print(f"   最新: {all_data[0]['period']} ({all_data[0]['date']})")
            print(f"   最老: {all_data[-1]['period']} ({all_data[-1]['date']})")
            
            print(f"\n📄 数据预览:")
            for item in all_data[:5]:
                basic = ' '.join(item.get('basic_numbers', []))
                special = item.get('special_number', '')
                print(f"   {item['period']} {item['date']}  {basic} + {special}")
        
        await page.screenshot(path='/home/lang/.openclaw/workspace/caipiao/current_data.png')
        print(f"\n📸 截图已保存: current_data.png")
        
        await browser.close()
    
    return all_data

async def main():
    print("=" * 60)
    print("📊 获取当前页面数据")
    print("=" * 60)
    
    await get_current_data()

if __name__ == '__main__':
    asyncio.run(main())
