#!/usr/bin/env python3
import requests
import re

# 完整的浏览器头信息
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

session = requests.Session()
session.headers.update(headers)

print("尝试访问 https://cf.2hg.com/?action=mc")
print("=" * 50)

try:
    response = session.get('https://cf.2hg.com/?action=mc', timeout=30)
    
    print(f"状态码: {response.status_code}")
    print(f"响应大小: {len(response.text)} 字节")
    
    # 检查响应头
    print("\n重要响应头:")
    for key, value in response.headers.items():
        if any(x in key.lower() for x in ['cf-', 'set-cookie', 'content-', 'server']):
            print(f"  {key}: {value}")
    
    # 提取标题
    title_match = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE)
    if title_match:
        print(f"\n页面标题: {title_match.group(1)}")
    
    # 检查是否是挑战页面
    if 'just a moment' in response.text.lower():
        print("\n检测到Cloudflare挑战页面")
        
        # 尝试提取挑战信息
        cf_ray = response.headers.get('CF-RAY', '未找到')
        print(f"CF-RAY: {cf_ray}")
        
        # 查找挑战脚本
        if 'cdn-cgi/challenge-platform' in response.text:
            print("找到挑战平台脚本")
            
    # 显示cookies
    print(f"\nCookies ({len(session.cookies)}个):")
    if session.cookies:
        for cookie in session.cookies:
            print(f"  {cookie.name}: {cookie.value}")
            if 'cf_' in cookie.name.lower():
                print(f"    ^ Cloudflare相关cookie")
    else:
        print("  无cookies")
        
except Exception as e:
    print(f"请求错误: {e}")
    
print("\n" + "=" * 50)
print("分析完成")