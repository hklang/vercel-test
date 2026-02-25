#!/usr/bin/env python3
"""
分析Cloudflare挑战页面，提取关键信息
"""

import re
import json
import base64

def extract_cf_challenge_info(html_content):
    """从HTML中提取Cloudflare挑战信息"""
    print("=== Cloudflare挑战页面分析 ===")
    
    # 查找关键信息
    patterns = {
        'ray_id': r'cRay:\s*[\'"]([^\'"]+)[\'"]',
        'challenge_token': r'__cf_chl_tk=([^\s&"\']+)',
        'cf_chl_opt': r'window\._cf_chl_opt\s*=\s*({[^;]+});',
        'challenge_script': r'src="([^"]*cdn-cgi/challenge-platform[^"]*)"',
    }
    
    results = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, html_content, re.IGNORECASE)
        if match:
            if key == 'cf_chl_opt':
                try:
                    # 尝试解析JSON
                    json_str = match.group(1)
                    results[key] = json.loads(json_str)
                    print(f"找到 {key}: JSON对象")
                except:
                    results[key] = match.group(1)
                    print(f"找到 {key}: {match.group(1)[:100]}...")
            else:
                results[key] = match.group(1)
                print(f"找到 {key}: {match.group(1)}")
    
    # 检查挑战类型
    if 'turnstile' in html_content.lower():
        print("挑战类型: Cloudflare Turnstile")
    elif 'managed' in html_content.lower():
        print("挑战类型: Cloudflare Managed Challenge")
    else:
        print("挑战类型: 未知")
    
    # 提取更多信息
    title_match = re.search(r'<title>([^<]+)</title>', html_content, re.IGNORECASE)
    if title_match:
        print(f"页面标题: {title_match.group(1)}")
    
    # 检查是否有自动刷新
    refresh_match = re.search(r'<meta[^>]*http-equiv="refresh"[^>]*content="([^"]*)"', html_content, re.IGNORECASE)
    if refresh_match:
        print(f"自动刷新: {refresh_match.group(1)}")
    
    return results

def decode_base64_url(url_encoded):
    """解码Base64 URL编码的字符串"""
    try:
        # 替换URL安全字符
        url_encoded = url_encoded.replace('-', '+').replace('_', '/')
        # 添加填充
        padding = 4 - len(url_encoded) % 4
        if padding != 4:
            url_encoded += '=' * padding
        
        decoded = base64.b64decode(url_encoded).decode('utf-8', errors='ignore')
        return decoded
    except:
        return None

