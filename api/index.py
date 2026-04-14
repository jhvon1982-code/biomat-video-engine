"""
Vercel Serverless Function API Adapter
适配Vercel部署的API端点 - 调用Coze Bot API
"""
import os
import json
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import httpx

app = Flask(__name__)
CORS(app)

# API Configuration
BIOMAT_API_KEY = os.getenv("BIOMAT_API_KEY", "bm_Pla1ic3_D3y3k3y_2k0k0k0k0k0k0k0k0k0k0k0k0k0k")

# Coze Bot Configuration
COZE_BOT_ID = os.getenv("COZE_BOT_ID", "7624342475888590902")
COZE_API_TOKEN = os.getenv("COZE_API_TOKEN", "sat_CIaDvIIgWkvI7Ziny0Cdz6aIO7Sluw8qnyZXJsLVMp1t9kUuF5xX8qD0HB0kxQdC")
COZE_API_URL = "https://api.coze.cn/open_api/v2/chat"

# Validate API key
def validate_api_key(request):
    """验证API密钥"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return False
    provided_key = auth_header.replace('Bearer ', '')
    return provided_key == BIOMAT_API_KEY

# Generate video endpoint
@app.route('/api/v1/generate-video', methods=['POST'])
def generate_video():
    """视频生成API端点"""
    # Validate API key
    if not validate_api_key(request):
        return jsonify({
            "success": False,
            "error": "Unauthorized: Invalid API key"
        }), 401

    # Parse request
    try:
        data = request.get_json()
        material = data.get('material', 'auto')
        scenes = data.get('scenes', 3)
        platform = data.get('platform', 'youtube')
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Invalid request format: {str(e)}"
        }), 400

    # Execute workflow via Coze Bot
    try:
        # Prepare prompt
        if material == "auto":
            prompt = f"""
请执行Biomat_Video_Engine Pro v2.0完整工作流：

1. 自动分析当前热门生物材料趋势（TikTok + YouTube）
2. 识别市场痛点
3. 自动匹配最优材料策略
4. 生成{scenes}个关键场景视频（使用即梦seedance2.0）
5. 生成完整的YouTube SEO包装
6. 生成TikTok发布指南

平台需求：{platform}

请严格按照以下JSON格式返回结果：
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
请执行Biomat_Video_Engine Pro v2.0工作流，材料：{material}：

1. 分析{material}的市场趋势和痛点
2. 生成{scenes}个关键场景视频
3. 生成YouTube SEO包装
4. 生成TikTok发布指南

平台需求：{platform}

请严格按照JSON格式返回结果（同上）。
            """

        # Call Coze Bot API
        async def call_coze_bot():
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
                        "stream": false
                    },
                    timeout=300.0
                )
                return response.json()

        # Synchronous wrapper
        import asyncio
        try:
            result = asyncio.run(call_coze_bot())
        except RuntimeError:
            # If no event loop, create one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(call_coze_bot())

        # Check Coze API response
        if result.get("code") != 0:
            return jsonify({
                "success": False,
                "error": f"Coze API error: {result.get('msg', 'Unknown error')}"
            }), 500

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

        # Return success
        return jsonify({
            "success": True,
            "data": result_data,
            "execution_time": datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Workflow execution failed: {str(e)}"
        }), 500

# Health check endpoint
@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        "status": "healthy",
        "service": "Biomat_Video_Engine",
        "version": "2.0",
        "timestamp": datetime.now().isoformat()
    })

# Vercel entry point
app_handler = app
