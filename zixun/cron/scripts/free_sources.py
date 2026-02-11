#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
免费数据源集成脚本
100% 免费，无API限制
"""

import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 代理配置
PROXIES = {
    "http": "http://127.0.0.1:20171",
    "https": "http://127.0.0.1:20171"
}

# GitHub headers
HEADERS_GITHUB = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# Reddit headers (需要更完整)
HEADERS_REDDIT = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.reddit.com/"
}


def get_github_trending(language="", period="daily", max_repos=10):
    """
    获取 GitHub Trending（完全免费）
    """
    try:
        url = f"https://github.com/trending/{language}?since={period}"
        response = requests.get(url, headers=HEADERS_GITHUB, proxies=PROXIES, timeout=30)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        repos = []
        
        for article in soup.select('article.box-shadow')[:max_repos]:
            try:
                repo_link = article.select_one('h2 a')
                if repo_link:
                    full_repo = repo_link.get('href', '').strip('/')
                    stars = article.select_one('.muted-link').text.strip() if article.select_one('.muted-link') else "0"
                    desc = ""
                    if article.select_one('p'):
                        desc = article.select_one('p').text.strip()
                    language = article.select_one('[itemprop="programmingLanguage"]')
                    lang = language.text if language else "Unknown"
                    
                    repos.append({
                        "repo": full_repo,
                        "stars": stars,
                        "description": desc,
                        "language": lang
                    })
            except Exception as e:
                continue
        
        return {
            "source": "GitHub Trending",
            "url": url,
            "count": len(repos),
            "data": repos,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}


def get_hackernews_top(stories=10):
    """
    获取 Hacker News Top Stories（完全免费）
    API: https://github.com/HackerNews/API
    """
    try:
        # 获取Top Stories IDs
        top_ids_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        top_ids = requests.get(top_ids_url, timeout=30).json()[:stories]
        
        stories_data = []
        for story_id in top_ids:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story = requests.get(story_url, timeout=30).json()
            
            if story:
                stories_data.append({
                    "title": story.get("title", ""),
                    "url": story.get("url", ""),
                    "score": story.get("score", 0),
                    "by": story.get("by", ""),
                    "comments": story.get("descendants", 0),
                    "hn_id": story_id
                })
        
        return {
            "source": "Hacker News",
            "url": "https://news.ycombinator.com/",
            "count": len(stories_data),
            "data": stories_data,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}


def get_reddit_hot(subreddits=["technology", "programming", "AI"], limit_per_sub=5):
    """
    获取 Reddit 热门帖子（完全免费）
    """
    try:
        all_posts = []
        
        for sub in subreddits:
            url = f"https://www.reddit.com/r/{sub}/hot.json?limit={limit_per_sub}"
            response = requests.get(
                url, 
                headers=HEADERS_REDDIT, 
                proxies=PROXIES,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                for post in data['data']['children']:
                    post_data = post['data']
                    all_posts.append({
                        "subreddit": sub,
                        "title": post_data.get("title", ""),
                        "url": f"https://reddit.com{post_data.get('permalink', '')}",
                        "score": post_data.get("score", 0),
                        "comments": post_data.get("num_comments", 0),
                        "upvote_ratio": post_data.get("upvote_ratio", 0)
                    })
        
        return {
            "source": "Reddit",
            "url": "https://www.reddit.com/",
            "count": len(all_posts),
            "data": all_posts[:15],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}


def get_all_sources():
    """
    获取所有免费数据源
    """
    results = {}
    
    print("📦 获取 GitHub Trending...")
    results['github'] = get_github_trending()
    
    print("📰 获取 Hacker News...")
    results['hackernews'] = get_hackernews_top()
    
    print("🤖 获取 Reddit...")
    results['reddit'] = get_reddit_hot()
    
    return results


def format_for_feishu(data):
    """
    格式化数据为飞书推送模板
    """
    formatted = "🌍 域外资讯 · 全球视野\n"
    formatted += "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    # GitHub Trending
    if 'github' in data and 'data' in data['github']:
        repos = data['github']['data'][:5]
        formatted += "🔧 GitHub Trending\n"
        formatted += "━━━━━━━━━━━━━━━━━━━━━━\n"
        for i, repo in enumerate(repos, 1):
            formatted += f"{i}. {repo['repo']} ⭐{repo['stars']}\n"
            if repo.get('description'):
                desc = repo['description'][:60] + "..." if len(repo['description']) > 60 else repo['description']
                formatted += f"   {desc}\n"
        formatted += "\n"
    
    # Hacker News
    if 'hackernews' in data and 'data' in data['hackernews']:
        stories = data['hackernews']['data'][:5]
        formatted += "💻 Hacker News\n"
        formatted += "━━━━━━━━━━━━━━━━━━━━━━\n"
        for i, story in enumerate(stories, 1):
            title = story['title'][:50] + "..." if len(story['title']) > 50 else story['title']
            formatted += f"{i}. {title}\n"
            formatted += f"   ⭐{story['score']} 💬{story.get('comments', 0)}\n"
        formatted += "\n"
    
    # Reddit
    if 'reddit' in data and 'data' in data['reddit']:
        posts = data['reddit']['data'][:5]
        formatted += "🤖 Reddit 热门\n"
        formatted += "━━━━━━━━━━━━━━━━━━━━━━\n"
        for i, post in enumerate(posts, 1):
            title = post['title'][:40] + "..." if len(post['title']) > 40 else post['title']
            formatted += f"{i}. r/{post['subreddit']}: {title}\n"
            formatted += f"   ⭐{post['score']}\n"
    
    formatted += "\n━━━━━━━━━━━━━━━━━━━━━━\n"
    formatted += "🦊 来源：GitHub + Hacker News + Reddit\n"
    formatted += "📝 语言：100% 中文\n"
    formatted += "💰 成本：完全免费 ✅\n"
    
    return formatted


if __name__ == "__main__":
    print("=== 测试免费数据源 ===\n")
    
    data = get_all_sources()
    
    print(f"\nGitHub: {data['github'].get('count', 0)} 条")
    print(f"Hacker News: {data['hackernews'].get('count', 0)} 条")
    print(f"Reddit: {data['reddit'].get('count', 0)} 条")
    
    print("\n" + "="*50)
    print(format_for_feishu(data))
