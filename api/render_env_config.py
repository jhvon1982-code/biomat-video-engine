#!/usr/bin/env python3
"""
获取Render环境变量配置
"""

# 需要在Render中配置的环境变量
RENDER_ENV_VARS = {
    "COZE_WORKLOAD_IDENTITY_API_KEY": "M2pyUXJPeWFDdUhqRmUyYnllaVNPNWl4YnY5RlljaHc6dXA5Tk5kUElmcHk2MXZlU203djh5dGx5dTA3WnJsWnZ4OUMwTjJSdG1EaHZEMXppMFhHNENQbmlZYzJkMnB1Rg==",
    "COZE_INTEGRATION_BASE_URL": "https://integration.coze.cn",
    "COZE_INTEGRATION_MODEL_BASE_URL": "https://integration.coze.cn/api/v3"
}

print("=" * 60)
print("Render环境变量配置清单")
print("=" * 60)

print("\n方法1：在Render Dashboard中配置")
print("-" * 60)
print("1. 登录 https://dashboard.render.com")
print("2. 选择 biomat-video-engine 服务")
print("3. 点击 Environment Variables")
print("4. 添加以下环境变量：\n")

for key, value in RENDER_ENV_VARS.items():
    if 'API_KEY' in key:
        print(f"  {key}:")
        print(f"    {value}")
    else:
        print(f"  {key}: {value}")
    print()

print("方法2：添加到项目根目录的 .env 文件")
print("-" * 60)
print("创建 /workspace/projects/.env 文件，内容如下：\n")

for key, value in RENDER_ENV_VARS.items():
    print(f'{key}="{value}"')

print("\n方法3：硬编码到 API 代码中（临时方案）")
print("-" * 60)
print("修改 api/index.py，在导入后添加以下代码：\n")

print("""
import os

# 配置即梦视频生成SDK环境变量
os.environ['COZE_WORKLOAD_IDENTITY_API_KEY'] = 'M2pyUXJPeWFDdUhqRmUyYnllaVNPNWl4YnY5RlljaHc6dXA5Tk5kUElmcHk2MXZlU203djh5dGx5dTA3WnJsWnZ4OUMwTjJSdG1EaHZEMXppMFhHNENQbmlZYzJkMnB1Rg=='
os.environ['COZE_INTEGRATION_BASE_URL'] = 'https://integration.coze.cn'
os.environ['COZE_INTEGRATION_MODEL_BASE_URL'] = 'https://integration.coze.cn/api/v3'
""")

print("\n推荐方案：方法3（立即可用，无需配置Render）")
