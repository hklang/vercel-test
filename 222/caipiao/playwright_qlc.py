#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七乐彩数据爬虫 - 改进版
使用Playwright直接执行JavaScript操作页面
"""

import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime

async def scrape_qlc():
    all_data = []
    consecutive_no_new = 0
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox'])
        page = await browser.new_page()
        
        try:
            print("🚀 访问中彩网七乐彩页面...")
            await page.goto('https://www.zhcw.com/kjxx/qlc/', timeout=60000)
            await page.wait_for_load_state('networkidle', timeout=30000)
            
            # 使用JavaScript直接操作页面
            print("📋 执行JavaScript切换到'近100期'...")
            
            result = await page.evaluate('''async () => {
                // 尝试查找并点击"近100期"元素
                const elements = document.querySelectorAll('*');
                for (let el of elements) {
                    if (el.textContent && el.textContent.includes('近100期') && el.click) {
                        el.click();
                        return { success: true, action: 'clicked 近100期' };
                    }
                }
                
                // 如果没找到，尝试直接修改查询参数
                // 中彩网使用Vue或类似框架，数据在Vue实例中
                return { success: false, action: 'element not found' };
            }''')
            
            print(f"JavaScript结果: {result}")
            await page.wait_for_timeout(3000)
            
            # 获取当前表格数据量
            rows = await page.query_selector_all('table tr')
            print(f"📊 当前表格有 {len(rows)} 行")
            
            page_num = 1
            
            while consecutive_no_new < 5:
                print(f"\n📄 第 {page_num} 页...")
                
                await page.wait_for_selector('table tr', timeout=15000)
                
                rows = await page.query_selector_all('table tr')
                count = 0
                
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
                        count += 1
                
                if count == 0:
                    consecutive_no_new += 1
                    print(f"  本页无新数据 (连续 {consecutive_no_new} 次)")
                else:
                    consecutive_no_new = 0
                    print(f"  获取 {count} 条，累计 {len(all_data)} 条")
                    if all_data:
                        latest = all_data[0]['period']
                        print(f"  最新期号: {latest}")
                
                if page_num % 5 == 0:
                    print(f"\n📊 进度: 已获取 {len(all_data)} 条数据...")
                
                # 点击下一页
                next_link = await page.query_selector('a:has-text("»")')
                
                if next_link:
                    cls = await next_link.get_attribute('class') or ''
                    href = await next_link.get_attribute('href') or ''
                    
                    if 'disabled' in cls or href == '':
                        print("\n✅ 已到最后一页!")
                        break
                    
                    await next_link.click()
                    await page.wait_for_timeout(2500)
                    page_num += 1
                else:
                    print("\n⚠️ 未找到下一页按钮")
                    break
        
        except Exception as e:
            print(f"❌ 错误: {e}")
        
        finally:
            await browser.close()
    
    return all_data


async def main():
    print("=" * 60)
    print("🎯 七乐彩历史数据爬虫")
    print("📌 目标: 获取全部历史开奖数据")
    print("=" * 60)
    
    data = await scrape_qlc()
    
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
        
        print(f"\n✅ 完成! 数据已保存:")
        print(f"   {json_file} ({len(data)} 条)")
        print(f"   {txt_file}")
        
        if data:
            print(f"\n📋 数据预览:")
            print(f"   最新: {data[0]['period']} ({data[0]['date']})")
            print(f"   最老: {data[-1]['period']} ({data[-1]['date']})")
    else:
        print("\n❌ 未能获取数据")
        print("\n💡 提示: 中彩网可能有反爬虫机制")
        print("   建议手动访问 https://www.zhcw.com/kjxx/qlc/")
        print("   点击'自定义查询'获取数据后复制保存")


if __name__ == '__main__':
    asyncio.run(main())
