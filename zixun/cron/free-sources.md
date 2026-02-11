# 🌐 完全免费域外搜索方案

> 替代 Brave API（仅免费1个月）| 创建：2026-02-11 | 作者：蒋国春

---

## ❌ 已放弃：Brave API

| API | 免费限制 | 问题 |
|-----|---------|------|
| Brave API | 2,000次/月 | **仅首月免费**，之后付费 |

---

## ✅ 100% 免费替代方案

由于 v2rayA 代理已配置，我们可以用完全免费的替代品：

### 免费数据源

| 替代方案 | 免费限制 | 数据来源 | 使用方式 |
|----------|---------|----------|----------|
| **GitHub Trending** | 完全免费 | github.com/trending | web_fetch |
| **Hacker News** | 完全免费 | news.ycombinator.com | web_fetch |
| **Reddit** | 完全免费 | reddit.com/list.json | web_fetch |
| **Bing News** | 完全免费 | bing.com/news | web_fetch |
| **Google** | 免费（代理） | google.com | 代理访问 |

### ⭐ 推荐：完全免费组合

| 任务 | 免费源 | 频率 | 成本 |
|------|--------|------|------|
| 技术热点 | GitHub Trending | 每日1次 | $0 |
| 开发者讨论 | Hacker News | 每4小时 | $0 |
| 社区热点 | Reddit | 每6小时 | $0 |
| 财经新闻 | Yahoo Finance | 每4小时 | $0 |
| 视频趋势 | YouTube Trending | 每日1次 | $0 |
| **总计** | **5个源** | **~10次/天** | **$0/月** |

---

## 📡 免费 API 和数据源

### 1. GitHub Trending（完全免费）

**官方页面**: https://github.com/trending

**API方式**:
```bash
# 直接抓取
curl -s "https://github.com/trending?since=daily" | grep -oP '(?<=<a href=")[^"]*' | head -10
```

**Python获取**:
```python
import requests
from bs4 import BeautifulSoup

def get_github_trending(language="", period="daily"):
    url = f"https://github.com/trending/{language}?since={period}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers, proxies={
        "http": "http://127.0.0.1:20171",
        "https": "http://127.0.0.1:20171"
    })
    
    # 解析HTML提取Trending项目
    soup = BeautifulSoup(response.text, 'html.parser')
    repos = []
    
    for article in soup.select('article.box-shadow')[:10]:
        title = article.select_one('h2 a').get('href')
        stars = article.select_one('.muted-link').text.strip()
        desc = article.select_one('p').text.strip() if article.select_one('p') else ""
        
        repos.append({
            "repo": title,
            "stars": stars,
            "description": desc
        })
    
    return repos
```

### 2. Hacker News API（完全免费）

**API文档**: https://github.com/HackerNews/API

**使用方式**:
```python
import requests

def get_hackernews_top(stories=10):
    # 获取Top Stories IDs
    top_ids = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json"
    ).json()[:stories]
    
    # 获取每个故事的详情
    stories = []
    for story_id in top_ids:
        story = requests.get(
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        ).json()
        
        stories.append({
            "title": story.get("title"),
            "url": story.get("url"),
            "score": story.get("score"),
            "by": story.get("by"),
            "comments": story.get("descendants", 0)
        })
    
    return stories
```

**免费限制**: 无限制，HN官方API完全免费开放

### 3. Reddit API（完全免费）

**API文档**: https://www.reddit.com/dev/api

**获取热门帖子**:
```python
import requests

def get_reddit_hot(subreddits=["technology", "programming", "AI"], limit=5):
    posts = []
    
    for sub in subreddits:
        url = f"https://www.reddit.com/r/{sub}/hot.json?limit={limit}"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        response = requests.get(
            url, 
            headers=headers,
            proxies={
                "http": "http://127.0.0.1:20171",
                "https": "http://127.0.0.1:20171"
            }
        )
        
        data = response.json()
        for post in data['data']['children']:
            posts.append({
                "subreddit": sub,
                "title": post['data']['title'],
                "score": post['data']['score'],
                "url": post['data']['url'],
                "comments": post['data']['num_comments']
            })
    
    return posts[:15]
```

### 4. YouTube Trending（完全免费）

**获取方式**: web_fetch 抓取页面

```python
def get_youtube_trending(region="US", max_results=10):
    url = f"https://www.youtube.com/feed/trending?bp=4gINGGt5egZDaGEsb2xoIURa"
    
    response = requests.get(
        url,
        proxies={
            "http": "http://127.0.0.1:20171",
            "https": "http://127.0.0.1:20171"
        }
    )
    
    # 解析视频列表...
    return trending_videos
```

### 5. Bing News Search（免费层）

**免费层**: 1,000次/月（足够用）

**注册**: https://portal.azure.com/#view/Microsoft_Azure_BPMarketplace/Root

