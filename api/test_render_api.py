#!/usr/bin/env python3
"""
测试Render API - 模拟Make工作流调用
"""
import asyncio
import httpx
import json
from datetime import datetime

BIOMAT_API_KEY = "bm_Pla1ic3_D3y3k3y_2k0k0k0k0k0k0k0k0k0k0k0k0k0k"
RENDER_API_URL = "https://biomat-video-engine.onrender.com/api/v1/generate-video-simple"

async def test_api():
    """测试API"""
    print("🔍 测试Render API...")

    headers = {
        "Authorization": f"Bearer {BIOMAT_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        print(f"📡 请求URL: {RENDER_API_URL}")
        print("⏳ 等待响应（API可能需要几分钟生成视频）...")

        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                RENDER_API_URL,
                headers=headers,
                json={},
            )

            print(f"📊 状态码: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                print("✅ API调用成功!")
                print(f"\n📄 返回数据:")
                print(json.dumps(result, indent=2, ensure_ascii=False))

                if "data" in result and len(result["data"]) > 0:
                    video_data = result["data"][0]
                    print(f"\n🎬 视频信息:")
                    print(f"  产品: {video_data.get('product')}")
                    print(f"  视频链接: {video_data.get('video_link')}")
                    print(f"  时长: {video_data.get('duration')}")

                    seo_info = video_data.get('seo_info', {})
                    if seo_info:
                        print(f"\n📝 SEO信息:")
                        print(f"  标题: {seo_info.get('title')}")
                        print(f"  描述: {seo_info.get('description')}")
                        print(f"  标签: {seo_info.get('tags')}")
                return True
            else:
                print(f"❌ API调用失败")
                print(f"响应内容: {response.text}")
                return False

    except httpx.TimeoutException:
        print("⏱️  请求超时")
        return False
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_api())
    if success:
        print("\n✅ 测试通过 - API正常工作，可以上传到YouTube")
    else:
        print("\n❌ 测试失败 - 请检查API部署状态")
