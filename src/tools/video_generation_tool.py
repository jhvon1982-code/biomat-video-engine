"""
Video generation tool for creating 8K anime-style material science videos.
"""
from langchain.tools import tool
from coze_coding_utils.runtime_ctx.context import new_context

# Try to import coze_coding_dev_sdk
try:
    from coze_coding_dev_sdk.video import VideoGenerationClient, TextContent
    HAS_SDK = True
except ImportError:
    HAS_SDK = False
    print("Warning: coze_coding_dev_sdk not available. Video generation tools will be disabled.")


@tool
def generate_biomat_video(
    prompt: str,
    duration: int = 5,
    resolution: str = "720p",
    ratio: str = "16:9",
    style_preset: str = "Anime style, cyber lab, pearl-white material texture, 8K"
) -> str:
    """
    Generate an 8K anime-style biopolymer material science video.

    This tool creates high-quality videos with the following default visual style:
    - Anime style: Love, Death & Robots aesthetic
    - Cyber lab: Futuristic laboratory setting with neon accents
    - Pearl-white material texture: Translucent biodegradable polymer appearance
    - 8K: Ultra-high definition quality

    Supported materials: PCL, PLLA, PLGA, PTMC, AMPPD, APS-5, etc.

    Args:
        prompt: Text description of the video content (e.g., "PCL 3D printed scaffold structure")
        duration: Video duration in seconds (4-12 recommended, default: 5)
        resolution: Video resolution ("480p", "720p", "1080p", default: "720p")
        ratio: Aspect ratio ("16:9", "9:16", "1:1", default: "16:9")
        style_preset: Visual style preset (default: Anime style, cyber lab, pearl-white material texture, 8K)

    Returns:
        Generated video URL (valid for 24 hours)
    """
    if not HAS_SDK:
        return "❌ Error: coze_coding_dev_sdk is not available. Video generation is disabled."

    try:
        ctx = new_context(method="video.generate")

        client = VideoGenerationClient(ctx=ctx)

        # Combine style preset with user prompt
        full_prompt = f"{style_preset}, {prompt}"

        # Generate video
        video_url, response, last_frame_url = client.video_generation(
            content_items=[
                TextContent(text=full_prompt)
            ],
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
            result += f"\n⚠️ Note: Video URL is valid for 24 hours. Please download if needed."
            return result
        else:
            return f"❌ Video generation failed. Response: {response}"

    except Exception as e:
        return f"❌ Video generation error: {str(e)}"


@tool
def generate_video_with_prompt(
    prompt: str,
    visual_keywords: str = "biopolymer, scaffold, crystalline microstructure, translucent",
    duration: int = 5
) -> str:
    """
    Generate a biopolymer material video with enhanced visual keywords.

    This tool automatically appends relevant visual keywords to ensure
    the generated video has appropriate material science aesthetics.

    Args:
        prompt: Core video description (e.g., "PCL scaffold supporting tissue growth")
        visual_keywords: Comma-separated visual keywords (default: biopolymer, scaffold, crystalline)
        duration: Video duration in seconds (default: 5)

    Returns:
        Generated video URL with details
    """
    # Build enhanced prompt
    enhanced_prompt = f"{visual_keywords}, {prompt}"
    enhanced_prompt += ", macro photography, depth of field, smooth animation, scientific visualization"

    return generate_biomat_video(
        prompt=enhanced_prompt,
        duration=duration,
        resolution="720p",
        ratio="16:9"
    )
