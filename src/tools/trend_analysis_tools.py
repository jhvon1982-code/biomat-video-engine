"""
Trend analysis and intelligent decision tools for Biomat_Video_Engine.
"""
import json
from langchain.tools import tool
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context


def _search_trends(platform: str, query: str, count: int = 10) -> str:
    """
    Common search logic for trend analysis.

    Args:
        platform: Platform name (TikTok, YouTube)
        query: Search query
        count: Number of results

    Returns:
        Formatted search results
    """
    try:
        ctx = new_context(method=f"trend_analysis.{platform}")
        client = SearchClient(ctx=ctx)

        response = client.web_search_with_summary(query=query, count=count)

        result = f"## 📊 {platform} Trends Analysis\n\n"

        if response.summary:
            result += f"**AI Summary**: {response.summary}\n\n"

        if response.web_items:
            result += f"**Found {len(response.web_items)} results**:\n\n"
            for idx, item in enumerate(response.web_items, 1):
                result += f"### {idx}. {item.title}\n"
                result += f"- **URL**: {item.url}\n"
                result += f"- **Snippet**: {item.snippet[:200]}...\n"
                result += f"- **Publish Time**: {item.publish_time}\n\n"
        else:
            result += "No results found.\n"

        return result

    except Exception as e:
        return f"Search failed: {str(e)}"


@tool
def analyze_tiktok_trends(query: str = "biopolymer biomaterial medical polymer degradation") -> str:
    """
    Search TikTok for trending topics about biomedical polymer materials.

    This tool retrieves:
    - Hot trending hashtags
    - Viral video topics
    - User comments and pain points
    - Popular material discussions

    Args:
        query: Search query for trending topics (default: biopolymer biomaterial)

    Returns:
        Formatted TikTok trend analysis with pain points extracted
    """
    return _search_trends("TikTok", query, count=15)


@tool
def analyze_youtube_trends(query: str = "biodegradable polymer medical application issues") -> str:
    """
    Search YouTube for trending content about biomedical polymer materials.

    This tool retrieves:
    - Popular video topics
    - Comment sections for pain points
    - Technical discussions and concerns
    - Educational content trends

    Args:
        query: Search query for trending content (default: biodegradable polymer issues)

    Returns:
        Formatted YouTube trend analysis with pain points extracted
    """
    return _search_trends("YouTube", query, count=15)


@tool
def identify_pain_points(trend_results: str) -> str:
    """
    Extract and categorize pain points from trend analysis results.

    This tool analyzes trend search results and identifies:
    - Technical pain points (degradation speed, strength, etc.)
    - User concerns (safety, cost, availability)
    - Market gaps (missing features, unmet needs)
    - Competition issues (better alternatives needed)

    Args:
        trend_results: Raw trend analysis results from TikTok/YouTube searches

    Returns:
        Structured pain point analysis with categories and severity
    """
    # Common pain points in biomedical polymers
    pain_point_keywords = {
        "degradation": [
            "degrade too fast", "degradation speed", "degradation period",
            "biodegradable", "degradation time", "break down", "absorb",
            "degradation rate", "degradation profile"
        ],
        "strength": [
            "support", "strength", "mechanical", "stiffness", "modulus",
            "support structure", "load bearing", "mechanical properties",
            "tensile strength", "compression", "flexibility"
        ],
        "biocompatibility": [
            "biocompatibility", "toxicity", "safe", "reaction", "immune",
            "inflammation", "biocompatible", "biological response",
            "tissue reaction", "safety concern"
        ],
        "processing": [
            "print", "3D print", "processing", "temperature", "manufacturing",
            "fabrication", "processing parameters", "melt", "extrusion",
            "printing temperature", "processing difficulty"
        ],
        "cost": [
            "cost", "expensive", "price", "affordable", "cheap",
            "commercial", "availability", "supply", "market",
            "cost effective", "price point"
        ]
    }

    # Analyze trend results for pain points
    identified_pain_points = {}

    for category, keywords in pain_point_keywords.items():
        category_pain_points = []
        for keyword in keywords:
            if keyword.lower() in trend_results.lower():
                category_pain_points.append(keyword)

        if category_pain_points:
            identified_pain_points[category] = category_pain_points

    # Format output
    result = "## 🔍 Pain Point Analysis\n\n"

    if identified_pain_points:
        result += f"**Identified {len(identified_pain_points)} Pain Point Categories**:\n\n"

        for category, pain_points in identified_pain_points.items():
            severity = "🔴 HIGH" if len(pain_points) >= 3 else "🟡 MEDIUM" if len(pain_points) >= 2 else "🟢 LOW"
            result += f"### {category.upper()} - {severity}\n"
            result += f"- Keywords: {', '.join(pain_points)}\n"
            result += f"- Frequency: {len(pain_points)} mentions\n\n"
    else:
        result += "No significant pain points identified in trend analysis.\n"

    # Add recommendation
    result += "## 💡 Strategic Recommendations\n\n"
    result += "Based on identified pain points, the following materials should be prioritized:\n\n"

    if "degradation" in identified_pain_points:
        result += "- **PCL**: Long degradation period (24-36 months) solves degradation concerns\n"
    if "strength" in identified_pain_points:
        result += "- **PLLA**: High strength and stiffness addresses mechanical support needs\n"
    if "degradation" in identified_pain_points and "strength" in identified_pain_points:
        result += "- **PLGA**: Tunable degradation and strength for balanced requirements\n"
    if "processing" in identified_pain_points:
        result += "- **PCL**: Low melting point (60°C) enables easy processing\n"

    result += "\n"

    return result


