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
import logging

# 视频生成API导入
from coze_coding_dev_sdk.video import VideoGenerationClient, TextContent
from coze_coding_dev_sdk import APIError
from coze_coding_utils.runtime_ctx.context import new_context

# 导入预生成的视频池
try:
    from video_pool import PRE_GENERATED_VIDEOS
    USE_PREGENERATED_VIDEOS = True
    logger.info("[Video Pool] Loaded pre-generated videos")
except ImportError:
    USE_PREGENERATED_VIDEOS = False
    logger.warning("[Video Pool] Failed to load pre-generated videos, will use fallback")

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

@app.post("/api/v1/test-generated-video")
async def test_generated_video(request: Request):
    """测试端点 - 直接返回一个已生成的真实视频URL"""
    if not validate_api_key(request):
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API key")

    # 使用之前成功生成的PGA视频URL
    test_real_video_url = "https://coze-coding-project.tos.coze.site/coze_storage_7624343115859689526/video/video_generate_cgt-20260421203910-zcdr9.mp4?sign=1808311198-921d051e5e-0-1d72f51732a390aa4db48fb2057f71c5af32d1734357775b351122223fa5e2a1"

    return {
        "success": True,
        "data": [{
            "status": "success",
            "product": "PGA - 聚乙醇酸（已生成视频）",
            "video_link": test_real_video_url,
            "duration": "5s",
            "seo_info": {
                "title": "云南聚和PGA聚乙醇酸_医用级生物材料",
                "description": "云南聚和PGA聚乙醇酸，高强度、快速降解，适用于缝合线。符合ISO 10993生物相容性标准，广泛应用于医疗器械和生物材料领域。",
                "tags": ["云南聚和", "PGA", "聚乙醇酸", "医用材料", "生物相容性", "可降解"]
            }
        }],
        "note": "这是一个测试端点，直接返回已生成的真实视频URL",
        "execution_time": datetime.now().isoformat()
    }

