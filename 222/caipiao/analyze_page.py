#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七乐彩数据爬虫 - 直接分析页面结构版
"""

import asyncio
import json
from playwright.async_api import async_playwright
from datetime import datetime

async def analyze_and_scrape():
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
        
        # 分析页面结构
        print("\n🔍 分析页面结构...")
        
        structure = await page.evaluate('''() => {
            const result = {
                hasTable: false,
                tableRows: 0,
                hasCustomQuery: false,
                dialogVisible: false,
                inputs: [],
                buttons: [],
                vueData: null
            };
            
            // 检查表格
            const table = document.querySelector('table');
            if (table) {
                result.hasTable = true;
                result.tableRows = table.querySelectorAll('tr').length;
            }
            
            // 检查自定义查询
            const allElements = document.querySelectorAll('*');
            for (let el of allElements) {
                if (el.textContent && el.textContent.includes('自定义查询')) {
                    result.hasCustomQuery = true;
                    break;
                }
            }
            
            // 检查dialog
            const dialogs = document.querySelectorAll('[class*="dialog"], [class*="modal"], [class*="popup"]');
            result.dialogVisible = dialogs.length > 0;
            
            // 收集输入框
            const inputs = document.querySelectorAll('input');
            for (let inp of inputs) {
                result.inputs.push({
                    type: inp.type,
                    placeholder: inp.placeholder,
                    visible: inp.offsetParent !== null,
                    disabled: inp.disabled
                });
            }
            
            // 收集按钮
            const buttons = document.querySelectorAll('button');
            for (let btn of buttons) {
                result.buttons.push({
                    text: btn.textContent?.substring(0, 30),
                    visible: btn.offsetParent !== null
                });
            }
            
            // 查找Vue实例数据
            try {
                const vueEl = document.querySelector('[class*="el-dialog"]') || document.querySelector('.ivu-modal');
                if (vueEl && vueEl.__vue__) {
                    result.vueData = JSON.stringify(vueEl.__vue__.$data).substring(0, 500);
                }
            } catch(e) {}
            
            return result;
        }''')
        
        print(f"\n📊 页面分析结果:")
        print(f"   表格: {structure['hasTable']}, 行数: {structure['tableRows']}")
        print(f"   自定义查询: {structure['hasCustomQuery']}")
        print(f"   对话框: {structure['dialogVisible']}")
        print(f"   输入框数量: {len(structure['inputs'])}")
        for i, inp in enumerate(structure['inputs'][:5]):
            print(f"     [{i}] type={inp['type']}, placeholder='{inp['placeholder']}', visible={inp['visible']}")
        print(f"   按钮数量: {len(structure['buttons'])}")
        for i, btn in enumerate(structure['buttons'][:5]):
            print(f"     [{i}] text='{btn['text']}', visible={btn['visible']}")
        
        # 点击自定义查询
        print("\n🔘 点击'自定义查询'...")
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
        
        # 再次分析页面
        print("\n🔍 再次分析页面（点击后）...")
        structure2 = await page.evaluate('''() => {
            const result = {
                dialogVisible: false,
                inputs: [],
                buttons: []
            };
            
            // 检查dialog
            const dialogs = document.querySelectorAll('[class*="dialog"], [class*="modal"], [class*="popup"]');
            result.dialogVisible = dialogs.length > 0;
            
            // 收集输入框
            const inputs = document.querySelectorAll('input');
            for (let inp of inputs) {
                result.inputs.push({
                    type: inp.type,
                    placeholder: inp.placeholder,
                    visible: inp.offsetParent !== null,
                    value: inp.value
                });
            }
            
            // 收集按钮
            const buttons = document.querySelectorAll('button');
            for (let btn of buttons) {
                const text = btn.textContent?.trim();
                if (text) {
                    result.buttons.push({
                        text: text,
                        visible: btn.offsetParent !== null
                    });
                }
            }
            
            return result;
        }''')
        
        print(f"   对话框: {structure2['dialogVisible']}")
        print(f"   输入框数量: {len(structure2['inputs'])}")
        for i, inp in enumerate(structure2['inputs']):
            if inp['visible']:
                print(f"     [{i}] type={inp['type']}, placeholder='{inp['placeholder']}', value='{inp['value']}'")
        print(f"   按钮: {len(structure2['buttons'])}")
        for btn in structure2['buttons'][:10]:
            if btn['visible']:
                print(f"     - {btn['text']}")
        
        await page.screenshot(path='/home/lang/.openclaw/workspace/caipiao/analyze.png')
        
        await browser.close()
    
    return all_data

async def main():
    print("=" * 60)
    print("🔍 七乐彩页面结构分析")
    print("=" * 60)
    
    await analyze_and_scrape()

if __name__ == '__main__':
    asyncio.run(main())
