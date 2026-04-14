# Biomat Video Engine - Vercel部署版

## 快速部署

### 1. 上传代码到GitHub

```bash
# 初始化Git
git init

# 添加文件
git add .

# 提交
git commit -m "feat: 添加Vercel部署支持"

# 推送到GitHub
git remote add origin https://github.com/your-username/biomat-video-engine.git
git branch -M main
git push -u origin main
```

### 2. 在Vercel部署

1. 访问 [vercel.com](https://vercel.com)
2. 登录/注册
3. 点击 "Add New Project"
4. 导入你的GitHub仓库
5. 配置环境变量（见下方）
6. 点击 "Deploy"

### 3. 配置环境变量

在Vercel项目设置中添加以下环境变量：

```bash
# API密钥（Make使用）
BIOMAT_API_KEY=bm_Pla1ic3_D3y3k3y_2k0k0k0k0k0k0k0k0k0k0k0k0k0k

# Coze Bot配置
COZE_BOT_ID=7624342475888590902
COZE_API_TOKEN=sat_CIaDvIIgWkvI7Ziny0Cdz6aIO7Sluw8qnyZXJsLVMp1t9kUuF5xX8qD0HB0kxQdC
```

### 4. 获取API地址

部署成功后：
- 默认地址: `https://your-project.vercel.app/api/v1/generate-video`
- 自定义域名: `https://juhepolymer.com/api/v1/generate-video`

### 5. 配置Make.com

在Make的HTTP模块中：

**URL:**
```
https://juhepolymer.com/api/v1/generate-video
```

**Method:** POST

**Headers:**
```
Authorization: Bearer bm_Pla1ic3_D3y3k3y_2k0k0k0k0k0k0k0k0k0k0k0k0k0k
Content-Type: application/json
```

**Body:**
```json
{
  "material": "auto",
  "scenes": 3,
  "platform": "youtube"
}
```

## API端点

### POST /api/v1/generate-video

生成视频并返回数据

**请求体:**
```json
{
  "material": "auto" | "PCL" | "PLLA" | "PLGA",
  "scenes": 3,
  "platform": "youtube" | "tiktok" | "both"
}
```

**响应:**
```json
{
  "success": true,
  "data": {
    "material": "PLLA",
    "videos": [...],
    "youtube_metadata": {...}
  }
}
```

### GET /api/v1/health

健康检查端点

**响应:**
```json
{
  "status": "healthy",
  "service": "Biomat_Video_Engine",
  "version": "2.0"
}
```

## 测试

```bash
curl -X POST https://juhepolymer.com/api/v1/generate-video \
  -H "Authorization: Bearer bm_Pla1ic3_D3y3k3y_2k0k0k0k0k0k0k0k0k0k0k0k0k0k" \
  -H "Content-Type: application/json" \
  -d '{"material": "auto", "scenes": 3, "platform": "youtube"}'
```

## 工作流程

1. **Make定时触发** (每天20:00)
2. **Vercel API接收请求**
3. **调用Coze Bot API**
4. **Bot执行视频生成工作流**
5. **返回JSON数据给Make**
6. **Make处理数据并发布到YouTube**

## 注意事项

- Vercel免费版函数超时时间: 10秒（付费版可延长）
- 视频生成可能需要较长时间，建议升级到Vercel Pro
- Coze Bot API有调用频率限制
- 确保环境变量正确配置

## 故障排查

### 500错误
- 检查环境变量是否正确设置
- 查看Vercel日志
- 检查Coze Bot API是否正常

### 401错误
- 检查API Key是否正确
- 确认Authorization Header格式

### 超时
- 视频生成时间较长
- 升级到Vercel Pro版
- 优化视频生成参数
