# Make.com 工作流配置文档

## 工作流名称
Biomat Video Engine - 自动视频生成与发布

## 触发器配置

### 定时器设置
- **触发类型**：Clock / Schedule
- **运行频率**：Daily
- **运行时间**：19:00（美国东部时间）
- **时区**：America/New_York

---

## 工作流步骤

### 步骤1：HTTP Request - 触发视频生成

**模块**：HTTP - Make an a request

**配置**：
- **URL**：`https://biomat-video-engine.onrender.com/api/v1/generate-video`
- **Method**：POST
- **Headers**：
  ```json
  {
    "Authorization": "Bearer bm_Pla1ic3_D3y3k3y_2k0k0k0k0k0k0k0k0k0k0k0k0k0k",
    "Content-Type": "application/json"
  }
  ```
- **Body**（JSON格式）：
  ```json
  {
    "material": "auto",
    "scenes": 3,
    "platform": "youtube",
    "product_name": "PCL"
  }
  ```

**可选参数说明**：
- `material`:
  - `auto`：自动选择产品（推荐）
  - 具体产品名：`PCL`, `PLGA`, `PLLA`, `PTMC`, `PLCL`
- `scenes`:
  - `3`：3个场景（每场景5秒，总时长15秒）
  - `5`：5个场景（每场景3秒，总时长15秒）
  - `8`：8个场景（每场景2秒，总时长16秒）
- `platform`:
  - `youtube`：生成YouTube视频
  - `tiktok`：生成TikTok视频
  - `instagram`：生成Instagram视频
- `product_name`（可选）：
  - 指定具体产品名称
  - 不指定时自动轮播产品

---

### 步骤2：Iterator - 处理返回的视频列表

**模块**：Iterator

**配置**：
- **Array**：从步骤1的响应中提取 `videos` 字段

---

### 步骤3：HTTP Request - 下载视频

**模块**：HTTP - Download a file

**配置**：
- **URL**：从Iterator中获取 `video_url`
- **Method**：GET
- **File name**：从Iterator中获取 `filename`

---

### 步骤4：YouTube - 上传视频

**模块**：YouTube - Upload a video

**配置**：
- **Video file**：从步骤3获取
- **Title**：
  ```
  {{步骤1.title}} - 四川琢新-云南聚和
  ```
- **Description**：
  ```
  {{步骤1.description}}

  四川琢新-云南聚和专业生产可降解高分子材料
  官网：https://juhepolymer.com/
  ```
- **Tags**：从步骤1获取 `tags`
- **Privacy**：Public（公开）

---

## 产品轮播策略

### 方案1：自动轮播（推荐）
```json
{
  "material": "auto",
  "scenes": 3,
  "platform": "youtube"
}
```
系统会自动从产品库中选择产品，每天一个。

### 方案2：指定产品
```json
{
  "material": "PCL",
  "scenes": 3,
  "platform": "youtube"
}
```
生成指定产品的视频。

### 方案3：批量生成（高级）
创建多个HTTP Request模块，每个生成不同产品的视频。

---

## 响应格式

### 成功响应示例
```json
{
  "status": "success",
  "video": {
    "title": "PCL聚己内酯 - 四川琢新-云南聚和",
    "description": "聚己内酯（PCL）是一种生物可降解高分子材料...",
    "url": "https://example.com/video.mp4",
    "duration": 15,
    "resolution": "720p"
  },
  "seo": {
    "title": "PCL Polycaprolactone 3D Printing Material - Medical Grade Biodegradable Polymer",
    "tags": ["PCL", "Polycaprolactone", "Biodegradable", "3D Printing", "Medical"]
  }
}
```

### 错误响应示例
```json
{
  "status": "error",
  "error": "Workflow execution failed",
  "message": "Coze API error: We're currently experiencing server issues."
}
```

---

## 错误处理

### 常见错误

**1. Render服务休眠**
- **现象**：第一次请求响应慢（30-90秒）
- **处理**：等待服务唤醒，自动重试

**2. Coze服务故障**
- **现象**：返回500错误
- **处理**：记录错误日志，等待Coze恢复

**3. API鉴权失败**
- **现象**：返回401 Unauthorized
- **处理**：检查API Key是否正确

---

## 监控与日志

### Make日志
- 查看每次运行的详细日志
- 记录成功/失败状态
- 记录视频生成时间

### 建议监控指标
- 工作流运行成功率
- 视频生成平均时长
- YouTube上传成功率

---

## 高级配置

### 变量管理
在Make中使用变量管理API Key：
- `BIOMAT_API_KEY`: bm_Pla1ic3_D3y3k3y_2k0k0k0k0k0k0k0k0k0k0k0k0k0k
- `YOUTUBE_API_KEY`: [YouTube API Key]
- `COZE_BOT_ID`: 7624342475888590902

### 环境变量切换
- **生产环境**：使用真实的YouTube频道
- **测试环境**：使用测试频道或本地下载

---

## 发布时间优化

### 北美市场最佳发布时间
- **YouTube**：美国东部时间20:00（北京时间上午8:00）
- **Agent启动时间**：美国东部时间19:00
- **视频生成耗时**：约5-10分钟
- **上传耗时**：约2-5分钟
- **预计发布时间**：美国东部时间19:15-19:25

### 其他时区调整
- **欧洲市场**：美国东部时间02:00（欧洲时间08:00）
- **亚洲市场**：美国东部时间23:00（北京时间11:00）

---

## 附录

### 产品列表
1. PCL - 聚己内酯
2. PLGA - 聚（乳酸-乙交酯）共聚物
3. PTLA - 聚（乳酸-三亚甲基碳酸酯）共聚物
4. PLCL - 左旋聚乳酸-聚己内酯共聚物
5. PTMC - 聚三亚甲基碳酸酯

### 联系方式
- **公司官网**：https://juhepolymer.com/
- **Make工作流**：需要用户手动保存
- **技术支持**：通过Make社区或Coze官方

---

**最后更新时间**：2026-04-15
**版本**：v2.0
