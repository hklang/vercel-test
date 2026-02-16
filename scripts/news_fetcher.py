#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日新闻推送 - 新闻获取模块
支持多个新闻源，自动切换
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time

# 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

class NewsFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.news_list = []
    
    def fetch_sina_news(self):
        """获取新浪新闻"""
        try:
            # 新浪新闻移动端
            url = 'https://news.sina.com.cn/'
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找新闻标题
            headlines = []
            for item in soup.find_all(['a', 'h1', 'h2', 'h3']):
                text = item.get_text(strip=True)
                if len(text) > 10 and len(text) < 80:
                    # 过滤掉导航、广告等
                    if not any(kw in text for kw in ['登录', '注册', '客户端', '专题', '视频', '图片', '财经', '体育', '娱乐']):
                        if '疫情' not in text and '肺炎' not in text:  # 过滤过时关键词
                            headlines.append(text)
            
            # 去重并取前10条
            headlines = list(dict.fromkeys(headlines))[:10]
            return headlines
        except Exception as e:
            print(f"新浪新闻获取失败: {e}")
            return []
    
    def fetch_tengxun_news(self):
        """获取腾讯新闻"""
        try:
            url = 'https://news.qq.com/'
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            headlines = []
            for item in soup.find_all(['a', 'h1', 'h2', 'h3']):
                text = item.get_text(strip=True)
                if len(text) > 10 and len(text) < 80:
                    if not any(kw in text for kw in ['登录', '注册', '客户端', '专题', '广告']):
                        headlines.append(text)
            
            headlines = list(dict.fromkeys(headlines))[:10]
            return headlines
        except Exception as e:
            print(f"腾讯新闻获取失败: {e}")
            return []
    
    def fetch_ifeng_news(self):
        """获取凤凰网新闻"""
        try:
            url = 'https://news.ifeng.com/'
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            headlines = []
            for item in soup.find_all(['a', 'h1', 'h2', 'h3']):
                text = item.get_text(strip=True)
                if len(text) > 10 and len(text) < 80:
                    if not any(kw in text for kw in ['登录', '注册', '客户端', '专题', '广告', '视频']):
                        headlines.append(text)
            
            headlines = list(dict.fromkeys(headlines))[:10]
            return headlines
        except Exception as e:
            print(f"凤凰网新闻获取失败: {e}")
            return []
    
    def fetch_163_news(self):
        """获取网易新闻"""
        try:
            url = 'https://news.163.com/'
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            headlines = []
            for item in soup.find_all(['a', 'h1', 'h2', 'h3']):
                text = item.get_text(strip=True)
                if len(text) > 10 and len(text) < 80:
                    if not any(kw in text for kw in ['登录', '注册', '客户端', '专题', '广告', '跟帖']):
                        headlines.append(text)
            
            headlines = list(dict.fromkeys(headlines))[:10]
            return headlines
        except Exception as e:
            print(f"网易新闻获取失败: {e}")
            return []
    
    def get_news(self):
        """获取新闻（多源聚合）"""
        print("开始获取新闻...")
        
        # 尝试多个新闻源
        sources = [
            ('新浪新闻', self.fetch_sina_news),
            ('腾讯新闻', self.fetch_tengxun_news),
            ('凤凰网', self.fetch_ifeng_news),
            ('网易新闻', self.fetch_163_news),
        ]
        
        all_news = []
        for source_name, fetch_func in sources:
            print(f"正在获取 {source_name}...")
            try:
                news = fetch_func()
                if news:
                    for item in news:
                        all_news.append({
                            'source': source_name,
                            'title': item,
                            'time': datetime.now().strftime('%H:%M')
                        })
                time.sleep(1)  # 避免请求过快
            except Exception as e:
                print(f"{source_name} 获取异常: {e}")
        
        # 去重（按标题）
        seen = set()
        unique_news = []
        for item in all_news:
            title = item['title']
            if title not in seen:
                seen.add(title)
                unique_news.append(item)
        
        # 按来源分组
        result = {
            'time': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'count': len(unique_news),
            'news': unique_news[:20]  # 最多20条
        }
        
        return result

def main():
    fetcher = NewsFetcher()
    result = fetcher.get_news()
    
    # 输出JSON格式供其他程序使用
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    return result

if __name__ == '__main__':
    main()
