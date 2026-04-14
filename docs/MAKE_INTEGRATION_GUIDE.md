# Make.com集成配置指南

## 🎯 方案概述

**工作流程**：
```
Make定时触发（每天20:00）
    ↓
调用我的API
    ↓
我生成视频和数据
    ↓
返回JSON给Make
    ↓
Make自动发布到YouTube
```

---

## 🔧 Make配置步骤

### 步骤1：创建新Scenario

1. 登录 [Make.com](https://www.make.com)
2. 点击左侧 "Create a new scenario"
3. 点击中间的粉色 "+" 按钮

---

### 步骤2：添加Schedule模块

1. 搜索 "Schedule"
2. 选择 "Schedule" 模块（不是 "Webhooks"）
3. 配置：
   ```
   Trigger: Every day at
   Hour: 20
   Minute: 0
   Timezone: Asia/Shanghai (UTC+8)
   ```
4. 点击 "Save"

**作用**：每天北京时间20:00自动触发工作流

---

### 步骤3：添加HTTP模块（调用API）

1. 点击Schedule模块右侧的 "+"
2. 搜索 "HTTP"
3. 选择 "HTTP → Make a request"
4. 配置：

```
URL:
https://你的域名/api/v1/generate-video

Method:
POST

Headers:
Content-Type: application/json
Authorization: Bearer BIOMAT_API_KEY

Request body:
{
  "material": "auto",
  "scenes": 3,
  "platform": "youtube"
}

Timeout:
900 (15分钟)
```

5. 点击 "Save"

**重要**：将 `BIOMAT_API_KEY` 替换为实际的API密钥（我会提供）

---

### 步骤4：添加Iterator模块

1. 点击HTTP模块右侧的 "+"
2. 搜索 "Iterator"
3. 选择 "Iterator" 模块
4. 配置：

```
Array:
data.videos

Iterator:
item
```

5. 点击 "Save"

**作用**：遍历返回的视频数组

---

### 步骤5：添加HTTP模块（下载视频）

1. 点击Iterator模块右侧的 "+"
2. 搜索 "HTTP"
3. 选择 "HTTP → Make a request"
4. 配置：

```
URL:
{{item.video_url}}

Method:
GET

Response format:
File

File name:
{{item.scene_name}}_{{data.material}}.mp4
```

5. 点击 "Save"

**作用**：下载每个视频文件

---

### 步骤6：添加YouTube模块

1. 点击HTTP模块右侧的 "+"
2. 搜索 "YouTube"
3. 选择 "YouTube → Upload a video"
4. 配置：

```
Account:
连接你的YouTube账号

File:
Map:
  - From: Data
  - To: file

Title:
{{data.youtube_metadata.title}}

Description:
{{data.youtube_metadata.description}}

Tags:
{{data.youtube_metadata.tags}}

Privacy status:
Public

Category:
Science & Technology
```

5. 点击 "Save"

**作用**：上传视频到YouTube

---

### 步骤7：添加通知模块（可选）

1. 点击YouTube模块右侧的 "+"
2. 搜索 "Email"
3. 选择 "Email → Send an email"
4. 配置：

```
To:
your-email@example.com

Subject:
Biomat Video Generated - {{data.material}}

Body:
视频生成成功！

材料: {{data.material}}
视频数量: {{item.length}}

YouTube链接: https://youtube.com/your-channel

发布时间: {{data.execution_time}}
```
5. 点击 "Save"

**作用**：发送完成通知

---

### 步骤8：测试工作流

1. 点击左下角 "Save"
2. 点击右上角 "Run once"
3. 观察每个模块的执行情况
4. 检查是否成功发布到YouTube

---

### 步骤9：激活定时任务

1. 确保测试成功
2. 点击左下角 "ON/OFF" 开关
3. 确保开关为绿色（开启状态）
4. 工作流将在每天20:00自动运行

---

## 📊 数据流说明

### 请求格式（Make → 我）

```json
{
  "material": "auto",
  "scenes": 3,
  "platform": "youtube"
}
```

### 响应格式（我 → Make）

```json
{
  "success": true,
  "data": {
    "material": "PLLA",
    "strategy": "strength",
    "videos": [
      {
        "scene_id": "scene1",
        "scene_name": "Crystallinity Visualization",
        "duration": 8,
        "resolution": "720p",
        "ratio": "16:9",
        "video_url": "https://...",
        "thumbnail_url": "https://...",
        "expires_in_hours": 24
      },
      {
        "scene_id": "scene2",
        "scene_name": "Mechanical Support",
        "duration": 10,
        "resolution": "720p",
        "ratio": "16:9",
        "video_url": "https://...",
        "thumbnail_url": "https://...",
        "expires_in_hours": 24
      },
      {
        "scene_id": "scene3",
        "scene_name": "Strength Comparison",
        "duration": 5,
        "resolution": "720p",
        "ratio": "16:9",
        "video_url": "https://...",
        "thumbnail_url": "https://...",
        "expires_in_hours": 24
      }
    ],
    "youtube_metadata": {
      "title": "PLLA: 120MPa Ultra-High Strength...",
      "description": "Discover the game-changing strength...",
      "tags": [
        "PLLA",
        "Poly L Lactic Acid",
        "Biomaterials",
        ...
      ],
      "category": "Science & Technology"
    },
    "tiktok_publishing_guide": "# TikTok发布指南...",
    "execution_time": "2026-04-13T20:00:00+08:00"
  },
  "execution_time": "2026-04-13T20:30:00+08:00"
}
```

---

## 🔑 API密钥配置

### 获取API密钥

我会为你提供一个安全的API密钥，格式如下：

```
BIOMAT_API_KEY=bm_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 配置到Make

在HTTP模块的Headers中添加：

```
Authorization: Bearer bm_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## ⚠️ 重要提示

### 1. API密钥安全

- 不要在公开场合分享API密钥
- 定期更换API密钥
- 如果泄露，立即重新生成

### 2. 视频链接过期

- 返回的视频链接24小时后过期
- Make必须在24小时内下载
- 如果过期，Make会自动重试

### 3. 超时设置

- HTTP模块超时设置为900秒（15分钟）
- 视频生成可能需要5-10分钟
- 如果超时，Make会自动重试

### 4. 错误处理

Make会自动处理错误：
- 如果API调用失败，Make会重试3次
- 如果视频下载失败，Make会重试3次
- 如果YouTube上传失败，Make会重试3次

---

## 📈 监控和维护

### 查看Make日志

1. 登录Make.com
2. 进入Scenario详情
3. 查看"History"标签
4. 查看每次运行的详细日志

### 查看YouTube数据

1. 登录YouTube Studio
2. 查看"Analytics"
3. 监控播放量、点赞、评论

### 查看WhatsApp咨询

定期查看WhatsApp：
- +1 (213) 275-7332
- 统计咨询数量
- 分析咨询内容

---

## 🚀 故障排查

### 问题1：工作流未执行

**可能原因**：
- Schedule模块未激活
- 时间设置错误

**解决方法**：
- 检查Schedule模块是否开启
- 检查时间设置是否为20:00
- 检查时区是否为Asia/Shanghai

### 问题2：API调用失败

**可能原因**：
- API密钥错误
- 网络连接问题
- API服务不可用

**解决方法**：
- 检查API密钥是否正确
- 检查Make日志中的错误信息
- 联系我检查API服务状态

### 问题3：视频未生成

**可能原因**：
- 即梦服务不可用
- 生成超时

**解决方法**：
- 查看Make日志中的详细错误
- 检查即梦服务状态
- 增加超时时间

### 问题4：YouTube上传失败

**可能原因**：
- YouTube账号未授权
- 视频格式不支持
- 标题或描述过长

**解决方法**：
- 重新连接YouTube账号
- 检查视频格式（支持MP4、MOV）
- 检查标题长度（<100字符）

---

## 📞 需要帮助？

如果遇到问题：

1. 查看Make日志
2. 检查错误信息
3. 联系我获取支持

---

**配置完成后，整个工作流将完全自动化运行！** 🚀
