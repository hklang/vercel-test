#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七乐彩数据爬虫 - 手动操作版
"""

import asyncio
import json
from playwright.async_api import async_playwright
from datetime import datetime

async def manual_scrape():
    all_data = []
    
    print("🚀 启动浏览器...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # 显示浏览器，可以看到操作过程
            args=['--no-sandbox']
        )
        
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        page = await context.new_page()
        
        print("📍 步骤1: 访问中彩网...")
        await page.goto('https://www.zhcw.com/kjxx/qlc/')
        await page.wait_for_load_state('networkidle', timeout=60000)
        print("✅ 页面加载完成")
        
        # 截图
        await page.screenshot(path='/home/lang/.openclaw/workspace/caipiao/step1.png')
        print("📸 截图已保存: step1.png")
        
        print("\n📋 步骤2: 查找'自定义查询'按钮...")
        await page.wait_for_timeout(2000)
        
        # 查找并点击"自定义查询"
        custom_query = await page.query_selector('text=自定义查询')
        if custom_query:
            print("✅ 找到'自定义查询'按钮，正在点击...")
            await custom_query.click()
            await page.wait_for_timeout(3000)
            await page.screenshot(path='/home/lang/.openclaw/workspace/caipiao/step2.png')
            print("📸 截图已保存: step2.png（弹窗出现）")
        else:
            print("❌ 未找到'自定义查询'按钮")
            await page.screenshot(path='/home/lang/.openclaw/workspace/caipiao/error1.png')
        
        print("\n📝 步骤3: 查找查询表单...")
        await page.wait_for_timeout(2000)
        
        # 查找所有输入框
        inputs = await page.query_selector_all('input')
        print(f"找到 {len(inputs)} 个输入框")
        
        # 查找"按期号"标签
        period_tab = await page.query_selector('text=按期号')
        if period_tab:
            print("✅ 找到'按期号'标签，正在点击...")
            await period_tab.click()
            await page.wait_for_timeout(2000)
            await page.screenshot(path='/home/lang/.openclaw/workspace/caipiao/step3.png')
        else:
            print("⚠️ 未找到'按期号'标签")
        
        print("\n⌨️ 步骤4: 输入期号范围...")
        await page.wait_for_timeout(1000)
        
        # 获取所有输入框
        inputs = await page.query_selector_all('input')
        print(f"当前有 {len(inputs)} 个输入框")
        
        # 尝试输入起始期号和结束期号
        await page.evaluate('''() => {
            const inputs = document.querySelectorAll('input');
            // 尝试填写起始期号
            for (let i = 0; i < inputs.length; i++) {
                const rect = inputs[i].getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0 && !inputs[i].disabled) {
                    // 假设第一个可见的是起始期号
                    inputs[i].value = '2025001';
                    inputs[i].dispatchEvent(new Event('input', { bubbles: true }));
                    break;
                }
            }
        }''')
        
        await page.wait_for_timeout(500)
        
        await page.evaluate('''() => {
            const inputs = document.querySelectorAll('input');
            // 尝试填写结束期号
            let count = 0;
            for (let i = 0; i < inputs.length; i++) {
                const rect = inputs[i].getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0 && !inputs[i].disabled) {
                    count++;
                    if (count == 2) {  // 第二个可见输入框
                        inputs[i].value = '2026016';
                        inputs[i].dispatchEvent(new Event('input', { bubbles: true }));
                        break;
                    }
                }
            }
        }''')
        
        await page.wait_for_timeout(500)
        await page.screenshot(path='/home/lang/.openclaw/workspace/caipiao/step4.png')
        print("📸 截图已保存: step4（输入期号后）")
        
        print("\n🔘 步骤5: 点击'查询'按钮...")
        await page.wait_for_timeout(1000)
        
        # 查找并点击"查询"按钮
        query_btns = await page.query_selector_all('button, a')
        for btn in query_btns:
            text = await btn.text_content()
            if text and '查询' in text and '开始' not in text:
                print(f"✅ 找到查询按钮: '{text.strip()}'")
                try:
                    await btn.click()
                    print("✅ 点击查询按钮成功")
                    break
                except Exception as e:
                    print(f"❌ 点击失败: {e}")
        
        print("⏳ 等待数据加载...")
        await page.wait_for_timeout(8000)
        await page.screenshot(path='/home/lang/.openclaw/workspace/caipiao/step5.png')
        print("📸 截图已保存: step5（查询结果）")
        
        print("\n📊 步骤6: 解析表格数据...")
        rows = await page.query_selector_all('table tr')
        print(f"表格有 {len(rows)} 行")
        
        for row in rows[2:]:
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
        
        print(f"\n📈 第一批次获取 {len(all_data)} 条数据")
        
        # 保存第一批数据
        if all_data:
            all_data.sort(key=lambda x: x.get('period', ''), reverse=True)
            with open('/home/lang/.openclaw/workspace/caipiao/qlc_history.json', 'w', encoding='utf-8') as f:
                json.dump(all_data, f, ensure_ascii=False, indent=2)
            print(f"✅ 已保存 {len(all_data)} 条数据到 qlc_history.json")
        
        await browser.close()
    
    return all_data

async def main():
    print("=" * 60)
    print("🎯 七乐彩数据获取 - 手动操作版")
    print("=" * 60)
    print("\n⚠️ 注意: 浏览器窗口将会显示，你可以看到操作过程")
    print("📁 截图保存在: /home/lang/.openclaw/workspace/caipiao/step*.png")
    print()
    
    data = await manual_scrape()
    
    if data:
        print(f"\n🎉 第一批次完成! 获取 {len(data)} 条数据")
        print(f"📊 数据范围: {data[0]['period']} - {data[-1]['period']}")
    else:
        print("\n⚠️ 第一批次未获取到数据，请检查截图")

if __name__ == '__main__':
    asyncio.run(main())
