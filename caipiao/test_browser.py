#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七乐彩数据爬虫 - 直接操作版
"""

import asyncio
import json
from playwright.async_api import async_playwright
from datetime import datetime

async def scrape():
    print("🚀 启动浏览器...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # 非隐藏模式，可以看到操作过程
            args=['--no-sandbox']
        )
        
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        page = await context.new_page()
        
        print("📍 访问中彩网...")
        await page.goto('https://www.zhcw.com/kjxx/qlc/')
        await page.wait_for_load_state('networkidle', timeout=60000)
        
        print("📸 截图保存...")
        await page.screenshot(path='/home/lang/.openclaw/workspace/caipiao/screenshot_1.png')
        
        # 等待页面加载
        await page.wait_for_timeout(3000)
        
        print("🔍 查找并点击'自定义查询'...")
        
        # 尝试找到自定义查询按钮
        try:
            # 方法1：使用JavaScript查找包含"自定义查询"的元素
            clicked = await page.evaluate('''async () => {
                const elements = document.querySelectorAll('*');
                for (let el of elements) {
                    if (el.textContent && el.textContent.includes('自定义查询') && el.click) {
                        el.click();
                        return { success: true, text: el.textContent.substring(0, 50) };
                    }
                }
                return { success: false, reason: 'not found' };
            }''')
            print(f"点击结果: {clicked}")
        except Exception as e:
            print(f"点击失败: {e}")
        
        await page.wait_for_timeout(2000)
        
        print("📸 截图保存（点击后）...")
        await page.screenshot(path='/home/lang/.openclaw/workspace/caipiao/screenshot_2.png')
        
        # 获取当前页面HTML
        html = await page.content()
        print(f"页面HTML长度: {len(html)} 字符")
        
        await browser.close()
        
    return True

async def main():
    print("=" * 60)
    print("🎯 七乐彩数据获取测试")
    print("=" * 60)
    
    await scrape()
    
    print("\n✅ 测试完成!")
    print("📁 截图保存在: /home/lang/.openclaw/workspace/caipiao/screenshot_*.png")

if __name__ == '__main__':
    asyncio.run(main())
