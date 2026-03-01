# v2rayA 使用指南

## 基本信息

| 项目 | 内容 |
|------|------|
| 管理地址 | http://127.0.0.1:20171 |
| 本地代理 | 127.0.0.1:20170 (SOCKS5) |
| 订阅地址 | https://106.55.228.246:36666/hxvip?token=xxxx |

## 启用/禁用代理

### 方法1：Web界面
1. 打开 http://127.0.0.1:20171
2. 点击「启用」按钮

### 方法2：命令行
```bash
# 启用代理
v2raya enable

# 禁用代理
v2raya disable

# 查看状态
v2raya status
```

## 常用命令

```bash
# 重启服务
sudo systemctl restart v2raya

# 查看日志
sudo journalctl -u v2raya -f
```

## 浏览器配置

### Chrome/Edge
安装 SwitchyOmega 插件，配置：
- 协议：SOCKS5
- 地址：127.0.0.1
- 端口：20170

### 系统代理（全局）
- HTTP代理：127.0.0.1:20171
- SOCKS5代理：127.0.0.1:20170

## 网络策略
- 国内网站：直连
- 国外网站：走代理
