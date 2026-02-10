# 🌐 域外搜索配置

> 外部搜索引擎和信息网址配置 | 创建：2026-02-10

---

## 🔍 搜索引擎配置

### Google (通过 Brave API)
- **用途**: 综合热点搜索、Google Trends
- **方法**: `web_search` (Brave Search API)
- **特点**: 支持语言过滤、区域设置、 freshness 筛选

### Bing
- **用途**: 微软搜索结果补充
- **方法**: `web_search`
- **特点**: 新闻、图片、视频分类搜索

---

## 💻 国际信息网站列表

### 科技资讯
| 网站 | URL | 用途 |
|------|-----|------|
| Hacker News | https://news.ycombinator.com/ | 技术社区热门讨论 |
| TechCrunch | https://techcrunch.com/ | 科技新闻报道 |
| The Verge | https://www.theverge.com/ | 科技产品/文化 |
| Wired | https://www.wired.com/ | 科技深度报道 |
| Arxiv | https://arxiv.org/ | AI/ML学术论文 |

### 社交热门
| 网站 | URL | 用途 |
|------|-----|------|
| Reddit | https://www.reddit.com/ | 社区讨论热点 |
| YouTube Trending | https://www.youtube.com/feed/trending | 热门视频 |
| Twitter/X Trending | https://twitter.com/explore | 实时热门话题 |

### 财经数据
| 网站 | URL | 用途 |
|------|-----|------|
| TradingView | https://www.tradingview.com/ | 金融市场图表 |
| Bloomberg | https://www.bloomberg.com/ | 商业财经新闻 |
| Reuters | https://www.reuters.com/ | 国际新闻通讯社 |

### 代码社区
| 网站 | URL | 用途 |
|------|-----|------|
| GitHub Trending | https://github.com/trending | 开源项目热点 |
| Product Hunt | https://www.producthunt.com/ | 新产品发布 |

### 数据统计
| 网站 | URL | 用途 |
|------|-----|------|
| Our World in Data | https://ourworldindata.org/ | 全球数据可视化 |
| Google Trends | https://trends.google.com/ | 搜索趋势分析 |

---

## 🔑 搜索关键词模板

### 科技AI类（每日必搜）
```json
[
  "GPT-5",
  "GPT-4",
  "Claude 3",
  "Gemini AI",
  "OpenAI",
  "Anthropic",
  "LLM",
  "AGI",
  "Machine Learning",
  "Deep Learning",
  "Neural Network",
  "AI breakthrough",
  "AI news 2024"
]
```

### 商业财经类
```json
[
  "stock market",
  "NASDAQ",
  "S&P 500",
  "Tesla stock",
  "Apple earnings",
  "cryptocurrency",
  "Bitcoin price",
  "Ethereum",
  "FinTech"
]
```

### 热门趋势类
```json
[
  "viral video",
  "trending topic",
  "breaking news",
  "popular",
  "most shared"
]
```

### 开发者工具类
```json
[
  "GitHub trending",
  "open source project",
  "new programming language",
  "developer tool",
  "framework release"
]
```

---

## ⏰ 定时搜索时间表

| 时间 | 搜索重点 | 搜索内容 |
|------|----------|----------|
| **0:00** | 前日总结 | 前24小时全球热点汇总 |
| **6:00** | 凌晨动态 | 深夜至凌晨的国际动态 |
| **12:00** | 午间扫描 | 当日上午全球热点 |
| **18:00** | 晚间汇总 | 全天域外资讯总结 |

---

## 📊 输出格式模板

### 格式1：Google Trends 热点
```
🔍 Google Trends 热点
━━━━━━━━━━━━━━━━━━━━
🌍 全球 Top 5
1. 热点话题1 (地区: 全球)
2. 热点话题2 (地区: 美国)
3. 热点话题3 (地区: UK)
...

📈 上升趋势
• 话题A (↑ 500%)
• 话题B (↑ 200%)
```

### 格式2：Hacker News
```
💻 Hacker News Top 10
━━━━━━━━━━━━━━━━━━━━━━
1. 标题1 (分数: 520)
   链接: https://...
   标签: [AI, Startup]

2. 标题2 (分数: 480)
   链接: https://...
   标签: [DevOps, Cloud]
```

### 格式3：Reddit 热门
```
🤖 Reddit 热门讨论
━━━━━━━━━━━━━━━━━━━
r/all Top 3
• 帖子标题1 ( upvotes: 25k )
• 帖子标题2 ( upvotes: 20k )

r/technology
• 讨论标题 ( upvotes: 15k )

r/AI
• 讨论标题 ( upvotes: 12k )
```

### 格式4：GitHub Trending
```
🔧 GitHub Trending
━━━━━━━━━━━━━━━━━━
📈 今日 Top 5
1. 项目名/仓库 (⭐ 2.5k)
   描述：一句话介绍
   语言：TypeScript

2. 项目名/仓库 (⭐ 1.8k)
   描述：一句话介绍
   语言：Python
```

