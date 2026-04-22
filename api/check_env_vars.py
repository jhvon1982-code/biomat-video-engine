#!/usr/bin/env python3
"""
检查环境变量是从哪里获取的
"""
import os

print("=" * 60)
print("检查SDK环境变量的来源")
print("=" * 60)

# SDK需要的3个环境变量
required_env_vars = [
    "COZE_WORKLOAD_IDENTITY_API_KEY",
    "COZE_INTEGRATION_BASE_URL",
    "COZE_INTEGRATION_MODEL_BASE_URL"
]

print("\n当前环境中的值:")
for var in required_env_vars:
    value = os.getenv(var)
    if value:
        # 隐藏部分API Key
        if 'API_KEY' in var:
            masked = value[:20] + "..." + value[-20:]
            print(f"✅ {var} = {masked}")
        else:
            print(f"✅ {var} = {value}")
    else:
        print(f"❌ {var} = NOT SET")

print("\n" + "=" * 60)
print("检查这些值是否在配置文件中")
print("=" * 60)

# 检查常见配置文件
config_files = [
    "/workspace/projects/.env",
    "/workspace/projects/api/.env",
    "/workspace/projects/api/_config.py",
    "/workspace/projects/api/config.py",
    "/workspace/projects/coze_coding_utils/runtime_ctx/context.py"
]

for file_path in config_files:
    print(f"\n检查: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for var in required_env_vars:
                if var in content:
                    print(f"  📄 找到 {var}")
                    # 尝试提取值
                    import re
                    matches = re.findall(rf'{var}\s*=\s*[\'"]([^\'"]+)[\'"]', content)
                    if matches:
                        for match in matches:
                            print(f"      值: {match[:50]}..." if len(match) > 50 else f"      值: {match}")
    except FileNotFoundError:
        print(f"  📄 文件不存在")
    except Exception as e:
        print(f"  ❌ 读取错误: {str(e)}")

print("\n" + "=" * 60)
print("准备Render环境变量配置")
print("=" * 60)

print("\n需要在Render中配置的环境变量:")
print("-" * 60)

for var in required_env_vars:
    value = os.getenv(var)
    if value:
        if 'API_KEY' in var:
            print(f"{var}:")
            print(f"  Value: {value}")
            print(f"  (这是一个完整的API Key，需要复制到Render)")
        else:
            print(f"{var}: {value}")
    else:
        print(f"{var}: 需要设置")

print("\n" + "=" * 60)
print("配置说明")
print("=" * 60)
print("""
1. 登录 https://dashboard.render.com
2. 选择 biomat-video-engine 服务
3. 进入 Environment Variables 页面
4. 点击 "Add Environment Variable"
5. 复制粘贴上面的环境变量配置
6. 点击 "Save Changes"
7. 触发重新部署（或者等待下次自动部署）
""")
