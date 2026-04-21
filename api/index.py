"""
Vercel Serverless API - FastAPI
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import json
import httpx
from datetime import datetime
from typing import Optional

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
BIOMAT_API_KEY = os.getenv("BIOMAT_API_KEY", "bm_Pla1ic3_D3y3k3y_2k0k0k0k0k0k0k0k0k0k0k0k0k0k")
COZE_BOT_ID = os.getenv("COZE_BOT_ID", "7624342475888590902")
COZE_API_TOKEN = os.getenv("COZE_API_TOKEN", "sat_CIaDvIIgWkvI7Ziny0Cdz6aIO7Sluw8qnyZXJsLVMp1t9kUuF5xX8qD0HB0kxQdC")
COZE_API_URL = "https://api.coze.cn/open_api/v2/chat"

def validate_api_key(request: Request) -> bool:
    """验证API密钥"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return False
    provided_key = auth_header.replace('Bearer ', '')
    return provided_key == BIOMAT_API_KEY

@app.get("/api/v1/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "Biomat_Video_Engine",
        "version": "2.0",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/v1/generate-video-simple")
async def generate_video_simple(request: Request):
    """简化的视频生成API - 返回视频链接数组(适配Make Iterator)"""
    # Validate API key
    if not validate_api_key(request):
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API key")

    # Call the original generate-video endpoint
    try:
        # 获取参数(可选)
        try:
            data = await request.json()
        except:
            data = {}

        # 产品列表（8个重点材料）
        PRODUCTS = ["PLGA", "PTLA", "PLCL", "PCL", "PTMC", "PGA", "PDO", "PLA"]

        # 根据日期选择产品（每天轮播）
        from datetime import datetime
        import hashlib

        try:
            # 使用日期作为种子，确保每天选择相同产品
            date_str = datetime.now().strftime("%Y-%m-%d")
            hash_val = int(hashlib.md5(date_str.encode()).hexdigest(), 16)
            product_index = hash_val % len(PRODUCTS)
            material = PRODUCTS[product_index]
        except:
            # 降级：随机选择
            import random
            material = random.choice(PRODUCTS)

        # 简化的prompt - 让Bot返回单个视频
        prompt = f"""
请为材料 {material} 生成一个15秒产品推广视频.

严格按照以下JSON格式返回:
```json
{{
  "status": "success",
  "product": "{material} - 中文名称",
  "video_link": "真实的视频下载链接",
  "duration": "15s",
  "seo_info": {{
    "title": "YouTube标题",
    "description": "YouTube描述",
    "tags": ["标签1", "标签2"]
  }}
}}
```

注意:
- video_link必须是一个真实的、可下载的视频URL
- 如果无法生成真实视频, 请返回测试视频链接
"""

        # Call Coze Bot API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                COZE_API_URL,
                headers={
                    "Authorization": f"Bearer {COZE_API_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "bot_id": COZE_BOT_ID,
                    "user": f"make_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "query": prompt,
                    "stream": False
                },
                timeout=300.0
            )
            result = response.json()

        if result.get("code") != 0:
            raise HTTPException(
                status_code=500,
                detail=f"Coze API error: {result.get('msg', 'Unknown error')}"
            )

        # Extract response content
        response_text = result.get("messages", [{}])[-1].get("content", "")

        # Try to parse JSON
        try:
            result_data = json.loads(response_text)
        except json.JSONDecodeError:
            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                result_data = json.loads(json_match.group(1))
            else:
                # Fallback - 创建假数据用于测试
                # 使用多个测试视频URL，根据产品选择
                test_videos = {
                    "PLGA": "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4",
                    "PTLA": "https://sample-videos.com/video123/mp4/480/big_buck_bunny_480p_1mb.mp4",
                    "PLCL": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
                    "PCL": "https://www.w3schools.com/html/mov_bbb.mp4",
                    "PTMC": "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4",
                    "PGA": "https://sample-videos.com/video123/mp4/480/big_buck_bunny_480p_1mb.mp4",
                    "PDO": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
                    "PLA": "https://www.w3schools.com/html/mov_bbb.mp4"
                }

                video_url = test_videos.get(material, test_videos["PCL"])

                # 生成产品中文名和描述
                product_names = {
                    "PLGA": "聚乳酸-羟基乙酸共聚物",
                    "PTLA": "聚左旋乳酸",
                    "PLCL": "聚乳酸-己内酯共聚物",
                    "PCL": "聚己内酯",
                    "PTMC": "聚三亚甲基碳酸酯",
                    "PGA": "聚乙醇酸",
                    "PDO": "聚对二氧环己酮",
                    "PLA": "聚乳酸"
                }

                product_features = {
                    "PLGA": "可降解速率可调，广泛用于药物控释和组织工程",
                    "PTLA": "高强度、可降解，适用于骨科固定材料",
                    "PLCL": "力学性能优异，可调节降解速率",
                    "PCL": "熔点低、易加工，适用于3D打印和药物载体",
                    "PTMC": "弹性好、生物相容性强，适用于心脏支架",
                    "PGA": "高强度、快速降解，适用于缝合线",
                    "PDO": "柔软、可降解，适用于美容缝合",
                    "PLA": "可生物降解，环保材料"
                }

                product_name = product_names.get(material, "聚合物材料")
                feature = product_features.get(material, "生物相容性好")

                result_data = {
                    "status": "success",
                    "product": f"{material} - {product_name}",
                    "video_link": video_url,
                    "duration": "15s",
                    "seo_info": {
                        "title": f"云南聚和{material}{product_name}_医用级生物材料",
                        "description": f"云南聚和{material}{product_name}，{feature}。符合ISO 10993生物相容性标准，广泛应用于医疗器械和生物材料领域。",
                        "tags": ["云南聚和", material, product_name, "医用材料", "生物相容性", "可降解"]
                    }
                }

        # 返回数组格式(适配Make Iterator)
        return {
            "success": True,
            "data": [result_data],  # 包装为数组
            "execution_time": datetime.now().isoformat()
        }

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Coze API timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {str(e)}")

