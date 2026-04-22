# 部署说明

## 本地部署

### 1. 安装依赖

```bash
cd /workspace/projects
uv add google-auth google-api-python-client watchdog
```

### 2. 配置YouTube OAuth2

参考 `YOUTUBE_UPLOADER_README.md` 中的说明。

### 3. 测试

```bash
# 查看状态
python main.py status

# 上传单个视频
python main.py upload workspace/videos/PGA聚乙醇酸_example.mp4

# 监控模式
python main.py watch --simple --interval 60
```

## Render部署

### 1. 上传代码

代码已推送到GitHub，Render会自动部署。

### 2. 配置环境变量

在Render中不需要额外的环境变量。

### 3. 上传OAuth2凭证

**方法1：通过Render的环境变量**

```bash
# 在Render中设置环境变量
YOUTUBE_OAUTH2_TOKEN=你的OAuth2令牌
```

**方法2：直接上传凭证文件**

1. 本地执行OAuth2认证：`python main.py auth`
2. 将生成的 `workspace/youtube_credentials.json` 上传到Render
3. 使用Render的"Files"功能上传文件

### 4. 配置启动命令

在Render的"Start Command"中设置：

```bash
cd /workspace/projects && python main.py watch --simple --interval 60
```

### 5. 查看日志

在Render的"Logs"中查看上传工具的日志。

## 使用说明

### 你需要做的

1. **生成视频**：用DeepSeek/Gemini生成脚本，用即梦生成视频
2. **保存视频**：将视频保存到 `workspace/videos/` 文件夹
3. **保存脚本**：将脚本保存到 `workspace/scripts/` 文件夹（可选）

### 工具自动做的

1. **监控文件夹**：检测新视频文件
2. **加载脚本**：读取对应的脚本文件
3. **上传视频**：上传到YouTube
4. **添加元数据**：自动添加标题、描述、标签
5. **记录状态**：保存上传记录

## 注意事项

1. **YouTube API限制**：每天有上传配额限制
2. **视频格式**：支持mp4、mov、avi等格式
3. **文件命名**：脚本文件名必须与视频文件名匹配
4. **OAuth2刷新**：凭证会自动刷新，无需担心过期