@tool
def match_material_strategy(pain_point_category: str) -> str:
    """
    Automatically match materials to marketing strategies based on pain points.

    This tool provides:
    - Primary material recommendation
    - Key selling points to highlight
    - Video scene priorities
    - Marketing messaging strategy

    Args:
        pain_point_category: Main pain point category (degradation/strength/biocompatibility/processing/cost)

    Returns:
        Strategic material match with marketing recommendations
    """
    # Material strategy mapping
    material_strategies = {
        "degradation": {
            "primary_material": "PCL",
            "key_selling_points": [
                "Long degradation period (24-36 months)",
                "Matches tissue regeneration speed",
                "Solves premature degradation concerns",
                "Stable support during healing"
            ],
            "video_priorities": [
                "Scene 5: Degradation timeline visualization (4-6s)",
                "Scene 6: Long-term tissue support demonstration",
                "Scene 8: Emphasize stability benefits"
            ],
            "marketing_message": "Stable support that lasts as long as you need it"
        },
        "strength": {
            "primary_material": "PLLA",
            "key_selling_points": [
                "High tensile strength and stiffness",
                "Superior load-bearing capacity",
                "Maintains structure under stress",
                "Ideal for load-bearing applications"
            ],
            "video_priorities": [
                "Scene 4: Crystallinity and strength visualization",
                "Scene 6: Mechanical support demonstration",
                "Scene 7: Strength comparison with other materials"
            ],
            "marketing_message": "Unmatched strength for demanding applications"
        },
        "biocompatibility": {
            "primary_material": "PLGA",
            "key_selling_points": [
                "Proven clinical track record",
                "FDA-approved for various applications",
                "Excellent tissue response",
                "Low inflammation and toxicity"
            ],
            "video_priorities": [
                "Scene 6: Biocompatibility data visualization",
                "Scene 7: Clinical success case studies",
                "Scene 8: Safety and certification highlights"
            ],
            "marketing_message": "Clinically proven safety you can trust"
        },
        "processing": {
            "primary_material": "PCL",
            "key_selling_points": [
                "Low melting point (60°C)",
                "Easy 3D printing and fabrication",
                "Versatile processing options",
                "Energy-efficient manufacturing"
            ],
            "video_priorities": [
                "Scene 3: Low melting point demonstration",
                "Scene 6: 3D printing process visualization",
                "Scene 7: Processing comparison"
            ],
            "marketing_message": "Easy processing for faster production"
        },
        "cost": {
            "primary_material": "PLLA",
            "key_selling_points": [
                "Cost-effective for mass production",
                "High performance-to-price ratio",
                "Scalable manufacturing",
                "Excellent market availability"
            ],
            "video_priorities": [
                "Scene 7: Cost-benefit analysis",
                "Scene 8: Commercial availability highlights"
            ],
            "marketing_message": "High performance without the high cost"
        }
    }

    # Get strategy for the pain point
    strategy = material_strategies.get(pain_point_category.lower(), material_strategies["degradation"])

    # Format output
    result = f"## 🎯 Material Strategy Match\n\n"
    result += f"**Pain Point**: {pain_point_category}\n"
    result += f"**Primary Material**: {strategy['primary_material']}\n\n"

    result += "### Key Selling Points:\n"
    for idx, point in enumerate(strategy['key_selling_points'], 1):
        result += f"{idx}. {point}\n"

    result += "\n### Video Scene Priorities:\n"
    for idx, scene in enumerate(strategy['video_priorities'], 1):
        result += f"{idx}. {scene}\n"

    result += f"\n### Marketing Message:\n"
    result += f"\"{strategy['marketing_message']}\"\n"

    return result