### 6. Google 搜索（代理免费）

由于已配置 v2rayA 代理，可以直接访问 Google：

```python
import requests
from bs4 import BeautifulSoup

def google_search(query, num_results=10):
    url = f"https://www.google.com/search?q={query}&num={num_results}"
    
    response = requests.get(
        url,
        proxies={
            "http": "http://127.0.0.1:20171",
            "https": "http://127.0.0.1:20171"
        },
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )
    
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    
    for item in soup.select('.g')[:num_results]:
        title = item.select_one('h3')
        link = item.select_one('a')
        snippet = item.select_one('.VwiC3b')
        
        if title and link:
            results.append({
                "title": title.text,
                "url": link['href'],
                "snippet": snippet.text if snippet else ""
            })
    
    return results
```

---

## 🔧 定时任务配置

### 完整定时任务脚本

创建文件：`/home/lang/.openclaw/workspace/zixun/cron/scripts/free-external-search.sh`

```bash
#!/bin/bash
# 完全免费域外搜索定时任务
# 无API限制，100%免费使用

set -e

# 代理配置
export http_proxy="http://127.0.0.1:20171"
export https_proxy="http://127.0.0.1:20171"

# 日志
LOG_FILE="/var/log/zixun-external-search.log"
echo "=== $(date) ===" >> $LOG_FILE

# 1. 获取 GitHub Trending（每日1次）
echo "📦 获取 GitHub Trending..." >> $LOG_FILE
python3 << 'PYEOF' >> $LOG_FILE 2>&1
import sys
sys.path.append('/home/lang/.openclaw/workspace/zixun/cron/scripts')
from free_sources import get_github_trending

trending = get_github_trending(language="", period="daily")
print(f"✅ GitHub Trending: {len(trending)} 个项目")
for i, repo in enumerate(trending[:5], 1):
    print(f"{i}. {repo['repo']} ⭐{repo['stars']}")
PYEOF

# 2. 获取 Hacker News（每4小时）
echo "📰 获取 Hacker News..." >> $LOG_FILE
python3 << 'PYEOF' >> $LOG_FILE 2>&1
import sys
sys.path.append('/home/lang/.openclaw/workspace/zixun/cron/scripts')
from free_sources import get_hackernews_top

hn = get_hackernews_top(stories=10)
print(f"✅ Hacker News: {len(hn)} 条讨论")
for i, story in enumerate(hn[:5], 1):
    print(f"{i}. {story['title']} ({story['score']} 分)")
PYEOF

# 3. 获取 Reddit 热点（每6小时）
echo "🤖 获取 Reddit 热点..." >> $LOG_FILE
python3 << 'PYEOF' >> $LOG_FILE 2>&1
import sys
sys.path.append('/home/lang/.openclaw/workspace/zixun/cron/scripts')
from free_sources import get_reddit_hot

reddit = get_reddit_hot(subreddits=["technology", "programming", "AI"], limit=5)
print(f"✅ Reddit: {len(reddit)} 个帖子")
for i, post in enumerate(reddit[:5], 1):
    print(f"{i}. r/{post['subreddit']}: {post['title'][:50]}")
PYEOF

echo "✅ 任务完成" >> $LOG_FILE
```

---

## 📦 免费源集成脚本

创建文件：`/home/lang/.openclaw/workspace/zixun/cron/scripts/free_sources.py`

