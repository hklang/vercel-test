#!/usr/bin/env python3
import requests
import re
import time
import hashlib
import json

def solve_cf_challenge():
    session = requests.Session()
    
    # 第一次请求获取挑战页面
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    
    print("1. 获取初始页面...")
    resp = session.get('https://cf.2hg.com/?action=mc', headers=headers)
    print(f"   状态码: {resp.status_code}")
    
    # 提取挑战令牌
    cf_chl_tk_match = re.search(r'__cf_chl_tk=([^"\']+)', resp.text)
    if cf_chl_tk_match:
        cf_chl_tk = cf_chl_tk_match.group(1)
        print(f"   找到挑战令牌: {cf_chl_tk[:50]}...")
    else:
        print("   未找到挑战令牌")
        return None
    
    # 提取其他必要信息
    # 尝试查找ray ID
    ray_match = re.search(r'cRay:\s*\'([^\']+)\'', resp.text)
    if ray_match:
        ray_id = ray_match.group(1)
        print(f"   Ray ID: {ray_id}")
    
    # 尝试查找其他参数
    cv_id_match = re.search(r'cvId:\s*\'([^\']+)\'', resp.text)
    if cv_id_match:
        cv_id = cv_id_match.group(1)
        print(f"   cvId: {cv_id}")
    
    # 尝试直接访问带有令牌的URL
    print("\n2. 尝试使用挑战令牌访问...")
    challenge_url = f"https://cf.2hg.com/cdn-cgi/challenge-platform/h/b/orchestrate/chl_page/v1?ray={ray_id if 'ray_id' in locals() else '9d328df1c9041e11'}"
    print(f"   挑战URL: {challenge_url}")
    
    # 设置referer和cookie
    headers['Referer'] = 'https://cf.2hg.com/?action=mc'
    
    # 尝试获取挑战脚本
    resp2 = session.get(challenge_url, headers=headers)
    print(f"   挑战脚本状态码: {resp2.status_code}")
    print(f"   挑战脚本长度: {len(resp2.text)}")
    
    # 尝试提交答案（简化版）
    print("\n3. 尝试提交答案...")
    # 这里需要实际计算挑战答案，但比较复杂
    # 作为简化，我们尝试等待然后重试
    
    time.sleep(3)
    
    # 再次尝试访问原始URL
    print("\n4. 重试访问原始页面...")
    resp3 = session.get('https://cf.2hg.com/?action=mc', headers=headers)
    print(f"   状态码: {resp3.status_code}")
    print(f"   Cookies: {session.cookies.get_dict()}")
    
    # 保存cookies
    with open('cf_cookies_final.txt', 'w') as f:
        for name, value in session.cookies.get_dict().items():
            f.write(f"{name}={value}\n")
    
    return session.cookies.get_dict()

if __name__ == "__main__":
    cookies = solve_cf_challenge()
    if cookies:
        print(f"\n最终获取的Cookies: {cookies}")
    else:
        print("\n未能获取cookies")