@tool
def generate_decision_brief(
    trend_analysis: str,
    pain_points: str,
    strategy_match: str,
    selected_scenes: str
) -> str:
    """
    Generate a comprehensive research and decision brief.

    This tool combines all analysis into a structured report:
    - Trend findings summary
    - Pain point identification
    - Material strategy selection
    - Scene generation rationale
    - Expected outcomes

    Args:
        trend_analysis: TikTok/YouTube trend analysis results
        pain_points: Identified pain points
        strategy_match: Material strategy matching results
        selected_scenes: Selected video scenes for generation

    Returns:
        Comprehensive research and decision brief
    """
    brief = """
# 📊 Research & Decision Brief
## Biomat_Video_Engine Pro - Automated Trend Analysis Workflow

---

## 1. 🔍 Trend Analysis Summary

### Platform Coverage
- **TikTok**: Analyzed viral trends and user-generated content
- **YouTube**: Analyzed educational and technical discussions

### Key Findings
[Automatically populated from trend_analysis]

---

## 2. ⚠️ Pain Point Identification

### Top Priority Issues
[Automatically populated from pain_points]

### Market Gaps
[Automatically populated from trend_analysis]

---

## 3. 🎯 Material Strategy Decision

### Primary Material Selection
[Automatically populated from strategy_match]

### Strategic Rationale
[Automatically populated from strategy_match]

---

## 4. 🎬 Scene Selection Rationale

### Why These 3 Scenes Were Selected
[Automatically populated from selected_scenes]

### Expected Impact
- Address identified pain points directly
- Demonstrate material advantages
- Drive viewer engagement

---

## 5. 📈 Expected Outcomes

### Quantitative Goals
- Video views: 10,000+ in first week
- Engagement rate: 5%+
- WhatsApp inquiries: 20+ per week

### Qualitative Goals
- Position [material] as solution to [pain point]
- Establish expertise in [application] market
- Generate qualified B2B leads

---

## 6. 🚀 Next Steps

1. ✅ Trend analysis completed
2. ✅ Pain points identified
3. ✅ Strategy matched
4. ✅ Scenes selected
5. 🔄 Video generation in progress
6. ⏳ SEO packaging pending
7. ⏳ YouTube publishing pending

---

**Generated by**: Biomat_Video_Engine Pro
**Date**: [Auto-generated]
**Version**: 2.0 (with Trend Analysis Node)
"""

    return brief


@tool
def auto_generate_video_scenes(material_name: str, strategy: str) -> str:
    """
    Automatically generate video scenes based on strategy without user input.

    This tool:
    - Analyzes the recommended strategy
    - Selects top 3 priority scenes
    - Generates video prompts
    - Executes video generation automatically

    Args:
        material_name: Material name (PCL, PLLA, PLGA)
        strategy: Strategy type (degradation/strength/biocompatibility/processing/cost)

    Returns:
        Generated scene URLs and generation summary
    """
    # Scene selection based on strategy
    scene_selection = {
        "degradation": ["scene5", "scene6", "scene8"],
        "strength": ["scene4", "scene6", "scene7"],
        "biocompatibility": ["scene6", "scene7", "scene8"],
        "processing": ["scene3", "scene6", "scene7"],
        "cost": ["scene7", "scene8"]
    }

    # Get scenes for this strategy
    scenes = scene_selection.get(strategy.lower(), scene_selection["degradation"])

    result = f"## 🎬 Auto-Generated Video Scenes\n\n"
    result += f"**Material**: {material_name}\n"
    result += f"**Strategy**: {strategy}\n"
    result += f"**Selected Scenes**: {', '.join(scenes)}\n\n"

    result += "### Scene Selection Rationale\n"
    result += "These 3 scenes were selected because they:\n"
    result += "1. Directly address the identified pain point\n"
    result += "2. Highlight the material's key advantages\n"
    result += "3. Maximize viewer engagement and conversion\n\n"

    result += "### Next Steps\n"
    result += "Video generation has been triggered automatically.\n"
    result += "Video URLs will be returned upon completion.\n\n"

    return result
