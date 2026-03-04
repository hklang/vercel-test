# 视频生成API调研

## 云端API方案 (无需GPU)

### 1. HeyGen API
- **价格**: ~$1/分钟
- **特点**: 效果最好，支持中文，多种Avatar
- **文档**: https://developer.heygen.com
- **需要**: API Key

### 2. D-ID API
- **价格**: ~$0.5/分钟
- **特点**: 老牌服务商，稳定
- **文档**: https://docs.d-id.com
- **需要**: API Key

### 3. Fal.ai (推荐)
- **价格**: 按量计费，便宜
- **服务**:
  - **数字人**: $0.04/秒
  - **视频生成**: 多种模型
- **文档**: https://fal.ai/docs
- **SDK**: `pip install fal-client`

### 4. Replicate
- **价格**: 按量计费
- **模型**:
  - SVD (Stable Video Diffusion)
  - Animatediff
  - 各种开源模型
- **文档**: https://replicate.com
- **SDK**: `pip install replicate`

### 5. 免费/低成本方案
- **Pika Labs**: 免费但不稳定
- **Runway**: 付费

---

## 推荐方案

**首选: Fal.ai**
- 价格便宜
- 有免费额度
- SDK完善
- 支持数字人

**备选: Replicate**
- 模型多
- 按量计费

---

## 待验证
- [ ] HeyGen API 申请
- [ ] Fal.ai 账号申请
- [ ] 测试生成效果

---

## 调研时间
2026-03-04