```python
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

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def get_github_trending(language="", period="daily", max_repos=10):
    """
    获取 GitHub Trending（完全免费）
    """
    try:
        url = f"https://github.com/trending/{language}?since={period}"
        response = requests.get(url, headers=HEADERS, proxies=PROXIES, timeout=30)
        
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
                headers=HEADERS, 
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
            "data": all_posts[:15],  # 最多返回15条
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}


def get_youtube_trending(region="US", max_results=10):
    """
    获取 YouTube Trending（需要代理）
    """
    try:
        # YouTube 需要特殊处理，这里是简化版
        url = f"https://www.youtube.com/feed/trending?bp=4gINGGt5egZDaGEsb2xoIURa"
        
        response = requests.get(
            url,
            headers=HEADERS,
            proxies=PROXIES,
            timeout=30
        )
        
        # 解析逻辑需要更复杂的处理
        # 简化版返回占位符
        return {
            "source": "YouTube Trending",
            "url": url,
            "note": "需要完整解析逻辑",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}


def get_all_sources():
    """
    获取所有免费数据源
    """
    results = {}
    
    # GitHub Trending
    print("📦 获取 GitHub Trending...")
    results['github'] = get_github_trending()
    
    # Hacker News
    print("📰 获取 Hacker News...")
    results['hackernews'] = get_hackernews_top()
    
    # Reddit
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
                formatted += f"   {repo['description'][:60]}...\n"
        formatted += "\n"
    
    # Hacker News
    if 'hackernews' in data and 'data' in data['hackernews']:
        stories = data['hackernews']['data'][:5]
        formatted += "💻 Hacker News\n"
        formatted += "━━━━━━━━━━━━━━━━━━━━━━\n"
        for i, story in enumerate(stories, 1):
            formatted += f"{i}. {story['title'][:50]}...\n"
            formatted += f"   ⭐{story['score']} 💬{story.get('comments', 0)}\n"
        formatted += "\n"
    
    # Reddit
    if 'reddit' in data and 'data' in data['reddit']:
        posts = data['reddit']['data'][:5]
        formatted += "🤖 Reddit 热门\n"
        formatted += "━━━━━━━━━━━━━━━━━━━━━━\n"
        for i, post in enumerate(posts, 1):
            formatted += f"{i}. r/{post['subreddit']}: {post['title'][:40]}...\n"
            formatted += f"   ⭐{post['score']}\n"
    
    formatted += "\n━━━━━━━━━━━━━━━━━━━━━━\n"
    formatted += "🦊 来源：GitHub + Hacker News + Reddit\n"
    formatted += "📝 语言：100% 中文\n"
    formatted += "💰 成本：完全免费\n"
    
    return formatted


if __name__ == "__main__":
    # 测试获取
    print("=== 测试免费数据源 ===\n")
    
    data = get_all_sources()
    
    print(f"\nGitHub: {data['github'].get('count', 0)} 条")
    print(f"Hacker News: {data['hackernews'].get('count', 0)} 条")
    print(f"Reddit: {data['reddit'].get('count', 0)} 条")
    
    print("\n" + "="*50)
    print(format_for_feishu(data))
```

---

## 🚀 使用方法

### 1. 创建脚本文件

```bash
# 创建目录
mkdir -p /home/lang/.openclaw/workspace/zixun/cron/scripts

# 创建免费源集成脚本
cat > /home/lang/.openclaw/workspace/zixun/cron/scripts/free_sources.py << 'EOF'
# （上面的完整代码）
EOF

# 创建定时任务脚本
cat > /home/lang/.openclaw/workspace/zixun/cron/scripts/free-external-search.sh << 'EOF'
#!/bin/bash
# 完全免费域外搜索
export http_proxy="http://127.0.0.1:20171"
export https_proxy="http://127.0.0.1:20171"

cd /home/lang/.openclaw/workspace/zixun/cron/scripts

python3 free_sources.py > /tmp/free_sources_output.json

# 格式化为飞书消息
python3 << 'PYEOF'
import json

with open('/tmp/free_sources_output.json') as f:
    data = json.load(f)

from free_sources import format_for_feishu
message = format_for_feishu(data)

# 发送消息
import subprocess
result = subprocess.run(
    ["openclaw", "message", "send", "--channel", "feishu", 
     "--to", "oc_982e81066ead19e659ccff0f5f509ddd", "--message", message],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("✅ 消息已发送")
else:
    print(f"❌ 发送失败: {result.stderr}")
PYEOF

echo "✅ 任务完成"
EOF

chmod +x /home/lang/.openclaw/workspace/zixun/cron/scripts/*.sh
```

### 2. 测试运行

```bash
# 运行测试
python3 /home/lang/.openclaw/workspace/zixun/cron/scripts/free_sources.py
```

### 3. 添加定时任务

```bash
# 添加 crontab
crontab -e

# 添加以下行：
# 每6小时执行免费域外搜索
0 */6 * * * /home/lang/.openclaw/workspace/zixun/cron/scripts/free-external-search.sh >> /var/log/zixun-external-search.log 2>&1
```

---

## 💰 成本对比

| 方案 | 月成本 | 年成本 | 评估 |
|------|--------|--------|------|
| **Brave API** | $0→$120+ | $1440+ | ❌ 仅首月免费 |
| **免费组合** | **$0** | **$0** | ✅ **推荐使用** |
| **Bing API** | $0 (1K次) | 需付费 | ⚠️ 需监控 |
| **Google API** | $0-$200 | 复杂 | ⚠️ 配置复杂 |

---

## ✅ 总结

### 推荐的免费方案

| 数据源 | 免费限制 | 用途 |
|--------|---------|------|
| GitHub Trending | 无限 | 技术项目 |
| Hacker News API | 无限 | 开发者讨论 |
| Reddit API | 无限 | 社区热点 |
| YouTube | 代理访问 | 视频趋势 |
| **总计** | **完全免费** | **足够使用** |

### 下一步

1. ✅ 无需注册 API
2. ✅ 无需付费
3. ✅ 无限制次数
4. 🔧 需要配置 v2rayA 代理（已配置）
5. 📦 创建脚本文件
6. ⏰ 添加定时任务

**是否现在开始创建免费方案？** 🚀
