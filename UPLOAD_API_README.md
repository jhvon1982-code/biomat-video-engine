# 文件上传API使用说明

## 概述

这是一个独立的文件上传API，支持上传视频文件和脚本文件，并自动上传到YouTube。

## API端点

### 1. 健康检查

**端点:** `GET /health`

**返回示例:**
```json
{
  "status": "healthy",
  "youtube_configured": false,
  "workspace": {
    "videos_dir": "/workspace/projects/workspace/videos",
    "scripts_dir": "/workspace/projects/workspace/scripts",
    "uploaded_dir": "/workspace/projects/workspace/uploaded"
  }
}
```

---

### 2. 上传视频

**端点:** `POST /api/v1/upload/video`

**请求参数:**
- `file`: 视频文件（必需）
- `title`: 视频标题（可选）
- `description`: 视频描述（可选）
- `tags`: 视频标签（逗号分隔，可选）
- `auto_upload_youtube`: 是否自动上传到YouTube（默认false）

**请求示例（curl）:**
```bash
curl -X POST http://your-api-url/api/v1/upload/video \
  -F "file=@/path/to/your/video.mp4" \
  -F "title=你的视频标题" \
  -F "description=你的视频描述" \
  -F "tags=标签1,标签2,标签3" \
  -F "auto_upload_youtube=true"
```

**请求示例（Python）:**
```python
import requests

url = "http://your-api-url/api/v1/upload/video"
files = {
    'file': open('/path/to/your/video.mp4', 'rb')
}
data = {
    'title': '你的视频标题',
    'description': '你的视频描述',
    'tags': '标签1,标签2,标签3',
    'auto_upload_youtube': 'true'
}

response = requests.post(url, files=files, data=data)
print(response.json())
```

**返回示例:**
```json
{
  "success": true,
  "message": "视频上传成功",
  "data": {
    "video_id": "0a597d96-dde9-4a07-aa27-64542a8037f5",
    "video_filename": "video_0a597d96-dde9-4a07-aa27-64542a8037f5.mp4",
    "video_path": "/workspace/projects/workspace/videos/video_0a597d96-dde9-4a07-aa27-64542a8037f5.mp4",
    "video_size_mb": 5.23,
    "original_filename": "your_video.mp4",
    "title": "你的视频标题",
    "description": "你的视频描述",
    "tags": ["标签1", "标签2", "标签3"]
  },
  "youtube_upload": null,
  "youtube_configured": false
}
```

---

### 3. 上传脚本

**端点:** `POST /api/v1/upload/script`

**请求参数:**
- `file`: JSON脚本文件（必需）
- `video_filename`: 对应的视频文件名（必需）

**请求示例（curl）:**
```bash
curl -X POST http://your-api-url/api/v1/upload/script \
  -F "file=@/path/to/your/script.json" \
  -F "video_filename=video_0a597d96-dde9-4a07-aa27-64542a8037f5.mp4"
```

**脚本文件格式（script.json）:**
```json
{
  "title": "云南聚和PGA聚乙醇酸_医用级生物材料",
  "description": "云南聚和PGA聚乙醇酸，高强度、快速降解，适用于缝合线...",
  "tags": ["云南聚和", "PGA", "聚乙醇酸", "医用材料"],
  "category": "People & Blogs"
}
```

---

### 4. 列出文件

**端点:** `GET /api/v1/upload/list`

**返回示例:**
```json
{
  "success": true,
  "data": {
    "videos": [
      {
        "filename": "video_0a597d96-dde9-4a07-aa27-64542a8037f5.mp4",
        "path": "/workspace/projects/workspace/videos/video_0a597d96-dde9-4a07-aa27-64542a8037f5.mp4",
        "size_mb": 5.23,
        "created_time": "2026-04-22T08:30:00",
        "has_script": false
      }
    ],
    "scripts": [],
    "upload_records": [],
    "statistics": {
      "total_videos": 1,
      "total_scripts": 0,
      "total_uploads": 0,
      "youtube_configured": false
    }
  }
}
```

---

### 5. 删除视频

**端点:** `DELETE /api/v1/upload/video/{filename}`

**请求示例:**
```bash
curl -X DELETE http://your-api-url/api/v1/upload/video/video_0a597d96-dde9-4a07-aa27-64542a8037f5.mp4
```

---

### 6. 手动上传到YouTube

**端点:** `POST /api/v1/upload/youtube/{filename}`

**请求示例:**
```bash
curl -X POST http://your-api-url/api/v1/upload/youtube/video_0a597d96-dde9-4a07-aa27-64542a8037f5.mp4
```

**注意:** 此功能需要先配置YouTube OAuth2认证。

---

## 完整工作流程

### 方式1：上传视频，自动上传YouTube

1. 上传视频（设置 `auto_upload_youtube=true`）
2. API自动上传到YouTube
3. 返回YouTube URL

**Python代码:**
```python
import requests

# 上传视频并自动上传YouTube
url = "http://your-api-url/api/v1/upload/video"
files = {
    'file': open('my_video.mp4', 'rb')
}
data = {
    'title': '你的视频标题',
    'description': '你的视频描述',
    'tags': '标签1,标签2,标签3',
    'auto_upload_youtube': 'true'
}

response = requests.post(url, files=files, data=data)
result = response.json()

if result.get('success'):
    if result.get('youtube_upload', {}).get('success'):
        youtube_url = result['youtube_upload']['youtube_url']
        print(f"视频已上传到YouTube: {youtube_url}")
    else:
        print("视频上传成功，但YouTube上传失败")
        print(f"错误: {result.get('youtube_upload', {}).get('error')}")
```

### 方式2：上传视频和脚本，手动上传YouTube

1. 上传视频
2. 上传对应的脚本
3. 手动触发YouTube上传

**Python代码:**
```python
import requests
import time

base_url = "http://your-api-url/api/v1/upload"

# 1. 上传视频
video_response = requests.post(
    f"{base_url}/video",
    files={'file': open('my_video.mp4', 'rb')},
    data={'title': '临时标题'}
)
video_result = video_response.json()
video_filename = video_result['data']['video_filename']

# 2. 上传脚本
script_response = requests.post(
    f"{base_url}/script",
    files={'file': open('my_script.json', 'rb')},
    data={'video_filename': video_filename}
)
script_result = script_response.json()

# 3. 手动上传到YouTube
youtube_response = requests.post(
    f"{base_url}/youtube/{video_filename}"
)
youtube_result = youtube_response.json()

if youtube_result.get('success'):
    print(f"YouTube URL: {youtube_result['data']['youtube_url']}")
```

---

## 配置YouTube OAuth2

### 1. 创建Google Cloud项目

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目
3. 启用YouTube Data API v3

### 2. 创建OAuth2凭据

1. 进入"凭据"页面
2. 点击"创建凭据" → "OAuth客户端ID"
3. 应用类型选择"桌面应用"
4. 创建后下载JSON文件

### 3. 配置凭证

**在Render中:**
1. 将JSON文件内容作为环境变量 `YOUTUBE_OAUTH2_CLIENT_SECRETS` 设置
2. 或通过Files功能上传到 `config/youtube_client_secrets.json`

**在本地:**
1. 将JSON文件重命名为 `youtube_client_secrets.json`
2. 放到 `config/` 文件夹

### 4. 执行OAuth2认证

```bash
cd /workspace/projects
python main.py auth
```

按照提示在浏览器中授权，授权成功后凭证会自动保存。

---

## 部署到Render

### 1. 推送代码到GitHub

代码已推送到GitHub，Render会自动部署。

### 2. 配置环境变量

在Render中设置以下环境变量（可选）：
- `YOUTUBE_OAUTH2_CLIENT_SECRETS`: OAuth2客户端密钥JSON

### 3. 配置启动命令

在Render的"Start Command"中设置：

```bash
cd /workspace/projects && python -m uvicorn api.upload_api:app --host 0.0.0.0 --port $PORT
```

### 4. 访问API

部署成功后，通过Render提供的URL访问API：

- 健康检查: `https://your-app-name.onrender.com/health`
- 上传视频: `https://your-app-name.onrender.com/api/v1/upload/video`

---

## 注意事项

1. **文件大小限制**: 默认无限制，但YouTube有最大256GB的限制
2. **支持的格式**: mp4, mov, avi, mkv, webm
3. **YouTube API限制**: 每天有上传配额限制
4. **脚本命名**: 脚本文件名必须与视频文件名匹配（不含扩展名）

---

## 常见问题

### Q: API返回"YouTube OAuth2未配置"

A: 需要先配置YouTube OAuth2认证，参考"配置YouTube OAuth2"部分。

### Q: 上传大文件超时

A: 可以增加上传超时时间，或使用分片上传（需要额外开发）。

### Q: 如何查看上传状态

A: 调用 `GET /api/v1/upload/list` 查看所有文件和上传记录。

### Q: 如何删除上传的文件

A: 调用 `DELETE /api/v1/upload/video/{filename}` 删除视频文件。
