#!/usr/bin/env python3
"""
测试视频生成API
"""
import asyncio
import sys
import os

# 添加api目录到路径
sys.path.insert(0, '/workspace/projects/api')

from coze_coding_dev_sdk.video import VideoGenerationClient, TextContent
from coze_coding_dev_sdk import APIError
from coze_coding_utils.runtime_ctx.context import new_context

async def test_video_generation():
    """测试视频生成功能"""
    print("🎬 开始测试即梦视频生成API...")

    # 测试描述 - 使用PLGA材料的描述
    test_prompt = """
    一个专业的医学实验室场景，显微镜视角下的PLGA（聚乳酸-羟基乙酸共聚物）微球结构，
    纯白色的微球在蓝色背景中缓慢旋转，展示其完美的球形结构和均匀的尺寸分布。
    光影效果柔和，体现高科技生物材料的质感。
    镜头缓慢推进，展示微球表面的细微纹理。
    """

    try:
        # 创建客户端
        ctx = new_context(method="video.generate")
        client = VideoGenerationClient(ctx=ctx)

        print(f"📝 生成提示: {test_prompt[:100]}...")
        print("⏳ 正在生成视频，这可能需要几分钟...")

        # 调用视频生成API
        video_url, response, last_frame_url = await client.video_generation_async(
            content_items=[
                TextContent(text=test_prompt)
            ],
            model="doubao-seedance-1-5-pro-251215",
            resolution="720p",
            ratio="16:9",
            duration=5,
            watermark=False,
            max_wait_time=600,  # 最多等待10分钟
            generate_audio=True
        )

        if video_url:
            print("✅ 视频生成成功!")
            print(f"📹 视频URL: {video_url}")
            print(f"🖼️  最后一帧URL: {last_frame_url}")
            print(f"📊 响应详情: {response}")
            return True
        else:
            print("❌ 视频生成失败 - �有返回视频URL")
            print(f"📊 响应详情: {response}")
            return False

    except APIError as e:
        print(f"❌ API错误: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_video_generation())
    sys.exit(0 if success else 1)
