# Vercel部署指南

## 快速部署步骤

### 1. 准备代码
将以下文件复制到你的Vercel项目：
```
api/
  ├── index.py          # API服务
  └── requirements.txt  # 依赖包
src/                   # 现有代码
  ├── agents/
  │   └── agent.py
  ├── tools/
  ├── storage/
  └── utils/
config/                # 配置文件
  └── agent_llm_config.json
vercel.json           # Vercel配置
```

### 2. 在Vercel中创建项目

1. 访问 [vercel.com](https://vercel.com)
2. 点击 "Add New Project"
3. 导入你的GitHub仓库或上传代码
4. 配置环境变量：
   - `BIOMAT_API_KEY`: `bm_Pla1ic3_D3y3k3y_2k0k0k0k0k0k0k0k0k0k0k0k0k0k`
   - `COZE_WORKLOAD_IDENTITY_API_KEY`: 从你的Coze环境获取
   - `COZE_INTEGRATION_MODEL_BASE_URL`: 从你的Coze环境获取

### 3. 部署
点击 "Deploy" 按钮，等待部署完成。

### 4. 获取API地址
部署成功后，Vercel会提供URL：
- 默认：`https://your-project-name.vercel.app/api/v1/generate-video`
- 自定义域名：`https://juhepolymer.com/api/v1/generate-video`

### 5. 配置Make
在Make的HTTP模块中使用：
- URL: `https://juhepolymer.com/api/v1/generate-video`
- Method: POST
- Headers:
  - Authorization: `Bearer bm_Pla1ic3_D3y3k3y_2k0k0k0k0k0k0k0k0k0k0k0k0k0k`
- Body:
  ```json
  {
    "material": "auto",
    "scenes": 3,
    "platform": "youtube"
  }
  ```

## 测试API
部署后测试：
```bash
curl -X POST https://juhepolymer.com/api/v1/generate-video \
  -H "Authorization: Bearer bm_Pla1ic3_D3y3k3y_2k0k0k0k0k0k0k0k0k0k0k0k0k0k" \
  -H "Content-Type: application/json" \
  -d '{"material": "auto", "scenes": 3, "platform": "youtube"}'
```

## 故障排查
- **500错误**: 检查环境变量是否正确设置
- **401错误**: 检查API Key是否正确
- **超时**: Vercel免费版超时时间为10秒，可能需要升级或优化代码
