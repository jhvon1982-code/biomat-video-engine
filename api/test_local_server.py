#!/usr/bin/env python3
"""
直接在本地运行API服务器并测试
"""
import asyncio
import httpx
import json
import time
from datetime import datetime, timedelta

# 直接导入并运行API
import sys
sys.path.insert(0, '/workspace/projects/api')

from index import app
import uvicorn

async def test_local_api():
    """测试本地API"""
    print("🚀 启动本地API服务器...")

    # 启动服务器
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="info")
    server = uvicorn.Server(config)

    # 在后台运行服务器
    async def run_server():
        await server.serve()

    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(asyncio.run, run_server())

        # 等待服务器启动
        await asyncio.sleep(3)

        print("\n📡 测试本地API...")

        headers = {
            "Authorization": "Bearer bm_Pla1ic3_D3y3k3y_2k0k0k0k0k0k0k0k0k0k0k0k0k0k",
            "Content-Type": "application/json"
        }

        start_time = time.time()

        try:
            async with httpx.AsyncClient(timeout=600.0) as client:
                print("⏳ 发送请求...")
                response = await client.post(
                    "http://127.0.0.1:8000/api/v1/generate-video-simple",
                    headers=headers,
                    json={}
                )

            elapsed = time.time() - start_time
            print(f"⏱️  请求耗时: {elapsed:.2f}秒")

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

                    # 检查是否是真实视频
                    video_link = video_data.get('video_link', '')
                    if 'big_buck_bunny' in video_link.lower():
                        print(f"\n⚠️  仍然使用测试视频！")
                    else:
                        print(f"\n✅ 使用了真实生成的视频！")
            else:
                print(f"❌ API调用失败: {response.status_code}")
                print(f"响应: {response.text}")

        except Exception as e:
            print(f"❌ 错误: {str(e)}")
            import traceback
            traceback.print_exc()

        # 停止服务器
        await asyncio.sleep(1)
        server.should_exit = True

if __name__ == "__main__":
    asyncio.run(test_local_api())
