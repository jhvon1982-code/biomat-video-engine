#!/usr/bin/env python3
"""
直接测试视频生成API（不依赖Coze Bot）
"""
import asyncio
from coze_coding_dev_sdk.video import VideoGenerationClient, TextContent
from coze_coding_dev_sdk import APIError
from coze_coding_utils.runtime_ctx.context import new_context
import logging

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_direct_video_generation():
    """直接测试视频生成"""

    # 预设的PGA视频描述
    video_description = """
    一个专业的医学实验室场景，显微镜视角下的PGA（聚乙醇酸）缝合线纤维结构。
    纯白色的PGA纤维在蓝色背景中缓慢展开，展示其高强度和快速降解的特性。
    镜头缓慢推进，展示纤维的微观结构和均匀的直径。
    光影效果柔和，体现医用级生物材料的质感和纯净度。
    背景中有一些淡化的医疗设备轮廓，营造专业的医学氛围。
    """

    print(f"📝 视频描述: {video_description[:100]}...")

    try:
        # 创建客户端
        ctx = new_context(method="video.generate")
        client = VideoGenerationClient(ctx=ctx)

        print(f"\n⏳ 开始生成视频（这可能需要几分钟）...")
        print(f"🎬 模型: doubao-seedance-1-5-pro-251215")
        print(f"📐 分辨率: 720p, 16:9")
        print(f"⏱️  时长: 5秒")

        # 调用视频生成API
        video_url, response, last_frame_url = await client.video_generation_async(
            content_items=[
                TextContent(text=video_description)
            ],
            model="doubao-seedance-1-5-pro-251215",
            resolution="720p",
            ratio="16:9",
            duration=5,
            watermark=False,
            max_wait_time=600,
            generate_audio=True
        )

        if video_url:
            print(f"\n✅ 视频生成成功!")
            print(f"\n📹 视频URL:")
            print(f"   {video_url}")
            print(f"\n📊 生成信息:")
            print(f"   视频ID: {response.get('id')}")
            print(f"   状态: {response.get('status')}")
            print(f"   分辨率: {response.get('resolution')}")
            print(f"   比例: {response.get('ratio')}")
            print(f"   时长: {response.get('duration')}秒")
            print(f"   帧率: {response.get('framespersecond')} fps")
            print(f"   带音频: {response.get('generate_audio')}")
            print(f"\n💡 下一步:")
            print(f"   将此URL用于Make工作流，上传到YouTube")
            return True
        else:
            print(f"\n❌ 视频生成失败 - 没有返回URL")
            print(f"\n📊 完整响应:")
            print(f"   {json.dumps(response, indent=2, ensure_ascii=False)}")
            return False

    except APIError as e:
        print(f"\n❌ 视频生成API错误: {str(e)}")
        return False
    except Exception as e:
        print(f"\n❌ 未知错误: {str(e)}")
        import traceback
        import json
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import json
    success = asyncio.run(test_direct_video_generation())
    if success:
        print("\n✅ 测试成功 - 视频生成API工作正常")
    else:
        print("\n❌ 测试失败")
