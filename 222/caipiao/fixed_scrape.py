#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七乐彩数据爬虫 - 修复版
正确处理连在一起的号码
"""

import asyncio
import json
import re
from playwright.async_api import async_playwright
from datetime import datetime

def split_numbers(text):
    """拆分连在一起的号码，如 '02061014181923' -> ['02', '06', '10', '14', '18', '19', '23']"""
    if not text:
        return []
    # 每两个字符一组
    numbers = re.findall(r'\d{2}', text)
    return numbers

async def scrape():
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
        
        print("🚀 访问中彩网...")
        await page.goto('https://www.zhcw.com/kjxx/qlc/')
        await page.wait_for_load_state('networkidle', timeout=60000)
        print("✅ 页面加载完成")
        
        rows = await page.query_selector_all('table tr')
        print(f"表格共有 {len(rows)} 行")
        
        for row in rows[2:]:  # 跳过表头
            cells = await row.query_selector_all('td')
            if len(cells) < 4:
                continue
            
            period = (await cells[0].text_content()).strip()
            if not period.isdigit() or len(period) < 7:
                continue
            
            if any(d['period'] == period for d in all_data):
                continue
            
            date = (await cells[1].text_content()).strip()
            date = date.split('（')[0].split('(')[0]
            
            # 号码是连在一起的，需要拆分
            basic_text = await cells[2].text_content()
            basic = split_numbers(basic_text)
            
            special_text = await cells[3].text_content()
            special = split_numbers(special_text)
            special = special[0] if special else ''
            
            if len(basic) >= 7:
                all_data.append({
                    'period': period,
                    'date': date,
                    'basic_numbers': sorted(basic[:7]),
                    'special_number': special
                })
        
        print(f"\n📈 获取 {len(all_data)} 条数据")
        
        if all_data:
            all_data.sort(key=lambda x: x.get('period', ''), reverse=True)
            
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
            
            print(f"\n✅ 数据已保存!")
            print(f"   共 {len(all_data)} 条")
            print(f"   最新: {all_data[0]['period']} ({all_data[0]['date']})")
            print(f"   最老: {all_data[-1]['period']} ({all_data[-1]['date']})")
            
            print(f"\n📄 预览:")
            for item in all_data[:5]:
                basic = ' '.join(item.get('basic_numbers', []))
                special = item.get('special_number', '')
                print(f"   {item['period']} {item['date']}  {basic} + {special}")
        
        await page.screenshot(path='/home/lang/.openclaw/workspace/caipiao/result.png')
        await browser.close()
    
    return all_data

async def main():
    print("=" * 60)
    print("🎯 七乐彩数据获取")
    print("=" * 60)
    await scrape()

if __name__ == '__main__':
    asyncio.run(main())
