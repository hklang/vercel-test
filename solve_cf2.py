#!/usr/bin/env python3
import requests
import re
import time

def solve_cf():
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    print("获取页面...")
    resp = session.get('https://cf.2hg.com/?action=mc', headers=headers)
    print(f"HTML长度: {len(resp.text)}")
    print(f"状态码: {resp.status_code}")
    
    # 保存原始响应
    with open('cf_raw.html', 'w', encoding='utf-8') as f:
        f.write(resp.text)
    
    # 查找所有可能的令牌
    print("\n搜索令牌...")
    
    # 查找 __cf_chl_tk
    cf_tk_matches = re.findall(r'__cf_chl_tk=([^"\']+)', resp.text)
    print(f"找到 __cf_chl_tk: {len(cf_tk_matches)} 个")
    for i, tk in enumerate(cf_tk_matches[:3]):
        print(f"  {i+1}. {tk[:80]}...")
    
    # 查找 __cf_chl_rt_tk
    cf_rt_tk_matches = re.findall(r'__cf_chl_rt_tk=([^"\']+)', resp.text)
    print(f"找到 __cf_chl_rt_tk: {len(cf_rt_tk_matches)} 个")
    
    # 查找 __cf_chl_f_tk
    cf_f_tk_matches = re.findall(r'__cf_chl_f_tk=([^"\']+)', resp.text)
    print(f"找到 __cf_chl_f_tk: {len(cf_f_tk_matches)} 个")
    
    # 查找 ray ID
    ray_matches = re.findall(r'ray=([^"\']+)', resp.text)
    print(f"找到 ray: {len(ray_matches)} 个")
    for i, ray in enumerate(ray_matches[:3]):
        print(f"  {i+1}. {ray}")
    
    # 查找 cRay
    cray_matches = re.findall(r'cRay:\s*[\'"]([^\'"]+)[\'"]', resp.text)
    print(f"找到 cRay: {len(cray_matches)} 个")
    
    # 尝试使用第一个找到的ray访问挑战端点
    if ray_matches:
        ray = ray_matches[0]
        print(f"\n使用 ray={ray} 访问挑战端点...")
        
        challenge_url = f"https://cf.2hg.com/cdn-cgi/challenge-platform/h/b/orchestrate/chl_page/v1?ray={ray}"
        headers['Referer'] = 'https://cf.2hg.com/?action=mc'
        
        try:
            resp2 = session.get(challenge_url, headers=headers, timeout=10)
            print(f"挑战端点状态码: {resp2.status_code}")
            print(f"挑战端点响应长度: {len(resp2.text)}")
            
            # 保存挑战响应
            with open('cf_challenge_response.html', 'w', encoding='utf-8') as f:
                f.write(resp2.text)
                
        except Exception as e:
            print(f"访问挑战端点错误: {e}")
    
    # 等待并重试
    print("\n等待5秒后重试...")
    time.sleep(5)
    
    resp3 = session.get('https://cf.2hg.com/?action=mc', headers=headers)
    print(f"重试状态码: {resp3.status_code}")
    print(f"Cookies: {session.cookies.get_dict()}")
    
    # 保存最终cookies
    cookies = session.cookies.get_dict()
    with open('cf_final_cookies.txt', 'w') as f:
        for name, value in cookies.items():
            f.write(f"{name}={value}\n")
    
    return cookies

if __name__ == "__main__":
    cookies = solve_cf()
    print(f"\n最终Cookies: {cookies}")