#!/usr/bin/env python3
"""
简化版API - 直接生成视频，跳过Coze Bot
用于调试主API问题
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
from coze_coding_utils.runtime_ctx.context import new_context

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

# Configuration
BIOMAT_API_KEY = os.getenv("BIOMAT_API_KEY", "bm_Pla1ic3_D3y3k3y_2k0k0k0k0k0k0k0k0k0k0k0k0k0k")

def validate_api_key(request: Request) -> bool:
    """验证API密钥"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return False
    provided_key = auth_header.replace('Bearer ', '')
    return provided_key == BIOMAT_API_KEY

# 产品视频描述映射
PRODUCT_DESCRIPTIONS = {
    "PLGA": "一个专业的医学实验室场景，显微镜视角下的PLGA（聚乳酸-羟基乙酸共聚物）微球结构。纯白色的微球在蓝色背景中缓慢旋转，展示其完美的球形结构和均匀的尺寸分布。光影效果柔和，体现高科技生物材料的质感。镜头缓慢推进，展示微球表面的细微纹理。",
    "PTLA": "一个现代化的医疗设备车间，展示PTLA（聚左旋乳酸）骨科固定材料的加工过程。高纯度的PTLA材料在精密机械的切割下成型，材料呈现出半透明的乳白色。镜头切换到X光视角，展示材料在人体骨骼中的应用效果。背景有医疗影像设备的蓝绿色光芒。",
    "PLCL": "一个高科技材料研发实验室，PLCL（聚乳酸-己内酯共聚物）薄膜在测试设备中进行拉伸测试。材料展现出优异的弹性，拉伸后能够恢复原状。显微镜视角展示材料的分子结构，均匀的分子链排列清晰可见。实验室环境洁净，LED照明营造科技感。",
    "PCL": "一个3D打印实验室，PCL（聚己内酯）材料正在被熔融沉积打印成复杂的支架结构。白色的PCL丝材在打印头上缓慢移动，层层堆叠形成网格状的医用支架。镜头特写打印细节，展示材料的柔韧性和可塑性。背景有CAD设计图纸的蓝光。",
    "PTMC": "一个心血管介入手术室，PTMC（聚三亚甲基碳酸酯）心脏支架在血管模拟器中展开。支架具有良好的弹性，能够适应血管的弯曲。高倍显微镜展示支架的网状结构和表面光滑度。手术室灯光柔和，有监护设备的红色指示灯闪烁。",
    "PGA": "一个专业的医学实验室场景，显微镜视角下的PGA（聚乙醇酸）缝合线纤维结构。纯白色的PGA纤维在蓝色背景中缓慢展开，展示其高强度和快速降解的特性。镜头缓慢推进，展示纤维的微观结构和均匀的直径。光影效果柔和，体现医用级生物材料的质感和纯净度。",
    "PDO": "一个整形外科诊所，PDO（聚对二氧环己酮）可吸收缝合线在皮肤组织的显微视角下展示。透明的PDO纤维在肌理清晰的组织模型中穿行，材料柔软而强韧。镜头展示材料的柔韧性和生物相容性。背景有柔和的手术灯光和医疗设备的金属光泽。",
    "PLA": "一个环保材料展示空间，PLA（聚乳酸）颗粒在自动化流水线上被加工成医用级可降解材料。淡黄色的PLA颗粒在透明容器中展示，背景有绿色植物和循环利用的图标，体现环保理念。镜头切换到材料的降解过程，展示其在自然环境中的生物降解特性。"
}

# 产品信息映射
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
        "service": "Biomat_Video_Engine_Direct",
        "version": "3.0",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/v1/generate-video-direct")
async def generate_video_direct(request: Request):
    """直接生成视频 - 简化版本，不依赖Coze Bot"""
    # Validate API key
    if not validate_api_key(request):
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API key")

    try:
        # 获取参数
        data = await request.json() if request.headers.get('content-type') == 'application/json' else {}
        material_param = data.get('material', 'auto')

        logger.info(f"[Request] material_param: {material_param}")

        # 产品轮播
        PRODUCTS = ["PLGA", "PTLA", "PLCL", "PCL", "PTMC", "PGA", "PDO", "PLA"]

        if material_param == 'auto':
            import hashlib
            date_str = datetime.now().strftime("%Y-%m-%d")
            hash_val = int(hashlib.md5(date_str.encode()).hexdigest(), 16)
            product_index = hash_val % len(PRODUCTS)
            material = PRODUCTS[product_index]
            logger.info(f"[Rotation] Using hash-based rotation for date {date_str}")
        else:
            material = material_param if material_param in PRODUCTS else "PGA"
            logger.info(f"[Manual] Using manual material: {material}")

        logger.info(f"[Material] Selected: {material}")

        # 获取产品信息
        product_data = PRODUCT_INFO.get(material, PRODUCT_INFO["PGA"])
        product_name = product_data["name"]
        feature = product_data["feature"]

        # 获取视频描述
        video_description = PRODUCT_DESCRIPTIONS.get(material, PRODUCT_DESCRIPTIONS["PGA"])
        logger.info(f"[Description] Using preset description (length: {len(video_description)})")

        # 生成视频
        logger.info(f"[Video Generation] Starting for {material}...")
        logger.info(f"[Video Generation] Model: doubao-seedance-1-5-pro-251215")
        logger.info(f"[Video Generation] Resolution: 720p, 16:9")
        logger.info(f"[Video Generation] Duration: 5 seconds")

        try:
            ctx = new_context(method="video.generate")
            client = VideoGenerationClient(ctx=ctx)

            generated_url, response, _ = client.video_generation(
                content_items=[
                    TextContent(text=video_description)
                ],
                model="doubao-seedance-1-5-pro-251215",
                resolution="720p",
                ratio="16:9",
                duration=5,
                watermark=False,
                max_wait_time=600,  # 10分钟超时
                generate_audio=True
            )

            if generated_url:
                logger.info(f"[Video Generation] SUCCESS! Video URL: {generated_url[:100]}...")
                video_url = generated_url
            else:
                logger.error(f"[Video Generation] FAILED - no URL returned")
                logger.error(f"[Video Generation] Response: {response}")
                raise Exception("Video generation returned no URL")

        except APIError as e:
            logger.error(f"[Video Generation] APIError: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"[Video Generation] Exception: {str(e)}")
            import traceback
            logger.error(f"[Video Generation] Traceback: {traceback.format_exc()}")
            raise

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
            }
        }

        logger.info(f"[Response] Returning video URL for {material}")

        return {
            "success": True,
            "data": [result_data],
            "execution_time": datetime.now().isoformat(),
            "video_generation": "direct_mode",
            "note": "Direct video generation without Coze Bot"
        }

    except Exception as e:
        logger.error(f"[Error] Failed: {str(e)}")
        import traceback
        logger.error(f"[Error] Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")

# Vercel entry point
app_handler = app