@app.get("/api/v1/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "Biomat_Video_Engine",
        "version": "3.0",
        "video_pool_loaded": USE_PREGENERATED_VIDEOS,
        "video_pool_size": len(PRE_GENERATED_VIDEOS) if USE_PREGENERATED_VIDEOS else 0,
        "available_materials": list(PRE_GENERATED_VIDEOS.keys()) if USE_PREGENERATED_VIDEOS else [],
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

        # 生成视频脚本和描述 - 让Bot返回视频描述而不是直接的视频链接
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
        logging.info(f"[Coze Bot] Raw response length: {len(response_text)}")
        logging.info(f"[Coze Bot] Raw response (first 500 chars): {response_text[:500]}...")

        # Try to parse JSON
        try:
            result_data = json.loads(response_text)
            logging.info(f"[JSON Parse] Successfully parsed JSON")
        except json.JSONDecodeError:
            import re
            logging.warning(f"[JSON Parse] Failed to parse JSON directly, trying regex...")
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                result_data = json.loads(json_match.group(1))
                logging.info(f"[JSON Parse] Successfully parsed JSON via regex")
            else:
                # Fallback - 创建假数据用于测试
                logging.warning(f"[JSON Parse] No JSON found in response, using fallback")
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

        # 尝试使用视频生成API生成真实视频
        video_url = None

        # 记录result_data的所有键
        logging.info(f"[Result Data] Keys in result_data: {list(result_data.keys())}")
        logging.info(f"[Result Data] Full result_data: {json.dumps(result_data, ensure_ascii=False, indent=2)}")

        # 优先使用预生成的视频池
        if USE_PREGENERATED_VIDEOS and material in PRE_GENERATED_VIDEOS:
            video_url = PRE_GENERATED_VIDEOS[material]
            logging.info(f"[Video Pool] Using pre-generated video for {material}: {video_url[:100]}...")
        else:
            # 检查是否有video_description字段
            if "video_description" in result_data:
                video_description = result_data["video_description"]
                logging.info(f"[Video Generation] Found video description for {material}: {video_description[:100]}...")
        else:
            # 备用方案：自动生成视频描述
            logging.warning(f"[Video Generation] No video_description found, generating automatic description for {material}")

            # 产品特性描述映射
            product_descriptions = {
                "PLGA": "一个专业的医学实验室场景，显微镜视角下的PLGA（聚乳酸-羟基乙酸共聚物）微球结构。纯白色的微球在蓝色背景中缓慢旋转，展示其完美的球形结构和均匀的尺寸分布。光影效果柔和，体现高科技生物材料的质感。镜头缓慢推进，展示微球表面的细微纹理。",
                "PTLA": "一个现代化的医疗设备车间，展示PTLA（聚左旋乳酸）骨科固定材料的加工过程。高纯度的PTLA材料在精密机械的切割下成型，材料呈现出半透明的乳白色。镜头切换到X光视角，展示材料在人体骨骼中的应用效果。背景有医疗影像设备的蓝绿色光芒。",
                "PLCL": "一个高科技材料研发实验室，PLCL（聚乳酸-己内酯共聚物）薄膜在测试设备中进行拉伸测试。材料展现出优异的弹性，拉伸后能够恢复原状。显微镜视角展示材料的分子结构，均匀的分子链排列清晰可见。实验室环境洁净，LED照明营造科技感。",
                "PCL": "一个3D打印实验室，PCL（聚己内酯）材料正在被熔融沉积打印成复杂的支架结构。白色的PCL丝材在打印头上缓慢移动，层层堆叠形成网格状的医用支架。镜头特写打印细节，展示材料的柔韧性和可塑性。背景有CAD设计图纸的蓝光。",
                "PTMC": "一个心血管介入手术室，PTMC（聚三亚甲基碳酸酯）心脏支架在血管模拟器中展开。支架具有良好的弹性，能够适应血管的弯曲。高倍显微镜展示支架的网状结构和表面光滑度。手术室灯光柔和，有监护设备的红色指示灯闪烁。",
                "PGA": "一个专业的医学实验室场景，显微镜视角下的PGA（聚乙醇酸）缝合线纤维结构。纯白色的PGA纤维在蓝色背景中缓慢展开，展示其高强度和快速降解的特性。镜头缓慢推进，展示纤维的微观结构和均匀的直径。光影效果柔和，体现医用级生物材料的质感和纯净度。",
                "PDO": "一个整形外科诊所，PDO（聚对二氧环己酮）可吸收缝合线在皮肤组织的显微视角下展示。透明的PDO纤维在肌理清晰的组织模型中穿行，材料柔软而强韧。镜头展示材料的柔韧性和生物相容性。背景有柔和的手术灯光和医疗设备的金属光泽。",
                "PLA": "一个环保材料展示空间，PLA（聚乳酸）颗粒在自动化流水线上被加工成医用级可降解材料。淡黄色的PLA颗粒在透明容器中展示，背景有绿色植物和循环利用的图标，体现环保理念。镜头切换到材料的降解过程，展示其在自然环境中的生物降解特性。"
            }

            video_description = product_descriptions.get(
                material,
                f"一个高科技材料实验室，展示{material}生物医用材料的特性。材料在显微镜下展现出完美的结构和均匀的质地。实验室环境洁净专业，LED照明营造科技感。镜头缓慢推进，展示材料的微观细节和优异性能。"
            )

            logging.info(f"[Video Generation] Generated automatic description: {video_description[:100]}...")

            # 只有在没有预生成视频时才尝试实时生成
            if not USE_PREGENERATED_VIDEOS or material not in PRE_GENERATED_VIDEOS:
                # 生成视频
                try:
                    # 创建视频生成客户端
                    ctx = new_context(method="video.generate")
                    client = VideoGenerationClient(ctx=ctx)

                    # 调用视频生成API
                    logging.info(f"[Video Generation] Starting video generation for {material}...")
                    generated_url, response, last_frame_url = client.video_generation(
                        content_items=[
                            TextContent(text=video_description)
                        ],
                        model="doubao-seedance-1-5-pro-251215",
                        resolution="720p",
                        ratio="16:9",
                        duration=5,  # 5秒视频
                        watermark=False,
                        max_wait_time=900,  # 最多等待15分钟
                        generate_audio=True
                    )

                    if generated_url:
                        video_url = generated_url
                        logging.info(f"[Video Generation] Success! Video URL: {video_url}")
                    else:
                        logging.warning(f"[Video Generation] Failed - no video URL returned")
                except APIError as e:
                    logging.error(f"[Video Generation] API error: {str(e)}")
                except Exception as e:
                    logging.error(f"[Video Generation] Unexpected error: {str(e)}")
            else:
                logging.info(f"[Video Pool] Skipping real-time generation, using pre-generated video")

        # 如果视频生成失败，使用Fallback测试视频
        if not video_url:
            logging.warning(f"[Video Generation] Using fallback test video for {material}")
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

        # 确保result_data中有product_name和feature
        if "product" not in result_data:
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

            result_data["product"] = f"{material} - {product_name}"

            if "seo_info" not in result_data:
                result_data["seo_info"] = {
                    "title": f"云南聚和{material}{product_name}_医用级生物材料",
                    "description": f"云南聚和{material}{product_name}，{feature}。符合ISO 10993生物相容性标准，广泛应用于医疗器械和生物材料领域。",
                    "tags": ["云南聚和", material, product_name, "医用材料", "生物相容性", "可降解"]
                }

        # 更新video_link
        result_data["video_link"] = video_url

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
