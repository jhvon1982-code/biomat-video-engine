#!/usr/bin/env python3
"""
诊断端点 - 检查视频生成失败的具体原因
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import logging
from datetime import datetime
from typing import Optional
from coze_coding_dev_sdk.video import VideoGenerationClient, TextContent
from coze_coding_dev_sdk import APIError

app = FastAPI()

# 配置即梦视频生成SDK环境变量
import os
os.environ['COZE_WORKLOAD_IDENTITY_API_KEY'] = 'M2pyUXJPeWFDdUhqRmUyYnllaVNPNWl4YnY5RlljaHc6dXA5Tk5kUElmcHk2MXZlU203djh5dGx5dTA3WnJsWnZ4OUMwTjJSdG1EaHZEMXppMFhHNENQbmlZYzJkMnB1Rg=='
os.environ['COZE_INTEGRATION_BASE_URL'] = 'https://integration.coze.cn'
os.environ['COZE_INTEGRATION_MODEL_BASE_URL'] = 'https://integration.coze.cn/api/v3'

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BIOMAT_API_KEY = os.getenv("BIOMAT_API_KEY", "bm_Pla1ic3_D3y3k3y_2k0k0k0k0k0k0k0k0k0k0k0k0k0k")

def validate_api_key(request: Request) -> bool:
    """验证API密钥"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return False
    provided_key = auth_header.replace('Bearer ', '')
    return provided_key == BIOMAT_API_KEY

@app.get("/api/v1/diagnose")
async def diagnose():
    """诊断端点 - 检查环境配置"""
    return {
        "status": "diagnosing",
        "environment": {
            "COZE_WORKLOAD_IDENTITY_API_KEY": os.getenv('COZE_WORKLOAD_IDENTITY_API_KEY', 'NOT SET'),
            "COZE_INTEGRATION_BASE_URL": os.getenv('COZE_INTEGRATION_BASE_URL', 'NOT SET'),
            "COZE_INTEGRATION_MODEL_BASE_URL": os.getenv('COZE_INTEGRATION_MODEL_BASE_URL', 'NOT SET'),
            "COZE_API_TOKEN": os.getenv('COZE_API_TOKEN', 'NOT SET'),
        },
        "test_video_generation": "Use POST /api/v1/test-video-gen"
    }

@app.post("/api/v1/test-video-gen")
async def test_video_gen():
    """测试视频生成 - 返回详细错误信息"""
    diagnostics = {
        "step": [],
        "success": False,
        "video_url": None,
        "error": None
    }

    try:
        diagnostics["step"].append("Step 1: Checking environment variables")
        env_key = os.getenv('COZE_WORKLOAD_IDENTITY_API_KEY')
        if not env_key:
            diagnostics["error"] = "COZE_WORKLOAD_IDENTITY_API_KEY not set"
            return diagnostics
        diagnostics["step"].append(f"✅ Environment variables loaded (key length: {len(env_key)})")

        diagnostics["step"].append("Step 2: Initializing VideoGenerationClient")
        try:
            client = VideoGenerationClient()
            diagnostics["step"].append("✅ VideoGenerationClient initialized")
        except Exception as e:
            diagnostics["error"] = f"Failed to initialize client: {str(e)}"
            return diagnostics

        diagnostics["step"].append("Step 3: Preparing video generation request")
        video_description = "A simple test scene"
        diagnostics["step"].append(f"✅ Description prepared: {video_description}")

        diagnostics["step"].append("Step 4: Calling video_generation API")
        try:
            video_url, response, _ = client.video_generation(
                content_items=[
                    TextContent(text=video_description)
                ],
                model="doubao-seedance-1-5-pro-251215",
                resolution="720p",
                ratio="16:9",
                duration=5,
                watermark=False,
                max_wait_time=300,
                generate_audio=True
            )

            if video_url:
                diagnostics["step"].append(f"✅ Video generation succeeded")
                diagnostics["success"] = True
                diagnostics["video_url"] = video_url
                diagnostics["response"] = response
            else:
                diagnostics["error"] = "Video generation returned no URL"
                diagnostics["response"] = response

        except APIError as e:
            diagnostics["error"] = f"API Error: {str(e)}"
            diagnostics["step"].append(f"❌ API Error: {str(e)}")
        except Exception as e:
            diagnostics["error"] = f"Unexpected error: {str(e)}"
            diagnostics["step"].append(f"❌ Unexpected error: {str(e)}")

    except Exception as e:
        diagnostics["error"] = f"General error: {str(e)}"
        import traceback
        diagnostics["traceback"] = traceback.format_exc()

    return diagnostics
