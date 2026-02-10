# 天气查询

## 何时调用
当用户提及以下内容时激活：
- "天气"、"今天天气"、"天气预报"
- "明天天气"、"周末天气"
- "北京天气"、"上海天气"（任意城市名）

## 工具名称
`weather`（无 API key 要求）

## 服务商

### 1. wttr.in（主推荐）

快速查询：
```bash
curl -s "wttr.in/城市名?format=3"
# 示例：curl -s "wttr.in/北京?format=3"
# 输出：北京: ☀️ +22°C
```

紧凑格式：
```bash
curl -s "wttr.in/城市名?format=%l:+%c+%t+%h+%w"
# 输出：London: ⛅️ +8°C 71% ↙5km/h
```

完整预报：
```bash
curl -s "wttr.in/城市名?T"
```

### 2. Open-Meteo（备选，JSON 格式）

适合程序处理：
```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true"
```

## 格式代码
| 代码 | 说明 |
|-----|------|
| `%c` | 天气状况 |
| `%t` | 温度 |
| `%h` | 湿度 |
| `%w` | 风速 |
| `%l` | 地点 |
| `%m` | 月相 |

## 常用参数
| 参数 | 说明 |
|-----|------|
| `?m` | 公制单位 |
| `?u` | 美制单位 |
| `?1` | 仅今天 |
| `?0` | 仅当前 |
| `?0` | 仅今天 |

## 使用示例

**用户说**："北京天气"

**调用**：`curl -s "wttr.in/北京?format=3"`

**用户说**："上海明天天气"

**调用**：`curl -s "wttr.in/上海?format=3"`（wttr.in 默认返回今天+明天）

**用户说**："伦敦详细预报"

**调用**：`curl -s "wttr.in/伦敦?T"`

## 技巧
- 空格用 `+` 替代：`wttr.in/New+York`
- 支持机场代码：`wttr.in/JFK`
- 保存为图片：`curl -s "wttr.in/北京.png" -o /tmp/weather.png`

## 配置要求
```yaml
# 无需配置，无 API key 要求
# 依赖：curl 命令
```

## 注意事项
- wttr.in 是免费服务，无需 API key
- Open-Meteo 也是免费服务，无需 API key
- 两个服务可互为备份

