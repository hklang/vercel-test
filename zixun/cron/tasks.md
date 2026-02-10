# 定时任务配置

## 任务1：每小时新闻资讯推送（8:00-20:00）

### 添加命令
```bash
openclaw cron add \
  --name "每日新闻推送(8:00-20:00)" \
  --cron "0/30 8-20 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "执行每半小时新闻推送：使用web_fetch获取新闻网页，提取内容，按日报风格排版发送到feishu群 oc_982e81066ead19e659ccff0f5f509ddd" \
  --announce \
  --channel feishu \
  --to "oc_982e81066ead19e659ccff0f5f509ddd"
```

### 任务说明
- **时间**：每天 8:00 - 20:00，每半小时
- **Cron表达式**：`0/30 8-20 * * *` （每小时的00分和30分）
- **Session**: isolated
- **推送目标**: oc_982e81066ead19e659ccff0f5f509ddd
- **获取方式**：使用 web_fetch 自动抓取新闻网页

### 内容分配策略（每半小时）
| 时间 | 新闻类型 | 主要来源（4-5个） |
|------|----------|-------------------|
| **8:00** | 早间要闻 + 天气预报 | 新浪 + 澎湃 + 观察者网 + 中央气象台 |
| **8:30** | 国内民生 + 政策 | 人民日报 + 新华社 + 央视新闻 |
| **9:00** | 国际快讯 + 科技动态 | 新浪国际 + BBC + 虎嗅 + 钛媒体 |
| **9:30** | AI/科技前沿 | 36氪 + 雷锋网 + DeepTech + InfoQ |
| **10:00** | 财经资讯 | 华尔街见闻 + 第一财经 + 财新 |
| **10:30** | 股市动态 | 东方财富 + 同花顺 + 证券时报 |
| **11:00** | 热搜榜 TOP10 | 百度热榜 + 知乎 + 微博 + 今日头条 |
| **11:30** | 地方新闻 | 上观新闻 + 澎湃新闻 |
| **12:00** | 午间简报 | 新浪 + 腾讯 + 网易 + 凤凰 |
| **12:30** | 消费生活 | 大众点评 + 什么值得买 + 下厨房 |
| **13:00** | 体育新闻 | 虎扑 + 懂球帝 + 腾讯体育 |
| **13:30** | 篮球/足球专题 | 虎扑NBA + 新浪体育 |
| **14:00** | 娱乐头条 | 豆瓣 + 猫眼 + 哔哩哔哩 |
| **14:30** | 影视综艺 | 豆瓣电影 + 微博娱乐 |
| **15:00** | 科技动态 | 36氪 + 爱范儿 + 极客公园 |
| **15:30** | 商业创新 | 钛媒体 + 虎嗅 + 第一财经 |
| **16:00** | 财经股市 | 同花顺 + 东方财富 + 华尔街见闻 |
| **16:30** | 基金理财 | 天天基金 + 蛋卷基金 |
| **17:00** | 晚间预告 | 新浪 + 网易 + 凤凰 + 腾讯 |
| **17:30** | 汽车资讯 | 汽车之家 + 易车网 + 太平洋汽车 |
| **18:00** | 综合要闻 | 腾讯 + 新浪 + 搜狐 + 澎湃 |
| **18:30** | 房产市场 | 贝壳找房 + 链家 + 安居客 |
| **19:00** | 国际快讯 | 路透社 + BBC + CNN + 联合早报 |
| **19:30** | 国际深度 | 纽约时报 + 华尔街日报 + 卫报 |
| **20:00** | 晚间总结 | 综合各源TOP10 |

---

## 任务2：新闻源扩展任务（每12小时）

### 添加命令
```bash
openclaw cron add \
  --name "新闻源扩展（每12小时）" \
  --cron "0 */12 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "执行扩展任务：1.扫描新增可用新闻源 2.更新 zixun/cron/news-sources.md 3.评估渠道质量 4.更新每日寄语库 zixun/cron/daily-quotes.md" \
  --announce \
  --channel feishu \
  --to "oc_982e81066ead19e659ccff0f5f509ddd"
```

### 任务说明
- **时间**：每 12 小时（0:00, 12:00）
- **Cron表达式**：`0 */12 * * *`
- **Session**: isolated
- **功能**：
  1. 扫描新增可用新闻源
  2. 更新 `zixun/cron/news-sources.md`
  3. 评估渠道质量
  4. **更新每日寄语库** `zixun/cron/daily-quotes.md`
  5. 优化内容分配策略

---

## 快速添加（复制执行）

### 添加任务1（每半小时）
```bash
openclaw cron add --name "每日新闻推送(8:00-20:00)" --cron "0/30 8-20 * * *" --tz "Asia/Shanghai" --session isolated --message "执行每半小时新闻推送：使用web_fetch获取新闻网页，提取内容，按日报风格排版发送到feishu群" --announce --channel feishu --to "oc_982e81066ead19e659ccff0f5f509ddd"
```

### 添加任务2
```bash
openclaw cron add --name "新闻源扩展（每12小时）" --cron "0 */12 * * *" --tz "Asia/Shanghai" --session isolated --message "执行扩展任务：扫描新增新闻源，更新news-sources.md，评估渠道质量，更新寄语库" --announce --channel feishu --to "oc_982e81066ead19e659ccff0f5f509ddd"
```

---

## 查看任务
```bash
openclaw cron list
```

## 删除任务
```bash
openclaw cron rm <任务ID>
```

