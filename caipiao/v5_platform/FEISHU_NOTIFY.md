# 飞书通知配置

## 1. 创建飞书群机器人

1. 打开飞书群 → 设置 → 群机器人
2. 添加机器人 → 自定义机器人
3. 复制Webhook URL

## 2. 配置环境变量

```bash
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxx..."
```

或者写入 ~/.bashrc：

```bash
echo 'export FEISHU_WEBHOOK_URL="https://..."' >> ~/.bashrc
source ~/.bashrc
```

## 3. 测试发送

```bash
./send_optimizer_notify.sh
```

## 4. 查看发送日志

```bash
tail -f /tmp/optimizer_notify.log
```
