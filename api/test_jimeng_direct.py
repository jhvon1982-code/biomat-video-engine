#!/usr/bin/env python3
"""
测试即梦视频生成API的调用方式
"""
import asyncio
from coze_coding_dev_sdk.video import VideoGenerationClient, TextContent
from coze_coding_dev_sdk import APIError, Config

# 测试1：不使用任何配置
print("=" * 60)
print("测试1: 不使用任何配置（默认模式）")
print("=" * 60)

try:
    client1 = VideoGenerationClient()
    print("✅ 客户端1初始化成功（无参数）")

    video_url, response, last_frame_url = client1.video_generation(
        content_items=[
            TextContent(text="一个简单的测试场景")
        ],
        model="doubao-seedance-1-5-pro-251215",
        resolution="720p",
        ratio="16:9",
        duration=5,
        watermark=False,
        max_wait_time=120
    )

    if video_url:
        print(f"✅ 测试1成功！视频URL: {video_url[:100]}...")
    else:
        print(f"❌ 测试1失败：没有返回视频URL")

except Exception as e:
    print(f"❌ 测试1失败：{str(e)}")

print("\n")

# 测试2：使用Config对象（不传API Key）
print("=" * 60)
print("测试2: 使用Config对象（不传API Key）")
print("=" * 60)

try:
    config = Config()
    client2 = VideoGenerationClient(config=config)
    print("✅ 客户端2初始化成功（Config对象，无API Key）")

    video_url, response, last_frame_url = client2.video_generation(
        content_items=[
            TextContent(text="第二个测试场景")
        ],
        model="doubao-seedance-1-5-pro-251215",
        resolution="720p",
        ratio="16:9",
        duration=5,
        watermark=False,
        max_wait_time=120
    )

    if video_url:
        print(f"✅ 测试2成功！视频URL: {video_url[:100]}...")
    else:
        print(f"❌ 测试2失败：没有返回视频URL")

except Exception as e:
    print(f"❌ 测试2失败：{str(e)}")

print("\n")

# 测试3：查看Config对象需要哪些参数
print("=" * 60)
print("测试3: 查看Config对象签名")
print("=" * 60)

try:
    import inspect
    config_sig = inspect.signature(Config.__init__)
    print(f"Config类的初始化参数: {config_sig}")
except Exception as e:
    print(f"❌ 无法获取Config签名: {str(e)}")

print("\n")

# 测试4：查看是否有环境变量
print("=" * 60)
print("测试4: 检查当前环境变量")
print("=" * 60)

import os
coze_env_vars = {k: v for k, v in os.environ.items() if 'COZE' in k or 'coze' in k}
if coze_env_vars:
    print("发现COZE相关环境变量:")
    for k, v in coze_env_vars.items():
        print(f"  {k} = {v[:50]}..." if len(v) > 50 else f"  {k} = {v}")
else:
    print("❌ 未发现COZE相关环境变量")

print("\n")

# 测试5：尝试使用不同的环境变量名
print("=" * 60)
print("测试5: 检查是否有API_KEY相关的环境变量")
print("=" * 60)

api_key_vars = {k: v for k, v in os.environ.items() if 'API_KEY' in k or 'api_key' in k}
if api_key_vars:
    print("发现API_KEY相关环境变量:")
    for k, v in api_key_vars.items():
        print(f"  {k} = {v[:30]}..." if len(v) > 30 else f"  {k} = {v}")
else:
    print("❌ 未发现API_KEY相关环境变量")

print("\n")
print("=" * 60)
print("总结：")
print("=" * 60)
print("如果测试1或测试2成功，说明即梦API不需要额外的API Key配置")
print("如果都失败，说明需要配置API Key或环境变量")
