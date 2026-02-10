# v2rayA 安装与配置

## 概述

v2rayA 是一个轻量级的 V2Ray 客户端，支持 Web 管理界面和多种代理协议。

## 安装方式

### Snap 安装（推荐）

```bash
# 安装
echo 'lang1982' | sudo -S snap install v2raya

# 启动服务
echo 'lang1982' | sudo -S snap start v2raya

# 开机自启
echo 'lang1982' | sudo -S snap enable v2raya
```

### Docker 安装（备选）

```bash
# 安装Docker
echo 'lang1982' | sudo -S apt install -y docker.io docker-compose
echo 'lang1982' | sudo -S systemctl start docker

# 配置镜像加速（解决Docker Hub超时）
echo 'lang1982' | sudo -S tee /etc/docker/daemon.json << 'EOF'
{
  "registry-mirrors": [
    "https://dockerproxy.com",
    "https://docker.m.daocloud.io"
  ]
}
EOF
echo 'lang1982' | sudo -S systemctl restart docker
```

## Web 管理

- **地址**: http://127.0.0.1:2017
- **默认账号**: admin / admin

## 代理端口

| 类型 | 地址 | 用途 |
|------|------|------|
| SOCKS5 | 127.0.0.1:20170 | 支持UDP |
| HTTP | 127.0.0.1:20171 | 通用代理 |

## 使用方法

1. 登录 Web 界面
2. 添加订阅地址
3. 更新订阅，选择节点
4. 启动代理
5. 配置浏览器/系统代理

## 常用命令

```bash
# 查看状态
echo 'lang1982' | sudo -S snap services v2raya

# 重启
echo 'lang1982' | sudo -S snap restart v2raya

# 查看日志
echo 'lang1982' | sudo -S snap logs v2raya -n 50
```

## 故障排除

**Web无法访问**:
```bash
ss -tuln | grep 2017
```

**节点连接失败**: 尝试切换其他节点或更新订阅

**忘记密码**:
```bash
echo 'lang1982' | sudo -S snap run v2raya --reset-password
```

## 相关资源

- 官网: https://v2raya.org
- GitHub: https://github.com/v2rayA/v2rayA

## 使用场景

- 科学上网
- 访问 Google、GitHub 等服务
- 保护隐私流量

---

**创建时间**: 2026-02-10
**作者**: 蒋国春数字孪生
