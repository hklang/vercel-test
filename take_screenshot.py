#!/usr/bin/env python3
import asyncio
from pyppeteer import launch
import os

async def main():
    # 启动浏览器
    browser = await launch(
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1920,1080']
    )
    
    try:
        # 创建新页面
        page = await browser.newPage()
        
        # 设置用户代理
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # 导航到页面
        print("正在访问页面...")
        await page.goto('https://cf.2hg.com/?action=mc', {'waitUntil': 'networkidle0', 'timeout': 30000})
        
        # 等待页面加载
        await asyncio.sleep(3)
        
        # 获取页面标题
        title = await page.title()
        print(f"页面标题: {title}")
        
        # 截图
        screenshot_path = '/tmp/cf_challenge_screenshot.png'
        await page.screenshot({'path': screenshot_path, 'fullPage': True})
        print(f"截图已保存到: {screenshot_path}")
        
        # 获取cookies
        cookies = await page.cookies()
        print(f"Cookies数量: {len(cookies)}")
        for cookie in cookies:
            print(f"  {cookie['name']}: {cookie['value']}")
            
    except Exception as e:
        print(f"错误: {e}")
    finally:
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())