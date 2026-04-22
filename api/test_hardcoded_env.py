#!/usr/bin/env python3
"""
测试硬编码环境变量后的视频生成
"""
import asyncio
import httpx
import json
from datetime import datetime

# 硬编码环境变量（模拟API中的配置）
import os
os.environ['COZE_WORKLOAD_IDENTITY_API_KEY'] = 'M2pyUXJPeWFDdUhqRmUyYnllaVNPNWl4YnY5RlljaHc6dXA5Tk5kUElmcHk2MXZlU203djh5dGx5dTA3WnJsWnZ4OUMwTjJSdG1EaHZEMXppMFhHNENQbmlZYzJkMnB1Rg=='
os.environ['COZE_INTEGRATION_BASE_URL'] = 'https://integration.coze.cn'
os.environ['COZE_INTEGRATION_MODEL_BASE_URL'] = 'https://integration.coze.cn/api/v3'

from coze_coding_dev_sdk.video import VideoGenerationClient, TextContent

async def test_video_generation_with_env():
    """测试使用硬编码环境变量的视频生成"""

    print("=" * 60)
    print("测试：使用硬编码环境变量生成视频")
    print("=" * 60)

    # 验证环境变量已设置
    print("\n检查环境变量:")
    print(f"  COZE_WORKLOAD_IDENTITY_API_KEY: {'✅ 已设置' if os.getenv('COZE_WORKLOAD_IDENTITY_API_KEY') else '❌ 未设置'}")
    print(f"  COZE_INTEGRATION_BASE_URL: {os.getenv('COZE_INTEGRATION_BASE_URL', '❌ 未设置')}")
    print(f"  COZE_INTEGRATION_MODEL_BASE_URL: {os.getenv('COZE_INTEGRATION_MODEL_BASE_URL', '❌ 未设置')}")

    # 创建客户端
    print("\n初始化VideoGenerationClient...")
    try:
        client = VideoGenerationClient()
        print("✅ 客户端初始化成功")
    except Exception as e:
        print(f"❌ 客户端初始化失败: {str(e)}")
        return False

    # 测试视频描述
    video_description = """
    一个专业的医学实验室场景，显微镜视角下的PGA（聚乙醇酸）缝合线纤维结构。
    纯白色的PGA纤维在蓝色背景中缓慢展开，展示其高强度和快速降解的特性。
    镜头缓慢推进，展示纤维的微观结构和均匀的直径。
    光影效果柔和，体现医用级生物材料的质感和纯净度。
    """

    print(f"\n开始生成视频...")
    print(f"  模型: doubao-seedance-1-5-pro-251215")
    print(f"  分辨率: 720p, 16:9")
    print(f"  时长: 5秒")
    print(f"  描述: {video_description[:50]}...")

    try:
        video_url, response, last_frame_url = await client.video_generation_async(
            content_items=[
                TextContent(text=video_description)
            ],
            model="doubao-seedance-1-5-pro-251215",
            resolution="720p",
            ratio="16:9",
            duration=5,
            watermark=False,
            max_wait_time=900,
            generate_audio=True
        )

        if video_url:
            print("\n✅✅✅ 视频生成成功！")
            print(f"\n📹 视频URL:")
            print(f"   {video_url}")
            print(f"\n📊 响应信息:")
            print(f"   任务ID: {response.get('id', 'N/A')}")
            print(f"   状态: {response.get('status', 'N/A')}")
            print(f"   分辨率: {response.get('resolution', 'N/A')}")
            print(f"   时长: {response.get('duration', 'N/A')}秒")
            return True
        else:
            print(f"\n❌ 视频生成失败 - 没有返回URL")
            print(f"响应: {response}")
            return False

    except Exception as e:
        print(f"\n❌ 视频生成失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_video_generation_with_env())
    if success:
        print("\n" + "=" * 60)
        print("✅ 测试成功！硬编码环境变量方案可行")
        print("=" * 60)
        print("\n下一步:")
        print("1. 提交代码到GitHub")
        print("2. 等待Render自动部署")
        print("3. 测试主API端点")
    else:
        print("\n" + "=" * 60)
        print("❌ 测试失败")
        print("=" * 60)
