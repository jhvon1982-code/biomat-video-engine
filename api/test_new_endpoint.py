#!/usr/bin/env python3
"""
测试新端点 - 直接返回真实视频
"""
import asyncio
import httpx
import json

BIOMAT_API_KEY = "bm_Pla1ic3_D3y3k3y_2k0k0k0k0k0k0k0k0k0k0k0k0k0k"
TEST_URL = "https://biomat-video-engine.onrender.com/api/v1/test-generated-video"

async def test_new_endpoint():
    """测试新端点"""
    print("🔍 测试新端点 - 应该直接返回真实视频URL")

    headers = {
        "Authorization": f"Bearer {BIOMAT_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            print(f"📡 请求URL: {TEST_URL}")
            response = await client.post(
                TEST_URL,
                headers=headers,
                json={}
            )

            print(f"\n📊 状态码: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                print("✅ 调用成功!")

                print(f"\n📄 返回数据:")
                print(json.dumps(result, indent=2, ensure_ascii=False))

                if "data" in result and len(result["data"]) > 0:
                    video_data = result["data"][0]
                    video_link = video_data.get('video_link', '')

                    print(f"\n🎬 视频信息:")
                    print(f"  产品: {video_data.get('product')}")
                    print(f"  视频链接: {video_link}")

                    # 检查是否是真实视频
                    if 'video_generate_cgt-' in video_link:
                        print(f"\n✅✅✅ 这是真实生成的视频！")
                        print(f"💡 可以使用此URL更新Make工作流节点1的URL为：")
                        print(f"   {TEST_URL}")
                        print(f"   然后手动触发Make工作流测试")
                    else:
                        print(f"\n⚠️  不是预期的视频格式")
            else:
                print(f"❌ 调用失败")
                print(f"响应: {response.text}")

    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_new_endpoint())
