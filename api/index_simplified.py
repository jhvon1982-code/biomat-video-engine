#!/usr/bin/env python3
"""
简化版本 - 直接返回预生成视频，不尝试实时生成
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import logging
from datetime import datetime

app = FastAPI()

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

# 预生成的真实视频（使用有效的永久URL）
PRE_GENERATED_VIDEOS = {
    "PLGA": "https://www.w3schools.com/html/mov_bbb.mp4",  # 暂时使用测试视频，后续替换
    "PTLA": "https://www.w3schools.com/html/mov_bbb.mp4",
    "PLCL": "https://www.w3schools.com/html/mov_bbb.mp4",
    "PCL": "https://www.w3schools.com/html/mov_bbb.mp4",
    "PTMC": "https://www.w3schools.com/html/mov_bbb.mp4",
    "PGA": "https://www.w3schools.com/html/mov_bbb.mp4",
    "PDO": "https://www.w3schools.com/html/mov_bbb.mp4",
    "PLA": "https://www.w3schools.com/html/mov_bbb.mp4"
}

# 产品信息
PRODUCT_INFO = {
    "PLGA": {"name": "聚乳酸-羟基乙酸共聚物", "feature": "可降解速率可调，广泛用于药物控释和组织工程"},
    "PTLA": {"name": "聚左旋乳酸", "feature": "高强度、可降解，适用于骨科固定材料"},
    "PLCL": {"name": "聚乳酸-己内酯共聚物", "feature": "力学性能优异，可调节降解速率"},
    "PCL": {"name": "聚己内酯", "feature": "熔点低、易加工，适用于3D打印和药物载体"},
    "PTMC": {"name": "聚三亚甲基碳酸酯", "feature": "弹性好、生物相容性强，适用于心脏支架"},
    "PGA": {"name": "聚乙醇酸", "feature": "高强度、快速降解，适用于缝合线"},
    "PDO": {"name": "聚对二氧环己酮", "feature": "柔软、可降解，适用于美容缝合"},
    "PLA": {"name": "聚乳酸", "feature": "可生物降解，环保材料"}
}

@app.get("/api/v1/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "Biomat_Video_Engine_Simplified",
        "version": "2.1",
        "mode": "pre-generated-videos",
        "video_pool_size": len(PRE_GENERATED_VIDEOS),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/v1/generate-video-simple")
async def generate_video_simple(request: Request):
    """简化版本 - 直接返回预生成视频"""
    if not validate_api_key(request):
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API key")

    try:
        # 产品轮播
        import hashlib
        PRODUCTS = ["PLGA", "PTLA", "PLCL", "PCL", "PTMC", "PGA", "PDO", "PLA"]

        date_str = datetime.now().strftime("%Y-%m-%d")
        hash_val = int(hashlib.md5(date_str.encode()).hexdigest(), 16)
        product_index = hash_val % len(PRODUCTS)
        material = PRODUCTS[product_index]

        logger.info(f"Selected material: {material} for date: {date_str}")

        # 获取产品信息
        product_data = PRODUCT_INFO.get(material, PRODUCT_INFO["PGA"])
        product_name = product_data["name"]
        feature = product_data["feature"]

        # 获取视频URL
        video_url = PRE_GENERATED_VIDEOS.get(material, PRE_GENERATED_VIDEOS["PGA"])

        # 构建响应
        result_data = {
            "status": "success",
            "product": f"{material} - {product_name}",
            "video_link": video_url,
            "duration": "5s",
            "seo_info": {
                "title": f"云南聚和{material}{product_name}_医用级生物材料",
                "description": f"云南聚和{material}{product_name}，{feature}。符合ISO 10993生物相容性标准，广泛应用于医疗器械和生物材料领域。",
                "tags": ["云南聚和", material, product_name, "医用材料", "生物相容性", "可降解"]
            },
            "note": "Using pre-generated video pool (simplified version)"
        }

        logger.info(f"Returning video for {material}: {video_url[:100]}...")

        return {
            "success": True,
            "data": [result_data],
            "execution_time": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Vercel entry point
app_handler = app
