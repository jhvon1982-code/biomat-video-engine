"""
Biomat_Video_Engine Pro v2.0 - With Automated Trend Analysis Node

Enhanced workflow: Trend Analysis → Pain Point Identification → Strategy Matching
→ Auto Scene Generation → Video Production → Research Brief
"""
import os
import json
from typing import Annotated
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from coze_coding_utils.runtime_ctx.context import default_headers
from storage.memory.memory_saver import get_memory_saver

# Import all tools
from tools.knowledge_search_tool import search_polymer_specs, import_knowledge_url
from tools.product_knowledge_tool import (
    get_company_info,
    get_all_products,
    get_product_detail,
    search_product_by_name,
    get_standards,
    get_video_script_template
)

# Try to import video generation tools
try:
    from tools.pro_video_generation_tool import (
        generate_pro_video,
        generate_intro_scene,
        generate_data_scene,
        generate_property_scene,
        generate_application_scene,
        generate_conclusion_scene
    )
    HAS_PRO_VIDEO = True
except ImportError:
    HAS_PRO_VIDEO = False

# Try to import jimeng tools
try:
    from tools.jimeng_video_tool import (
        generate_jimeng_video,
        generate_jimeng_video_with_image
    )
    HAS_JIMENG = True
except ImportError:
    HAS_JIMENG = False

# Try to import other tools
try:
    from tools.tiktok_publisher import (
        generate_tiktok_publishing_guide,
        save_tiktok_publishing_guide
    )
    from tools.seo_tools import generate_whatsapp_cta, get_safe_vocabulary
    from tools.trend_search_tool import search_video_trends, search_seo_trends, search_material_trends
    from tools.trend_analysis_tools import (
        analyze_tiktok_trends,
        analyze_youtube_trends,
        identify_pain_points,
        match_material_strategy,
        generate_decision_brief,
        auto_generate_video_scenes
    )
    HAS_TOOLS = True
except ImportError as e:
    print(f"Warning: Some tools could not be imported: {e}")
    HAS_TOOLS = False

LLM_CONFIG = "config/agent_llm_config.json"

# 默认保留最近 20 轮对话 (40 条消息)
MAX_MESSAGES = 40


def _windowed_messages(old, new):
    """滑动窗口: 只保留最近 MAX_MESSAGES 条消息"""
    return add_messages(old, new)[-MAX_MESSAGES:]  # type: ignore


class AgentState(MessagesState):
    messages: Annotated[list[AnyMessage], _windowed_messages]


def build_agent(ctx=None):
    """
    Build and configure the Biomat_Video_Engine Pro v2.0 Agent.

    NEW WORKFLOW with Trend Analysis Node:
    1. Trend Analysis (TikTok/YouTube) → 2. Pain Point Identification →
    3. Strategy Matching → 4. Auto Scene Generation → 5. Video Production →
    6. Research Brief Generation

    Returns:
        Configured agent instance with all tools, memory, and system prompt
    """
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    config_path = os.path.join(workspace_path, LLM_CONFIG)

    # Load configuration
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    # Get API configuration from environment
    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")

    # Initialize LLM with configuration
    llm = ChatOpenAI(
        model=cfg['config'].get("model"),
        api_key=api_key,
        base_url=base_url,
        temperature=cfg['config'].get('temperature', 0.7),
        streaming=True,
        timeout=cfg['config'].get('timeout', 600),
        extra_body={
            "thinking": {
                "type": cfg['config'].get('thinking', 'disabled')
            }
        },
        default_headers=default_headers(ctx) if ctx else {}
    )

    # Configure all tools (v2.0 with trend analysis)
    tools = [
        # NEW: Product Knowledge Tools
        get_company_info,
        get_all_products,
        get_product_detail,
        search_product_by_name,
        get_standards,
        get_video_script_template,

        # Knowledge retrieval
        search_polymer_specs,
        import_knowledge_url,
    ]

    # Add tools if available
    if HAS_TOOLS:
        tools.extend([
            # Trend Analysis Tools
            analyze_tiktok_trends,
            analyze_youtube_trends,
            identify_pain_points,
            match_material_strategy,
            generate_decision_brief,
            auto_generate_video_scenes,

            # SEO & customer service
            generate_whatsapp_cta,
            get_safe_vocabulary,

            # Trend research
            search_video_trends,
            search_seo_trends,
            search_material_trends,

            # TikTok publishing
            generate_tiktok_publishing_guide,
            save_tiktok_publishing_guide,
        ])

    if HAS_PRO_VIDEO:
        tools.extend([
            generate_pro_video,
            generate_intro_scene,
            generate_data_scene,
            generate_property_scene,
            generate_application_scene,
            generate_conclusion_scene,
        ])

    if HAS_JIMENG:
        tools.extend([
            generate_jimeng_video,
            generate_jimeng_video_with_image,
        ])

    # Create and return agent with memory support
    return create_agent(
        model=llm,
        system_prompt=cfg.get("sp"),
        tools=tools,
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )
