#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七乐彩数据爬虫 - 完整版
直接使用Playwright操作浏览器获取数据
"""

import asyncio
import json
from playwright.async_api import async_playwright
from datetime import datetime

async def scrape_qlc_all():
    all_data = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # 非隐藏模式
            args=['--no-sandbox']
        )
        
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        page = await context.new_page()
        
        print("🚀 访问中彩网七乐彩...")
        await page.goto('https://www.zhcw.com/kjxx/qlc/')
        await page.wait_for_load_state('networkidle', timeout=60000)
        print("✅ 页面加载完成")
        
        # 尝试点击"自定义查询"
        print("📋 点击'自定义查询'...")
        await page.evaluate('''() => {
            const elements = document.querySelectorAll('*');
            for (let el of elements) {
                if (el.textContent && el.textContent.includes('自定义查询') && el.click) {
                    el.click();
                    return;
                }
            }
        }''')
        await page.wait_for_timeout(3000)
        
        # 查找弹出的对话框
        print("🔍 查找查询对话框...")
        dialogs = await page.query_selector_all('[class*="dialog"], [class*="modal"], [class*="popup"]')
        print(f"找到 {len(dialogs)} 个对话框")
        
        # 尝试在页面中查找输入框
        print("📝 查找输入框...")
        inputs = await page.query_selector_all('input')
        print(f"找到 {len(inputs)} 个输入框")
        
        # 尝试查找"按期数"相关的元素
        print("🔎 查找'按期数'标签...")
        period_tab = await page.query_selector('text=按期数')
        if period_tab:
            print("✅ 找到'按期数'标签")
            await period_tab.click()
            await page.wait_for_timeout(1000)
        
        # 尝试输入查询范围
        print("⌨️ 输入查询范围...")
        await page.evaluate('''() => {
            // 尝试找到起始期号输入框
            const inputs = document.querySelectorAll('input');
            for (let i = 0; i < inputs.length; i++) {
                const placeholder = inputs[i].placeholder || '';
                if (placeholder.includes('期') || placeholder.includes('Start')) {
                    inputs[i].value = '2024001';
                    inputs[i].dispatchEvent(new Event('input', { bubbles: true }));
                    break;
                }
            }
        }''')
        
        await page.wait_for_timeout(500)
        
        # 查找并点击"查询"按钮
        print("🔘 查找'查询'按钮...")
        query_btns = await page.query_selector_all('button, a')
        for btn in query_btns:
            text = await btn.text_content()
            if text and '查询' in text:
                print(f"✅ 找到查询按钮: {text.strip()}")
                await btn.click()
                break
        
        await page.wait_for_timeout(5000)  # 等待数据加载
        
        # 获取表格数据
        print("📊 获取表格数据...")
        rows = await page.query_selector_all('table tr')
        print(f"表格有 {len(rows)} 行")
        
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
        
        print(f"\n📈 第1批次获取 {len(all_data)} 条数据")
        
        # 截图保存
        await page.screenshot(path='/home/lang/.openclaw/workspace/caipiao/screenshot_result.png')
        print("📸 结果截图已保存")
        
        await browser.close()
    
    return all_data

async def main():
    print("=" * 60)
    print("🎯 七乐彩历史数据获取")
    print("=" * 60)
    
    print("\n⏳ 开始获取数据...")
    data = await scrape_qlc_all()
    
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
        
        print(f"\n✅ 数据已保存:")
        print(f"   {json_file}")
        print(f"   {txt_file}")
        
        if data:
            print(f"\n📋 数据预览:")
            print(f"   最新: {data[0]['period']} ({data[0]['date']})")
            print(f"   最老: {data[-1]['period']} ({data[-1]['date']})")
    else:
        print("\n⚠️ 未获取到数据")

if __name__ == '__main__':
    asyncio.run(main())
