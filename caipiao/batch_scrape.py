#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七乐彩数据爬虫 - 分批获取版
每获取100条数据就保存并反馈
"""

import asyncio
import json
from playwright.async_api import async_playwright
from datetime import datetime
import sys

# 全局进度
progress = {
    'total': 0,
    'current_batch': 0,
    'latest_period': None,
    'oldest_period': None
}

async def scrape_batch(page, start_period, end_period, batch_name):
    """获取指定期号范围的数据"""
    data = []
    
    print(f"\n📦 开始获取 {batch_name}: {start_period} - {end_period}")
    sys.stdout.flush()
    
    try:
        # 刷新页面
        await page.reload()
        await page.wait_for_load_state('networkidle', timeout=30000)
        await page.wait_for_timeout(2000)
        
        # 点击"自定义查询"
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
        
        # 查找并点击"按期号"标签
        period_tab = await page.query_selector('text=按期号')
        if period_tab:
            try:
                await period_tab.click()
                await page.wait_for_timeout(1000)
            except:
                pass
        
        # 找到所有输入框并输入期号范围
        await page.evaluate(f'''(start, end) => {{
            const inputs = document.querySelectorAll('input');
            let filled = 0;
            for (let inp of inputs) {{
                const ph = inp.placeholder || '';
                // 尝试找到第一个输入框作为起始期号
                if (filled === 0 && (ph.includes('期') || ph.includes('Start') || ph === '')) {{
                    inp.value = start;
                    inp.dispatchEvent(new Event('input', {{bubbles: true}}));
                    filled = 1;
                }} 
                // 找到第二个输入框作为结束期号
                else if (filled === 1 && (ph.includes('至') || ph.includes('End') || ph === '')) {{
                    inp.value = end;
                    inp.dispatchEvent(new Event('input', {{bubbles: true}}));
                    filled = 2;
                    break;
                }}
            }}
        }}''', start_period, end_period)
        
        await page.wait_for_timeout(1000)
        
        # 点击"查询"按钮
        query_btns = await page.query_selector_all('button, a')
        for btn in query_btns:
            text = await btn.text_content()
            if text and '查询' in text.strip():
                try:
                    await btn.click()
                    print(f"✅ 点击查询按钮: {text.strip()}")
                    sys.stdout.flush()
                    break
                except:
                    pass
        
        # 等待数据加载
        await page.wait_for_timeout(5000)
        
        # 获取表格数据
        rows = await page.query_selector_all('table tr')
        print(f"📊 表格有 {len(rows)} 行")
        sys.stdout.flush()
        
        batch_data = []
        for row in rows[2:]:
            cells = await row.query_selector_all('td, th')
            if len(cells) < 4:
                continue
            
            period = (await cells[0].text_content()).strip()
            if not period.isdigit() or len(period) < 7:
                continue
            
            date = (await cells[1].text_content()).strip()
            date = date.split('（')[0].split('(')[0]
            
            basic_text = await cells[2].text_content()
            basic = basic_text.strip().split()
            
            special_text = await cells[3].text_content()
            special = special_text.strip()
            
            if len(basic) >= 7:
                batch_data.append({
                    'period': period,
                    'date': date,
                    'basic_numbers': sorted(basic[:7]),
                    'special_number': special
                })
        
        print(f"📦 {batch_name} 获取 {len(batch_data)} 条数据")
        sys.stdout.flush()
        
        return batch_data
        
    except Exception as e:
        print(f"❌ {batch_name} 获取失败: {e}")
        sys.stdout.flush()
        return []


async def scrape_all():
    all_data = []
    
    print("🚀 启动浏览器...")
    sys.stdout.flush()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=['--no-sandbox']
        )
        
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        page = await context.new_page()
        
        # 访问主页面
        await page.goto('https://www.zhcw.com/kjxx/qlc/')
        await page.wait_for_load_state('networkidle', timeout=60000)
        print("✅ 页面加载完成")
        sys.stdout.flush()
        
        # 定义要查询的批次
        batches = [
            ('2025001', '2026016', '2025-2026年'),
            ('2023001', '2025000', '2023-2024年'),
            ('2021001', '2023000', '2021-2022年'),
            ('2019001', '2021000', '2019-2020年'),
            ('2017001', '2019000', '2017-2018年'),
            ('2015001', '2017000', '2015-2016年'),
            ('2013001', '2015000', '2013-2014年'),
            ('2011001', '2013000', '2011-2012年'),
            ('2009001', '2011000', '2009-2010年'),
            ('2007001', '2009150', '2007-2008年'),
        ]
        
        total_scraped = 0
        
        for start, end, name in batches:
            batch_data = await scrape_batch(page, start, end, name)
            
            # 去重合并
            existing_periods = set(d['period'] for d in all_data)
            new_count = 0
            for item in batch_data:
                if item['period'] not in existing_periods:
                    all_data.append(item)
                    existing_periods.add(item['period'])
                    new_count += 1
            
            total_scraped += new_count
            
            print(f"\n📈 进度报告:")
            print(f"   累计: {len(all_data)} 条")
            print(f"   本批次新增: {new_count} 条")
            if all_data:
                latest = max(all_data, key=lambda x: x['period'])
                oldest = min(all_data, key=lambda x: x['period'])
                print(f"   最新期号: {latest['period']} ({latest['date']})")
                print(f"   最老期号: {oldest['period']} ({oldest['date']})")
            sys.stdout.flush()
            
            # 保存中间结果
            all_data.sort(key=lambda x: x.get('period', ''), reverse=True)
            with open('/home/lang/.openclaw/workspace/caipiao/qlc_history.json', 'w', encoding='utf-8') as f:
                json.dump(all_data, f, ensure_ascii=False, indent=2)
            
            # 每批次之间等待一下
            await page.wait_for_timeout(2000)
        
        await browser.close()
    
    return all_data


async def main():
    print("=" * 60)
    print("🎯 七乐彩历史数据爬虫 - 分批获取版")
    print("📌 目标: 获取全部历史开奖数据")
    print("💾 每批次保存中间结果")
    print("=" * 60)
    sys.stdout.flush()
    
    print("\n⏳ 开始获取数据...")
    sys.stdout.flush()
    
    data = await scrape_all()
    
    if data:
        data.sort(key=lambda x: x.get('period', ''), reverse=True)
        
        print(f"\n" + "=" * 60)
        print(f"🎉 完成! 共获取 {len(data)} 条历史数据!")
        print(f"=" * 60)
        sys.stdout.flush()
        
        # 保存最终结果
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
        print(f"   {json_file} ({len(data)} 条)")
        print(f"   {txt_file}")
        sys.stdout.flush()
        
        print(f"\n📋 数据范围:")
        print(f"   最新: {data[0]['period']} ({data[0]['date']})")
        print(f"   最老: {data[-1]['period']} ({data[-1]['date']})")
        sys.stdout.flush()
    else:
        print("\n❌ 未获取到数据")
        sys.stdout.flush()


if __name__ == '__main__':
    asyncio.run(main())