### 格式5：AI/科技前沿
```
🧠 AI/科技前沿
━━━━━━━━━━━━━━━━
📰 最新动态
• 标题：重大突破/产品发布
  来源：媒体名
  摘要：...

📚 Arxiv 热门论文
1. 论文标题 (⭐ stars)
   链接：arxiv.org/...

2. 论文标题 (⭐ stars)
   链接：arxiv.org/...
```

---

## 🔧 使用方法

### 1. 手动执行搜索
```bash
# 搜索Google Trends
openclaw web_search --query "GPT-5 news" --count 10 --freshness "pw"

# 获取Hacker News
# 直接访问 https://news.ycombinator.com/

# 搜索Reddit
openclaw web_search --query "AI breakthrough reddit" --count 10
```

### 2. 添加定时任务
```bash
# 域外搜索定时任务（每6小时）
openclaw cron add \
  --name "域外搜索资讯" \
  --cron "0 */6 * * *" \
  --session isolated \
  --message "执行域外搜索任务..."
```

---

## 📈 数据统计

| 指标 | 数值 |
|------|------|
| 搜索引擎 | 2个 (Google, Bing) |
| 科技网站 | 5个 |
| 社交平台 | 3个 |
| 代码社区 | 2个 |
| 财经网站 | 3个 |
| 数据网站 | 2个 |
| **总计** | **17个** |

---

## 🛠️ 优化建议

1. **搜索频率**：每6小时一次，避免过度请求
2. **关键词轮换**：每周更新搜索关键词，保持新鲜度
3. **来源验证**：重要信息多源交叉验证
4. **内容筛选**：过滤广告、低质量内容
5. **本地化处理**：将国际新闻翻译整理成中文摘要

---

## ⚠️ 政治敏感内容过滤规则（重要）

### 绝对禁止发布的内容
- ❌ 意识形态相关内容
- ❌ 抹黑党和国家的言论
- ❌ 涉及政治敏感话题的国际评论
- ❌ 未经中国政府认证的国际组织观点
- ❌ 可能引发政治争议的热点话题

### 过滤原则
1. **技术/科技类**: ✅ 正常获取（AI、代码、科学发现等）
2. **商业/财经类**: ✅ 正常获取（市场数据、公司动态等）
3. **生活/娱乐类**: ✅ 正常获取（影视、游戏、生活技巧等）
4. **国际政治类**: ⚠️ 谨慎处理，优先使用国内官方媒体报道
5. **社会热点类**: ⚠️ 需评估，保持中立客观

### 可获取的内容类型
| 类型 | 示例 | 状态 |
|------|------|------|
| 🔬 科学研究 | Arxiv论文、技术突破 | ✅ 安全 |
| 💻 技术资讯 | Hacker News讨论、GitHub项目 | ✅ 安全 |
| 📈 财经数据 | 股市行情、公司财报 | ✅ 安全 |
| 🎮 娱乐生活 | 游戏发布、影视资讯 | ✅ 安全 |
| 🌤️ 生活技巧 | 烹饪、健身、旅行 | ✅ 安全 |
| 🏭 工业科技 | 汽车、手机、新产品 | ✅ 安全 |
| 🗳️ 国际政治 | 领导人动态、政策解读 | ⚠️ 需官方源验证 |
| 📰 社会事件 | 突发事件、社会话题 | ⚠️ 需谨慎评估 |

### 过滤操作流程
```
1. 获取国际资讯
       ↓
2. 自动过滤敏感词（AI/意识形态/政治敏感）
       ↓
3. 标记需要人工审核的内容
       ↓
4. 仅发布通过审核的安全内容
       ↓
5. 敏感内容→使用国内官方源替代报道
```

### 敏感词库示例
```
禁止词库：
- "中国崩溃论"
- "人权问题"（国外组织观点）
- "政治制度"（对比评价）
- "抗议活动"（相关报道）
- "台/港/藏/疆"（分离主义相关）
```

### 发布原则
1. **语言**: ✅ **全部翻译整理成中文发布**
2. **技术优先**: 多发布科技、财经、生活类内容
3. **政治回避**: 国际政治话题优先引用国内官方媒体
4. **中立表达**: 即使发布国际新闻，也保持客观中立
5. **来源可靠**: 优先使用官方权威媒体

---

## 📊 过滤效果统计

| 指标 | 预期值 |
|------|--------|
| 安全内容占比 | > 95% |
| 需审核内容占比 | < 5% |
| 禁止发布内容占比 | 0% |

### 记录时间
- **规则创建**: 2026-02-10 22:23
- **规则制定者**: 蒋国春
- **执行标准**: 严格遵守

