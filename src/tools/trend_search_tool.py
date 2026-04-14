"""
Web search tool for retrieving latest video creation trends and popular tags.
"""
from langchain.tools import tool
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context


def _search_with_sdk(query: str, count: int = 10) -> str:
    """
    Common search logic using SearchClient.

    Args:
        query: Search query text
        count: Number of results to return

    Returns:
        Formatted search results as string
    """
    ctx = new_context(method="search_trends")
    client = SearchClient(ctx=ctx)

    try:
        response = client.web_search_with_summary(query=query, count=count)

        # Build formatted output
        result_parts = []

        # Add AI summary if available
        if response.summary:
            result_parts.append(f"📊 AI Summary:\n{response.summary}\n")

        # Add search results
        if response.web_items:
            result_parts.append(f"🔍 Found {len(response.web_items)} results:\n")
            for idx, item in enumerate(response.web_items, 1):
                result_parts.append(
                    f"{idx}. {item.title}\n"
                    f"   Source: {item.site_name}\n"
                    f"   URL: {item.url}\n"
                    f"   Snippet: {item.snippet[:200]}...\n"
                )
        else:
            result_parts.append("No search results found.")

        return "\n".join(result_parts)
    except Exception as e:
        return f"Search failed: {str(e)}"


@tool
def search_video_trends(query: str) -> str:
    """
    Search for latest video creation trends, AI video generation techniques, and visual effects.

    Use this tool when you need to:
    - Get inspiration for video concepts
    - Understand current visual trends (cyberpunk, lab aesthetics, etc.)
    - Find popular AI video generation prompts
    - Research Jimeng/PixVerse capabilities
    - Discover effective visual storytelling techniques

    Args:
        query: Search query about video trends, visual styles, or creation techniques

    Returns:
        Formatted search results with AI summary and relevant links
    """
    return _search_with_sdk(query, count=8)


@tool
def search_seo_trends(platform: str = "TikTok") -> str:
    """
    Search for latest SEO trends and popular tags for video platforms.

    Use this tool when you need to:
    - Get trending hashtags for TikTok/YouTube
    - Understand platform algorithm preferences
    - Find effective SEO strategies for B2B content
    - Discover safe keyword alternatives to medical terms

    Args:
        platform: Target platform (TikTok, YouTube, Instagram, etc.)

    Returns:
        Formatted search results with trending tags and SEO tips
    """
    query = f"{platform} trending tags 2024 SEO optimization short videos"
    return _search_with_sdk(query, count=10)


@tool
def search_material_trends(material_name: str) -> str:
    """
    Search for latest applications and market trends for specific biodegradable polymers.

    Use this tool when you need to:
    - Find cutting-edge applications for PLLA, PCL, PLGA, PTMC, etc.
    - Get market insights and industry trends
    - Discover research breakthroughs
    - Find inspiration for material demonstration experiments

    Args:
        material_name: Name of the material (e.g., "PLLA", "PCL", "PLGA")

    Returns:
        Formatted search results with material applications and trends
    """
    query = f"{material_name} biodegradable polymer applications 2024 research trends"
    return _search_with_sdk(query, count=8)
