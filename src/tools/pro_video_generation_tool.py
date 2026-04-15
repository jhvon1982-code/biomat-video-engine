"""
Professional video generation tool matching Jimeng seedance 2.0 standards.
"""
from langchain.tools import tool
from coze_coding_utils.runtime_ctx.context import new_context

# Try to import coze_coding_dev_sdk
try:
    from coze_coding_dev_sdk.video import VideoGenerationClient, TextContent
    HAS_SDK = True
except ImportError:
    HAS_SDK = False
    print("Warning: coze_coding_dev_sdk not available. Professional video tools will be disabled.")


def _generate_video_with_params(prompt: str, duration: int, resolution: str, ratio: str) -> str:
    """
    Common video generation logic.

    Args:
        prompt: Text description of the video content
        duration: Video duration in seconds
        resolution: Video resolution (720p, 1080p)
        ratio: Aspect ratio (16:9, 9:16, 1:1)

    Returns:
        Generated video URL with details
    """
    if not HAS_SDK:
        return "❌ Error: coze_coding_dev_sdk is not available. Video generation is disabled."

    try:
        ctx = new_context(method="video.generate.pro")
        client = VideoGenerationClient(ctx=ctx)

        video_url, response, last_frame_url = client.video_generation(
            content_items=[TextContent(text=prompt)],
            model="doubao-seedance-1-5-pro-251215",
            resolution=resolution,
            ratio=ratio,
            duration=duration,
            watermark=False,
            return_last_frame=True,
            max_wait_time=900
        )

        if video_url:
            result = f"✅ Video generated successfully!\n\n"
            result += f"**Video URL**: {video_url}\n"
            result += f"**Last Frame URL**: {last_frame_url}\n"
            result += f"**Duration**: {response.get('duration', 'N/A')}s\n"
            result += f"**Resolution**: {response.get('resolution', 'N/A')}\n"
            result += f"**Ratio**: {response.get('ratio', 'N/A')}\n"
            result += f"**Frame Rate**: ~24fps\n"
            result += f"\n⚠️ Note: Video URL is valid for 24 hours. Please download if needed."
            return result
        else:
            return f"❌ Video generation failed. Response: {response}"

    except Exception as e:
        return f"❌ Video generation error: {str(e)}"


def _build_jimeng_prompt(
    material_name: str,
    content_type: str,
    data_value: str = ""
) -> str:
    """
    Build Jimeng-style prompt for different scene types.

    Args:
        material_name: Name of the material
        content_type: Type of content (intro/data/property/application/comparison/conclusion)
        data_value: Numeric value to display

    Returns:
        Formatted prompt string
    """
    prompt_templates = {
        "intro": (
            "{material} Polycaprolactone biodegradable polymer introduction,\n"
            "clean white background with subtle blue gradient,\n"
            "large bold text \"{material}\" in center,\n"
            "translucent polymer particles floating smoothly,\n"
            "professional medical illustration style,\n"
            "clean layout, high contrast text, smooth entrance animation"
        ),
        "data": (
            "{material} key technical data,\n"
            "clean medical blue background,\n"
            "large number \"{data}\" in bold text,\n"
            "subtitle text with technical label,\n"
            "data visualization graphics,\n"
            "clean professional layout, data animation"
        ),
        "property": (
            "{material} thermal property visualization,\n"
            "clean medical illustration style,\n"
            "temperature meter graphic,\n"
            "large data value \"{data}\",\n"
            "subtitle \"Melting Point\",\n"
            "smooth property transition animation,\n"
            "blue and white color scheme"
        ),
        "application": (
            "{material} 3D printed scaffold application,\n"
            "3D anatomical model visualization,\n"
            "clean professional medical illustration,\n"
            "smooth camera rotation, depth effect,\n"
            "cells growing in scaffold pores,\n"
            "professional clean style"
        ),
        "comparison": (
            "{material} biodegradation comparison,\n"
            "before and after split screen,\n"
            "clean data comparison graphics,\n"
            "large percentage improvement,\n"
            "professional medical style,\n"
            "smooth comparison transition"
        ),
        "conclusion": (
            "{material} key advantages summary,\n"
            "text \"Biodegradable in {data} months\",\n"
            "text \"High Strength Tissue Support\",\n"
            "text \"WhatsApp: +1 (213) 275-7332\",\n"
            "clean professional layout,\n"
            "gradient background with medical blue,\n"
            "professional conclusion animation"
        )
    }

    template = prompt_templates.get(content_type, prompt_templates["intro"])
    prompt = template.format(material=material_name, data=data_value)
    prompt += "\n720p, 24fps, professional medical animation, clean layout, data-driven"

    return prompt


@tool
def generate_pro_video(
    prompt: str,
    duration: int = 2,
    resolution: str = "720p",
    ratio: str = "16:9"
) -> str:
    """
    Generate professional biopolymer video matching Jimeng seedance 2.0 standards.

    Args:
        prompt: Text description of the video content (must be detailed and specific)
        duration: Video duration in seconds (2s for single scene, 4s for final scene)
        resolution: Video resolution (default: "720p" for Jimeng compatibility)
        ratio: Aspect ratio (default: "16:9" for horizontal video)

    Returns:
        Generated video URL with details
    """
    return _generate_video_with_params(prompt, duration, resolution, ratio)


@tool
def generate_intro_scene(material_name: str) -> str:
    """
    Generate scene 1: Material introduction (0-1 second).

    Args:
        material_name: Name of the material (e.g., "PCL", "PLLA")

    Returns:
        Generated video URL
    """
    prompt = _build_jimeng_prompt(material_name, "intro")
    return _generate_video_with_params(prompt, duration=1, resolution="720p", ratio="16:9")


@tool
def generate_data_scene(material_name: str, data_value: str) -> str:
    """
    Generate scene 2: Core data display (1-2 seconds).

    Args:
        material_name: Name of the material
        data_value: Numeric value to display (e.g., "60°C", "24-36 months")

    Returns:
        Generated video URL
    """
    prompt = _build_jimeng_prompt(material_name, "data", data_value)
    return _generate_video_with_params(prompt, duration=1, resolution="720p", ratio="16:9")


@tool
def generate_property_scene(material_name: str, property_value: str) -> str:
    """
    Generate scene 3-5: Physical property visualization (2-6 seconds).

    Args:
        material_name: Name of the material
        property_value: Property value (e.g., "60°C")

    Returns:
        Generated video URL
    """
    prompt = _build_jimeng_prompt(material_name, "property", property_value)
    return _generate_video_with_params(prompt, duration=2, resolution="720p", ratio="16:9")


@tool
def generate_application_scene(material_name: str) -> str:
    """
    Generate scene 6-7: Application scenario 3D visualization (6-11 seconds).

    Args:
        material_name: Name of the material

    Returns:
        Generated video URL
    """
    prompt = _build_jimeng_prompt(material_name, "application")
    return _generate_video_with_params(prompt, duration=3, resolution="720p", ratio="16:9")


@tool
def generate_conclusion_scene(material_name: str, degrad_period: str) -> str:
    """
    Generate scene 8: Summary + CTA (11-15 seconds).

    Args:
        material_name: Name of the material
        degrad_period: Degradation period (e.g., "24-36 months")

    Returns:
        Generated video URL
    """
    prompt = _build_jimeng_prompt(material_name, "conclusion", degrad_period)
    return _generate_video_with_params(prompt, duration=4, resolution="720p", ratio="16:9")
