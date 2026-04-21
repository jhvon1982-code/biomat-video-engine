#!/usr/bin/env python3
"""
本地测试 - 直接测试视频生成逻辑（不通过HTTP）
"""
import asyncio
import httpx
import json
from datetime import datetime
import hashlib
import logging
from coze_coding_dev_sdk.video import VideoGenerationClient, TextContent
from coze_coding_dev_sdk import APIError
from coze_coding_utils.runtime_ctx.context import new_context

# 配置
COZE_API_TOKEN = "sat_CIaDvIIgWkvI7Ziny0Cdz6aIO7Sluw8qnyZXJsLVMp1t9kUuF5xX8qD0HB0kxQdC"
COZE_BOT_ID = "7624342475888590902"
COZE_API_URL = "https://api.coze.cn/open_api/v2/chat"

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_video_generation_logic():
    """测试完整的视频生成逻辑"""

    # 产品轮播
    PRODUCTS = ["PLGA", "PTLA", "PLCL", "PCL", "PTMC", "PGA", "PDO", "PLA"]

    # 根据日期选择产品
    date_str = datetime.now().strftime("%Y-%m-%d")
    hash_val = int(hashlib.md5(date_str.encode()).hexdigest(), 16)
    product_index = hash_val % len(PRODUCTS)
    material = PRODUCTS[product_index]

    print(f"📅 日期: {date_str}")
    print(f"🎯 选择产品: {material}")

    # 生成prompt
    prompt = f"""
请为材料 {material} 编写一个15秒产品推广视频的详细描述。

请返回以下JSON格式:
```json
{{
  "status": "success",
  "product": "{material} - 中文名称",
  "video_description": "详细的视频场景描述，用于AI视频生成",
  "duration": "15s",
  "seo_info": {{
    "title": "YouTube标题",
    "description": "YouTube描述",
    "tags": ["标签1", "标签2"]
  }}
}}
```

注意:
- video_description应该是一个详细的、生动的视频场景描述
- 描述应该包含产品特性、应用场景和视觉效果
"""

    print(f"\n📝 发送prompt给Coze Bot...")
    print(f"Prompt (前200字符): {prompt[:200]}...")

    # 调用Coze Bot
    async with httpx.AsyncClient(timeout=300.0) as client:
        response = await client.post(
            COZE_API_URL,
            headers={
                "Authorization": f"Bearer {COZE_API_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "bot_id": COZE_BOT_ID,
                "user": f"test_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "query": prompt,
                "stream": False
            }
        )
        result = response.json()

    if result.get("code") != 0:
        print(f"❌ Coze Bot API错误: {result.get('msg')}")
        return False

    # 提取响应
    response_text = result.get("messages", [{}])[-1].get("content", "")
    print(f"\n📨 Coze Bot响应长度: {len(response_text)} 字符")
    print(f"📨 Coze Bot响应 (前500字符):\n{response_text[:500]}")

    # 解析JSON
    try:
        result_data = json.loads(response_text)
        print(f"\n✅ JSON解析成功")
    except json.JSONDecodeError:
        import re
        print(f"\n⚠️ 直接JSON解析失败，尝试正则提取...")
        json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            result_data = json.loads(json_match.group(1))
            print(f"✅ 正则JSON解析成功")
        else:
            print(f"❌ 无法从响应中提取JSON")
            return False

    # 检查result_data
    print(f"\n🔍 result_data的键: {list(result_data.keys())}")
    print(f"\n📄 完整的result_data:")
    print(json.dumps(result_data, indent=2, ensure_ascii=False))

    # 检查video_description
    if "video_description" in result_data:
        video_description = result_data["video_description"]
        print(f"\n✅ 找到video_description!")
        print(f"📝 视频描述: {video_description}")
    else:
        print(f"\n❌ 没有找到video_description字段")
        print(f"可用的字段: {list(result_data.keys())}")
        return False

    # 尝试生成视频
    print(f"\n🎬 开始调用视频生成API...")
    try:
        ctx = new_context(method="video.generate")
        client = VideoGenerationClient(ctx=ctx)

        print(f"⏳ 正在生成视频（这可能需要几分钟）...")
        generated_url, response, last_frame_url = await client.video_generation_async(
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

        if generated_url:
            print(f"\n✅ 视频生成成功!")
            print(f"📹 视频URL: {generated_url}")
            print(f"📊 响应: {response}")
            return True
        else:
            print(f"\n❌ 视频生成失败 - 没有返回URL")
            print(f"📊 响应: {response}")
            return False

    except APIError as e:
        print(f"\n❌ 视频生成API错误: {str(e)}")
        return False
    except Exception as e:
        print(f"\n❌ 未知错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_video_generation_logic())
    if success:
        print("\n✅ 完整测试成功!")
    else:
        print("\n❌ 测试失败，请检查上述错误")
