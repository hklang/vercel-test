#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七乐彩数据爬虫 - 深入分析版
"""

import asyncio
import json
from playwright.async_api import async_playwright
from datetime import datetime

async def deep_analyze():
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
        
        # 深入分析
        print("\n🔍 深度分析页面...")
        
        result = await page.evaluate('''() => {
            const info = {
                scripts: [],
                iframes: [],
                modals: [],
                forms: [],
                links: []
            };
            
            // 检查脚本中的数据
            const scripts = document.querySelectorAll('script');
            for (let script of scripts) {
                const content = script.textContent;
                if (content && content.includes('qh') && content.includes('kjsj')) {
                    info.scripts.push({
                        length: content.length,
                        sample: content.substring(0, 1000)
                    });
                }
            }
            
            // 检查iframe
            const iframes = document.querySelectorAll('iframe');
            for (let iframe of iframes) {
                info.iframes.push({
                    src: iframe.src,
                    visible: iframe.offsetParent !== null
                });
            }
            
            // 检查弹窗/模态框
            const modals = document.querySelectorAll('[class*="modal"], [class*="dialog"], [class*="popup"]');
            for (let modal of modals) {
                info.modals.push({
                    className: modal.className,
                    visible: modal.offsetParent !== null,
                    display: window.getComputedStyle(modal).display,
                    opacity: window.getComputedStyle(modal).opacity
                });
            }
            
            // 检查表单
            const forms = document.querySelectorAll('form');
            for (let form of forms) {
                info.forms.push({
                    action: form.action,
                    method: form.method
                });
            }
            
            // 检查所有链接
            const links = document.querySelectorAll('a');
            for (let link of links) {
                const text = link.textContent?.trim();
                if (text && (text.includes('查询') || text.includes('期'))) {
                    info.links.push({
                        text: text.substring(0, 30),
                        href: link.href,
                        visible: link.offsetParent !== null
                    });
                }
            }
            
            return info;
        }''')
        
        print(f"\n📊 深度分析结果:")
        print(f"   相关脚本: {len(result['scripts'])}")
        for i, script in enumerate(result['scripts'][:2]):
            print(f"     [{i}] 长度: {script['length']}")
            print(f"         样本: {script['sample'][:200]}...")
        
        print(f"   Iframes: {len(result['iframes'])}")
        for iframe in result['iframes']:
            print(f"     src: {iframe['src'][:50]}..., visible: {iframe['visible']}")
        
        print(f"   弹窗/对话框: {len(result['modals'])}")
        for modal in result['modals'][:5]:
            print(f"     class: {modal['className'][:50]}...")
            print(f"     visible: {modal['visible']}, display: {modal['display']}, opacity: {modal['opacity']}")
        
        print(f"   表单: {len(result['forms'])}")
        for form in result['forms']:
            print(f"     action: {form['action']}, method: {form['method']}")
        
        print(f"   相关链接: {len(result['links'])}")
        for link in result['links'][:10]:
            if link['visible']:
                print(f"     - {link['text']}: {link['href'][:50]}...")
        
        await page.screenshot(path='/home/lang/.openclaw/workspace/caipiao/deep_analyze.png')
        
        await browser.close()

async def main():
    print("=" * 60)
    print("🔍 深度分析中彩网页面结构")
    print("=" * 60)
    
    await deep_analyze()

if __name__ == '__main__':
    asyncio.run(main())