---

## 📊 来源统计（93个新闻源）

| 类别 | 数量 | 代表媒体 |
|------|------|----------|
| 🏠 国内门户 | 10 | 新浪、腾讯、网易、凤凰、搜狐等 |
| 📋 官方媒体 | 6 | 人民日报、新华社、央视等 |
| 🔥 热搜平台 | 7 | 百度、知乎、微博、抖音等 |
| 💻 科技媒体 | 10 | 36氪、虎嗅、钛媒体、雷锋网等 |
| 💰 财经媒体 | 10 | 东方财富、华尔街见闻、财新等 |
| 🌍 国际媒体 | 10 | BBC、CNN、路透社、纽约时报等 |
| ⚽ 体育媒体 | 7 | 虎扑、懂球帝、腾讯体育等 |
| 🎮 娱乐游戏 | 7 | 哔哩哔哩、豆瓣、游民星空等 |
| 🚗 汽车房产 | 6 | 汽车之家、链家、贝壳等 |
| 🏥 健康医疗 | 4 | 丁香医生、39健康网等 |
| 📚 教育文化 | 6 | 知乎、豆瓣读书、中国教育在线等 |
| 👨‍💼 职场招聘 | 5 | BOSS直聘、脉脉、智联招聘等 |
| 🌱 生活美食 | 5 | 大众点评、马蜂窝、下厨房等 |
| **总计** | **93** | **新闻源** |

---

## 🌐 域外搜索资讯（新增）

### 外部搜索引擎
| 引擎 | 用途 | 访问方式 |
|------|------|----------|
| 🔍 Google | 综合搜索 | web_search (Brave API) |
| 🗣️ Bing | 微软搜索 | web_search |
| 🔎 DuckDuckGo | 隐私搜索 | web_search |

### 国际信息网站
| 类别 | 网站 | 用途 |
|------|------|------|
| 📊 数据统计 | Our World in Data | 全球数据可视化 |
| 📈 财经数据 | TradingView | 金融市场图表 |
| 💻 技术资讯 | Hacker News | 科技新闻社区 |
| 🧠 AI前沿 | Arxiv | 学术论文预印本 |
| 📰 综合新闻 | Reuters | 路透社国际新闻 |
| 🗳️ 社交媒体 | Reddit | 社区讨论热点 |
| 🎥 视频资讯 | YouTube Trending | 热门视频趋势 |
| 💼 商业资讯 | Bloomberg | 彭博商业新闻 |

### 定时任务：域外热点扫描

#### 添加命令
```bash
openclaw cron add \
  --name "域外搜索资讯（每6小时）" \
  --cron "0 */6 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "执行域外搜索：1.使用web_search搜索今日Google Trends热点 2.获取Hacker News热门话题 3.抓取Reddit热门讨论 4.搜索AI/科技前沿关键词 5.整理成域外资讯摘要发送到飞书群" \
  --announce \
  --channel feishu \
  --to "oc_982e81066ead19e659ccff0f5f509ddd"
```

#### 任务说明
- **时间**：每 6 小时（0:00, 6:00, 12:00, 18:00）
- **Cron表达式**：`0 */6 * * *`
- **Session**: isolated
- **功能**：
  1. 搜索 Google Trends 今日热点
  2. 获取 Hacker News Top 10
  3. 抓取 Reddit 各社区热门话题
  4. 搜索 AI/科技前沿关键词（GPT-5, Claude, etc.）
  5. 搜索 GitHub Trending 热门项目
  6. **执行政治敏感内容过滤**
  7. 整理成域外资讯摘要

#### ⚠️ 政治敏感内容规则
- ❌ 禁止发布：意识形态相关、抹黑党和国家的言论
- ✅ 安全内容：科技、财经、生活、娱乐类资讯
- ⚠️ 谨慎处理：国际政治事件需引用国内官方媒体
- 📋 过滤机制：自动过滤敏感词，人工审核敏感内容

#### 内容分配（每6小时）
| 时间 | 搜索重点 |
|------|----------|
| **0:00** | 前一日全球热点总结 |
| **6:00** | 凌晨至早间国际动态 |
| **12:00** | 午间全球热点扫描 |
| **18:00** | 晚间域外资讯汇总 |

### 搜索关键词配置

#### 科技AI类
```
AI, GPT-4, GPT-5, Claude, Gemini, LLM, AGI
Machine Learning, Deep Learning, Neural Network
OpenAI, Anthropic, Google DeepMind
```

#### 商业财经类
```
Stock Market, NASDAQ, S&P 500
Tesla, Apple, Microsoft, Google
Cryptocurrency, Bitcoin, Ethereum
```

#### 热门话题类
```
Viral, Trending, Popular
Breaking News, Latest Updates
```

### 推送模板（域外资讯版）
```
🌍 域外资讯 · 全球视野
━━━━━━━━━━━━━━━━
🔍 Google Trends 热点
1. 热点话题1
2. 热点话题2
...

💻 Hacker News Top 10
1. 标题1 (分数)
2. 标题2 (分数)
...

🤖 Reddit 热门讨论
• r/all 热门1
• r/technology 热门2
...

🔧 GitHub Trending
• 项目1 (⭐ stars)
• 项目2 (⭐ stars)
...

📊 数据洞察
• 关键数据点
• 市场趋势分析
━━━━━━━━━━━━━━━━
🦊 来源：Google Trends + Hacker News + Reddit + GitHub
```