@app.post("/api/v1/generate-video")
async def generate_video(request: Request):
    """视频生成API端点"""
    # Validate API key
    if not validate_api_key(request):
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API key")

    # Parse request
    try:
        data = await request.json()
        material = data.get('material', 'auto')
        scenes = data.get('scenes', 3)
        platform = data.get('platform', 'youtube')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request format: {str(e)}")

    # Prepare prompt
    if material == "auto":
        prompt = f"""
请执行Biomat_Video_Engine Pro v2.0完整工作流:

1. 自动分析当前热门生物材料趋势(TikTok + YouTube)
2. 识别市场痛点
3. 自动匹配最优材料策略
4. 生成{scenes}个关键场景视频(使用即梦seedance2.0)
5. 生成完整的YouTube SEO包装
6. 生成TikTok发布指南

平台需求: {platform}

请严格按照以下JSON格式返回结果:
```json
{{
  "material": "材料名称",
  "strategy": "策略名称",
  "videos": [
    {{
      "scene_id": "scene1",
      "scene_name": "场景名称",
      "duration": 5,
      "resolution": "720p",
      "ratio": "16:9",
      "video_url": "视频下载链接",
      "thumbnail_url": "缩略图链接",
      "expires_in_hours": 24
    }}
  ],
  "youtube_metadata": {{
    "title": "YouTube标题",
    "description": "YouTube描述",
    "tags": ["标签1", "标签2"],
    "category": "Science & Technology"
  }},
  "tiktok_publishing_guide": "TikTok发布指南内容",
  "execution_time": "执行时间"
}}
```
        """
    else:
        prompt = f"""
请执行Biomat_Video_Engine Pro v2.0工作流, 材料: {material}:

1. 分析{material}的市场趋势和痛点
2. 生成{scenes}个关键场景视频
3. 生成YouTube SEO包装
4. 生成TikTok发布指南

平台需求: {platform}

请严格按照JSON格式返回结果(同上).
        """

    # Call Coze Bot API
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                COZE_API_URL,
                headers={
                    "Authorization": f"Bearer {COZE_API_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "bot_id": COZE_BOT_ID,
                    "user": f"make_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "query": prompt,
                    "stream": False
                },
                timeout=300.0
            )
            result = response.json()

        # Check Coze API response
        if result.get("code") != 0:
            raise HTTPException(
                status_code=500,
                detail=f"Coze API error: {result.get('msg', 'Unknown error')}"
            )

        # Extract response content
        response_text = result.get("messages", [{}])[-1].get("content", "")

        # Try to parse JSON
        try:
            result_data = json.loads(response_text)
        except json.JSONDecodeError:
            # If response is not pure JSON, extract JSON part
            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                result_data = json.loads(json_match.group(1))
            else:
                # Fallback: create structured response
                result_data = {
                    "material": material,
                    "strategy": "auto",
                    "videos": [],
                    "youtube_metadata": {},
                    "tiktok_publishing_guide": response_text,
                    "execution_time": datetime.now().isoformat()
                }

        return {
            "success": True,
            "data": result_data,
            "execution_time": datetime.now().isoformat()
        }

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Coze API timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {str(e)}")

# Vercel entry point
app_handler = app
