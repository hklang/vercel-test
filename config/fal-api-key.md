# Fal.ai API 配置

## API Key
- **Key**: `5528e0b6-af9e-4bff-b713-70b40d451ed9:81d42246638e45ca334407e48d113c4f`
- **描述**: 视频生成
- **创建时间**: 2026-03-04
- **范围**: API

## 使用方法

### Python
```python
import fal_client

# 设置 API Key
FAL_KEY = "5528e0b6-af9e-4bff-b713-70b40d451ed9:81d42246638e45ca334407e48d113c4f"

# 使用 fal_client
result = fal_client.submit(
    "fal-ai/kling-video/v3/pro/image-to-video",
    {
        "prompt": "视频描述",
        "image_url": "https://example.com/image.jpg"
    },
    auth=FAL_KEY
)
```

### 环境变量
```bash
export FAL_KEY="5528e0b6-af9e-4bff-b713-70b40d451ed9:81d42246638e45ca334407e48d113c4f"
```

## 相关模型
- **Kling Video**: 视频生成
- **Nano Banana**: 图片生成
- **Flux**: 图片生成

## 注意事项
- API Key 只显示一次，请妥善保存
- 当前账户余额: $0.00 (需要充值才能使用)

---

**更新时间**: 2026-03-04
