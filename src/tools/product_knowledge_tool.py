"""
产品知识库工具 - 用于检索四川琢新-云南聚和的产品信息
"""
import os
import json
from langchain.tools import tool
from typing import Dict, List, Optional


PRODUCT_KNOWLEDGE_PATH = "assets/product_knowledge.json"


@tool
def get_company_info() -> str:
    """获取公司基本信息"""
    try:
        workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
        knowledge_path = os.path.join(workspace_path, PRODUCT_KNOWLEDGE_PATH)

        with open(knowledge_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        company = data.get('company', {})
        return json.dumps(company, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def get_all_products() -> str:
    """获取所有产品列表"""
    try:
        workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
        knowledge_path = os.path.join(workspace_path, PRODUCT_KNOWLEDGE_PATH)

        with open(knowledge_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        products = data.get('products', [])
        product_list = []

        for p in products:
            product_info = {
                "id": p.get('id'),
                "name": p.get('name'),
                "english_name": p.get('english_name'),
                "cas": p.get('cas'),
                "applications": p.get('applications', [])[:3]  # 前3个应用
            }
            product_list.append(product_info)

        return json.dumps(product_list, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def get_product_detail(product_id: int) -> str:
    """根据产品ID获取详细信息

    Args:
        product_id: 产品ID

    Returns:
        产品的详细信息，包括名称、CAS号、分子式、应用场景等
    """
    try:
        workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
        knowledge_path = os.path.join(workspace_path, PRODUCT_KNOWLEDGE_PATH)

        with open(knowledge_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        products = data.get('products', [])

        for p in products:
            if p.get('id') == product_id:
                return json.dumps(p, ensure_ascii=False, indent=2)

        return f"Error: Product with ID {product_id} not found"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def search_product_by_name(name: str) -> str:
    """根据产品名称（或缩写）搜索产品

    Args:
        name: 产品名称或缩写，如"PCL", "PLGA", "聚己内酯"

    Returns:
        匹配的产品信息列表
    """
    try:
        workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
        knowledge_path = os.path.join(workspace_path, PRODUCT_KNOWLEDGE_PATH)

        with open(knowledge_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        products = data.get('products', [])
        results = []

        name_lower = name.lower()

        for p in products:
            product_name = p.get('name', '').lower()
            english_name = p.get('english_name', '').lower()

            if (name_lower in product_name or
                name_lower in english_name or
                name_lower == p.get('cas', '').lower()):

                result = {
                    "id": p.get('id'),
                    "name": p.get('name'),
                    "english_name": p.get('english_name'),
                    "cas": p.get('cas'),
                    "formula": p.get('formula'),
                    "molecular_weight": p.get('molecular_weight'),
                    "applications": p.get('applications', [])[:5],
                    "features": p.get('features', [])
                }
                results.append(result)

        if results:
            return json.dumps(results, ensure_ascii=False, indent=2)
        else:
            return f"No products found matching '{name}'"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def get_standards() -> str:
    """获取产品质量标准和认证信息"""
    try:
        workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
        knowledge_path = os.path.join(workspace_path, PRODUCT_KNOWLEDGE_PATH)

        with open(knowledge_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        standards = data.get('standards', {})
        return json.dumps(standards, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def get_video_script_template() -> str:
    """获取视频脚本模板"""
    try:
        workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
        knowledge_path = os.path.join(workspace_path, PRODUCT_KNOWLEDGE_PATH)

        with open(knowledge_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        template = data.get('video_script_template', {})
        return json.dumps(template, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"
