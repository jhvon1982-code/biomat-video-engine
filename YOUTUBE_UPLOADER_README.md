# YouTube自动上传工具

全自动上传视频到YouTube，自动添加标题、描述、标签。

## 功能特性

- ✅ 自动监控文件夹，检测新视频
- ✅ 自动加载脚本文件（JSON格式）
- ✅ 自动上传到YouTube
- ✅ 自动添加标题、描述、标签
- ✅ 记录上传状态和历史
- ✅ 支持批量上传
- ✅ 支持监控模式和轮询模式

## 工作流程

1. **生成视频**：你手动生成视频，保存到 `workspace/videos/` 文件夹
2. **生成脚本**（可选）：生成脚本文件，保存到 `workspace/scripts/` 文件夹
3. **自动上传**：工具自动检测新视频，上传到YouTube

## 文件结构

```
/workspace/projects/
├── youtube_uploader/          # 工具代码
│   ├── config.py
│   ├── watcher.py
│   ├── youtube_client.py
│   ├── uploader.py
│   └── utils.py
├── workspace/                 # 工作空间
│   ├── videos/                # 放视频文件（你手动放）
│   ├── scripts/               # 放脚本文件（你手动放）
│   └── uploaded/              # 上传记录
├── config/
│   └── youtube_client_secrets.json  # OAuth2配置（需要配置）
└── main.py                    # 启动入口
```

## 快速开始

### 1. 配置YouTube OAuth2认证

**第一步：创建Google Cloud项目**

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目
3. 启用YouTube Data API v3

**第二步：创建OAuth2凭据**

1. 进入"凭据"页面
2. 点击"创建凭据" → "OAuth客户端ID"
3. 应用类型选择"桌面应用"
4. 创建后下载JSON文件

**第三步：配置客户端密钥**

1. 复制下载的JSON文件内容
2. 重命名为 `youtube_client_secrets.json`
3. 放到 `config/` 文件夹
4. 或修改 `config/youtube_client_secrets.json.example` 并重命名

**第四步：执行OAuth2认证**

```bash
cd /workspace/projects
python main.py auth
```

按照提示在浏览器中授权，授权成功后凭证会自动保存。

### 2. 使用工具

#### 上传单个视频

```bash
python main.py upload workspace/videos/my_video.mp4
```

#### 监控模式（推荐）

自动监控 `workspace/videos/` 文件夹，上传新视频：

```bash
# 使用文件系统监控（需要watchdog库）
python main.py watch

# 使用简单轮询模式
python main.py watch --simple --interval 60
```

#### 批量上传

上传 `workspace/videos/` 文件夹中的所有视频：

```bash
python main.py batch
```

#### 查看状态

查看工作空间状态和上传记录：

```bash
python main.py status
```

## 脚本格式

### 脚本文件位置

`workspace/scripts/产品名.json`

**注意：** 脚本文件名必须与视频文件名匹配（不含扩展名）

例如：
- 视频：`workspace/videos/PGA聚乙醇酸.mp4`
- 脚本：`workspace/scripts/PGA聚乙醇酸.json`

### 脚本文件内容

```json
{
  "title": "云南聚和PGA聚乙醇酸_医用级生物材料",
  "description": "云南聚和PGA聚乙醇酸，高强度、快速降解，适用于缝合线。符合ISO 10993生物相容性标准，广泛应用于医疗器械和生物材料领域。",
  "tags": ["云南聚和", "PGA", "聚乙醇酸", "医用材料", "生物相容性", "可降解"],
  "category": "People & Blogs"
}
```

### 必填字段

- `title`: 视频标题（最多100字符）
- `description`: 视频描述（最多5000字符）

### 可选字段

- `tags`: 视频标签数组
- `category`: 视频分类（见下方分类列表）

### 视频分类列表

| 分类名称 | 分类ID |
|---------|--------|
| Film & Animation | 1 |
| Autos & Vehicles | 2 |
| Music | 10 |
| Pets & Animals | 15 |
| Sports | 17 |
| Travel & Events | 19 |
| Gaming | 20 |
| People & Blogs | 22 |
| Comedy | 23 |
| Entertainment | 24 |
| News & Politics | 25 |
| Howto & Style | 26 |
| Education | 27 |
| Science & Technology | 28 |

## 完整使用流程

### 方式1：手动上传单个视频

1. 生成视频：`workspace/videos/PGA聚乙醇酸.mp4`
2. 生成脚本：`workspace/scripts/PGA聚乙醇酸.json`
3. 上传：`python main.py upload workspace/videos/PGA聚乙醇酸.mp4`

### 方式2：监控模式（推荐）

1. 生成视频：`workspace/videos/PGA聚乙醇酸.mp4`
2. 生成脚本：`workspace/scripts/PGA聚乙醇酸.json`
3. 启动监控：`python main.py watch`
4. 工具自动检测并上传

### 方式3：批量上传

1. 生成多个视频到 `workspace/videos/`
2. 生成对应的脚本到 `workspace/scripts/`
3. 批量上传：`python main.py batch`

## 部署到Render

### 1. 安装依赖

```bash
uv add google-auth google-api-python-client watchdog
```

### 2. 配置环境变量

在Render中设置以下环境变量：

- `COZE_WORKLOAD_IDENTITY_API_KEY`: （已有）
- `COZE_INTEGRATION_BASE_URL`: （已有）
- `COZE_INTEGRATION_MODEL_BASE_URL`: （已有）

### 3. 上传OAuth2凭证

1. 本地执行OAuth2认证：`python main.py auth`
2. 将生成的 `workspace/youtube_credentials.json` 上传到Render
3. 或者直接配置OAuth2环境变量

### 4. 创建启动脚本

创建 `start_watcher.sh`：

```bash
#!/bin/bash
cd /workspace/projects
python main.py watch --simple --interval 60
```

在Render中配置启动命令为 `bash start_watcher.sh`

## 注意事项

1. **视频文件大小限制**：YouTube最大支持256GB
2. **视频时长限制**：最长12小时
3. **上传频率限制**：避免过于频繁上传
4. **版权问题**：确保你有上传内容的版权

## 常见问题

### Q: OAuth2认证失败？

A: 检查 `config/youtube_client_secrets.json` 文件是否正确配置。

### Q: 监控模式不工作？

A: 使用简单轮询模式：`python main.py watch --simple`

### Q: 视频上传失败？

A: 检查视频文件大小和格式，确保符合YouTube要求。

### Q: 如何查看上传记录？

A: 运行 `python main.py status` 或查看 `workspace/uploaded/` 文件夹。

## 技术支持

如有问题，请查看日志文件：`workspace/youtube_uploader.log`