def analyze_challenge_response():
    """分析挑战响应"""
    print("\n=== 挑战响应分析 ===")
    
    # 从之前的curl响应中获取的关键部分
    challenge_html = """<!DOCTYPE html><html lang="en-US"><head><title>Just a moment...</title><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=Edge"><meta name="robots" content="noindex,nofollow"><meta name="viewport" content="width=device-width,initial-scale=1"><style>*{box-sizing:border-box;margin:0;padding:0}html{line-height:1.15;-webkit-text-size-adjust:100%;color:#313131;font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji"}body{display:flex;flex-direction:column;height:100vh;min-height:100vh}.main-content{margin:8rem auto;padding-left:1.5rem;max-width:60rem}@media (width <= 720px){.main-content{margin-top:4rem}}.h2{line-height:2.25rem;font-size:1.5rem;font-weight:500}@media (width <= 720px){.h2{line-height:1.5rem;font-size:1.25rem}}#challenge-error-text{background-image:url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgZmlsbD0ibm9uZSI+PHBhdGggZmlsbD0iI0IyMEYwMyIgZD0iTTE2IDNhMTMgMTMgMCAxIDAgMTMgMTNBMTMuMDE1IDEzLjAxNSAwIDAgMCAxNiAzbTAgMjRhMTEgMTEgMCAxIDEgMTEtMTEgMTEuMDEgMTEuMDEgMCAwIDEtMTEgMTEiLz48cGF0aCBmaWxsPSIjQjIwRjAzIiBkPSJNMTcuMDM4IDE4LjYxNUgxNC44N2wxNC41NjMgOS41aDIuNzgzem0tMS4wODQgMS40MjdxLjY2IDAgMS4wNTcuMzg4LjQwNy4zODkuNDA3Ljk5NCAwIC41OTYtLjQwNy45ODQtLjM5Ny4zOS0xLjA1Ny4zODktLjY1IDAtMS4wNTYtLjM4OS0uMzk4LS4zODktLjM5OC0uOTg0IDAtLjU5Ny4zOTgtLjk4NS40MDYtLjM5NyAxLjA1Ni0uMzk3Ii8+PC9zdmc+");background-repeat:no-repeat;background-size:contain;padding-left:34px}@media (prefers-color-scheme: dark){body{background-color:#222;color:#d9d9d9}}</style><meta http-equiv="refresh" content="360"></head><body><div class="main-wrapper" role="main"><div class="main-content"><noscript><div class="h2"><span id="challenge-error-text">Enable JavaScript and cookies to continue</span></div></noscript></div></div><script>(function(){window._cf_chl_opt = {cvId: '3',cZone: 'cf.2hg.com',cType: 'managed',cRay: '9d32ac9fee393dc4',cH: '5u3TW_efTqFDp52.eJ7iJIAUrdHuJc1vKOIFl1547yE-1771975024-1.2.1.1-wjiSkq852rn2iH685Pm2rBmJELiMv7IMiPwP7k4VXCMot0obvdNH3kjRilBQTbu7',cUPMDTk:"\/?action=mc&__cf_chl_tk=JKKz6SJtAonvXAIjfkSgrf_IpbPA7w3hKyJHBmUo3Us-1771975024-1.0.1.1-GJjB3.RT8tU_rW3RaDJ0BhuXfsRBbcF04UuT6FBuuPc",cFPWv: 'b',cITimeS: '1771975024',cTplC:0,cTplV:5,cTplB: '0',fa:"\/?action=mc&__cf_chl_f_tk=JKKz6SJtAonvXAIjfkSgrf_IpbPA7w3hKyJHBmUo3Us-1771975024-1.0.1.1-GJjB3.RT8tU_rW3RaDJ0BhuXfsRBbcF04UuT6FBuuPc",md: 'EH52FXHuIbOFG76Qh8JMvqrD_CN9ox.CDavzTgGb1s8-1771975024-1.2.1.1-mbyWoPaKV2XTanqDMuRTx0_oeKGavCvAtmrbBjbWydMfXRJ97uKuYm.8TsDg6_Us5UF8oIWCgvCq8pYm48S_66QJYY0azmqE5MyDOjS022uMVxBUG5kyIr6ahL8g_mEtxf.VxP5Uhms89gGiXj2EgZByRlkCWONtrmSo6oGtX.L6Cni0p4kOyPniSAgmL5Tt2zlpAG9ZpHRnS22l02jF2c2lBZqTCP5su5nKy0ACgzeqOLJRn2YxvNm8m4PEWheMTLl1GA3zaefXH2y4ZeyVsH9GDM5iDFrUQc9EKR4uAL4shfrD7Oo4a9lpnvr_fgRqKv2qjOI834Hv4APJSCrWtzdggioMEbNW5nfyxgQAKvLr1AkpsbEV6EO5G3AQeWQUe_DhERzZEMvhOhtJZ6MnRO816oIR6SwOKUEFvvN5J91qApRdxjRwWHdPQroyi7IiZdmRDopWU_K55eV3oJmZ_5QF3DEljaAYSas5BkRLUsQujVzaRSkdqM_oFx6m6WgVx.OhC7RNvapDJ3GOSzt4s9bNk4z7ofFoyfv1VkJJYAVdJqcWvRY1g7qLw_dw5O92Vy7_FYap4JeGevHNKMbH92hMMm7bdht1K8wdB56SVvjnUCuFH92Q92whzgXLEqGVWmWCyJnqK0_2pkndYx0ykbFnMFXQU3JIxTYjRfhDX8EG7SMQw_SDwxbYZtQPxDl.SpYurHcL_miP5mFhaD_g6hrNEI64RrxYcsEztE2xV8_hUOeZFM1TU61.NArL7i4YP2o6elFaQDWk.rt1b9MRPOF__ajuW_cZjG8534WabiQeM.YAAhY7gmMMeuIkCfbSrD2qjukf89BFINlNKX4LytH.pUmRMqETcdvLrgsdVJ7gqGZE_shw9tIHgCYn9v6sbhgYFox8qbHrgYEJcCZXy0kVb6IaGyQ5Nvb5kE8kexKcfn2JYI59DnuAvVOfCXpHm0HAO4JVQo4aO3aDfxeIKzT6Ox0nQj.ozR6MCEWA_S98NEoa9kEPdsySald_oaCQnDx_Wlu5qESjmA1G6QAsdw',mdrd: 'DRoeBgoNLqwwa.UCy.2tKj7UAV4X8BXcf8glkXG54UY-1771975024-1.2.1.1-j27p4gxvh8vjVP59ofi8zi.MpNIQuvlO7nmaF_48tMDUfGsZiRajT9P4h1_4VNAO1sLyNtcffFnAK8oH.jV3KiWqSfU4f1EhCTURpfFcCw0H5Qt.93hMuL.dovBxICtryqgKVnt6H4OweHzFzaIAUeL.uWtc83wTPWNekGIwBhW6qNJS3SexI34nkxIHcFpYTiVN6GzYn_ddfknI_rdNjNp32nTJZyjodfgs9J2SwvOKY5ybcLC0kzEtRqSKfmQbCzonBbI4s527gY_ZV.LvWURP0duVLESprq.HPpA0sUYwZF0q476S4gW8TpBzopPzWdEgcwl.c6z2DnmcurcwnlvwvwbirfM6nsbZanDrO2ttsNyOP2iE23v4s60C2PE7BchCVW8hL3ktoRHtz2WBKchekb4C7sNbBDmR_y6QHWndHqU3fxwtZJhrdlR14SlFmRBDfcCcgksfeOSlzTYL9iIvogWXE4tK1VKECWdPHFoy3DOJo66snliKB5XBusRLvNJSguzaho3q8ePcXL585qSQa78Uyexvbm6X.K42XJvctfuuLGxLSDqnuRoTj8TsYPHlvajOU0e1o1P_xSQ8tq2_IS4L6RQRT2H7tICVXu41klsvM7o.bN6qxmUJ1V3tgvh_Dm9IOjpPPCvSliAhbcQQSzXZuwv_GWDctlkN373T_fGNK7VQ6Jj6_fndj_apc.FtPpQm2eYNYinQ9dmAPMrV8uLrM1BRawW.XKV6YEXdPRhN_OmA9XnVvvzzrh6vQ1YvYHfvw9ZSsAoLBvmAYZs9gK5uq35T5E21r1KLS0d1wNG5SkctUKK22YA7imQ6luMWqz1VnFmHsUEW5ZFWZgSyoxTlUK7PhNJY_O3rK7dOhMrwFFYP5zv9Qnls4J0uiKZJKvxs.rYZydSZrsdJvZPR5Tlu0dNRiDyEtJxg9vbvqMXBkR11IEjKM5EFxTqXCHDqqWJiFAB1EBlwNPXND2BCBtcJAoT1zIsZZWf_ppRqV8PmC.Efli7p.lKVKEhpuTzlo1U9TonC_BnhQNSMLRIHeY4RDBpwXaOfhgl2rYzNSp2JPBOf5yrXkMeM3yc4Sns7w4tigemjtQIVTVMYidQUs3T49XZjzCiDUoS6RJM8CLtjZjCbp4E7iJSIKzMfi5o56CTbBvpYYaB7dbVUhhJWUsi7b47Uh.DMzGoYUuwF41msKTGP4dSc1Kdq.UJQDFYY8FJ4Pm5YwGdIT_n_pILvVrxdtbY4BHEWakxJ3NJrTodKbb3F17NF5Nexrcr4QkeTgiZTh91HdWmUSMwht1PeepTpqNunmJewoD1lXSN38ernInE5wGpDmiC8ebLCESH8mfQ23xwcPjQDdcVUQ5eFUhAFT3a5vkAJmdcgBhx5X0G0uqu721lxeUw_05i2a4fh3z4mdYBLBS9FCTiL1xYzIxzN5B5Qy6Pr2LyFcCCx9xdpCjaLTkzbd0sbYSKBGFUJCjZITJo40urQDHJ0clyzAWKFx11QjaZ8o16XOEa0NUv6f2GfUeGPeqhhfk.QjYc3VDHvSas_E6iaqnyJlsXh5n.D_BBolrNQp8Ng4FRqMrZV8DN0aZsEX_1mJnZ._O9SqdDpa3mjPgdUx_9r51joOUkwfWxWL__YnW_diH3r.s8KPMo3KCJhNFFTH6tpa_GJ6QWx_yXTPLf0l3OCUlxdRgbj6xyvnluNX4lRlLdyRrAbW_J7Nk11agzTi1lWNPCLnXcDug1HrgsvdABR7aGq9Y60Z_lGO.xJ3McErvGXJ7IV1VPGGfX8qNfNeN9RaACMWzn8YroyUwZlTANTjtuHLtkDs42x0ezQ1l5uDD.Dwa6ypUGrnvw39V0zc_ZT5Ps7cJyS094_d0Fy85IR6d5CtEAqzOPzaET8P.yzlJOzf5wHEocDLbW00dQzh