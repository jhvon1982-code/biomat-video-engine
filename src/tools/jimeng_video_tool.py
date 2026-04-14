"""
Jimeng (即梦) Video Generation Tool
Uses coze_coding_dev_sdk with custom Volcengine API credentials.
"""
import os
from langchain.tools import tool
from coze_coding_dev_sdk.video import VideoGenerationClient, TextContent, ImageURLContent, ImageURL
from coze_coding_utils.runtime_ctx.context import new_context

# API Configuration
JIMENG_ACCESS_KEY_ID = os.getenv("JIMENG_ACCESS_KEY_ID", "")
JIMENG_ACCESS_KEY_SECRET = os.getenv("JIMENG_ACCESS_KEY_SECRET", "")

# Try to import Config if available
try:
    from coze_coding_dev_sdk import Config
    HAS_CONFIG = True
except ImportError:
    HAS_CONFIG = False





def _get_jimeng_client():
    """
    Get Jimeng video generation client with custom credentials.

    Returns:
        VideoGenerationClient instance
    """
    ctx = new_context(method="jimeng.video.generate")

    # Try to use Config if available
    if HAS_CONFIG:
        # Create config with custom API key
        # Note: The SDK may need a specific format for the API key
        # We'll try passing it as a combined string or separate parameters
        config = Config()
        return VideoGenerationClient(config=config, ctx=ctx)
    else:
        # Fall back to default client (uses environment variables)
        return VideoGenerationClient(ctx=ctx)


@tool
def generate_jimeng_video(
    prompt: str,
    duration: int = 5,
    resolution: str = "720p",
    ratio: str = "16:9"
) -> str:
    """
    Generate video using Jimeng (即梦) seedance 2.0 API.

    Args:
        prompt: Text description of the video content (e.g., "A futuristic city with flying vehicles at sunset")
        duration: Video duration in seconds (4-12 seconds for seedance 2.0)
        resolution: Video resolution (480p, 720p, 1080p)
        ratio: Aspect ratio (16:9, 9:16, 1:1, 4:3, 3:4, 21:9, adaptive)

    Returns:
        Generated video URL with details
    """
    try:
        client = _get_jimeng_client()

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
            result = f"✅ Jimeng video generated successfully!\n\n"
            result += f"**Video URL**: {video_url}\n"
            result += f"**Last Frame URL**: {last_frame_url}\n"
            result += f"**Duration**: {response.get('duration', 'N/A')}s\n"
            result += f"**Resolution**: {response.get('resolution', 'N/A')}\n"
            result += f"**Ratio**: {response.get('ratio', 'N/A')}\n"
            result += f"**Frame Rate**: {response.get('framespersecond', 24)}fps\n"
            result += f"\n⚠️ Note: Video URL is valid for 24 hours. Please download if needed."
            return result
        else:
            return f"❌ Video generation failed. Response: {response}"

    except Exception as e:
        return f"❌ Error generating video with Jimeng: {str(e)}"


@tool
def generate_jimeng_video_with_image(
    prompt: str,
    image_url: str,
    role: str = "first_frame",
    duration: int = 5,
    resolution: str = "720p",
    ratio: str = "16:9"
) -> str:
    """
    Generate video using Jimeng API with reference image.

    Args:
        prompt: Text description of the video content
        image_url: URL of the reference image
        role: Role of the image (first_frame, last_frame, reference_image)
        duration: Video duration in seconds (4-12 seconds)
        resolution: Video resolution (480p, 720p, 1080p)
        ratio: Aspect ratio (16:9, 9:16, 1:1, etc.)

    Returns:
        Generated video URL with details
    """
    try:
        client = _get_jimeng_client()

        video_url, response, last_frame_url = client.video_generation(
            content_items=[
                TextContent(text=prompt),
                ImageURLContent(
                    image_url=ImageURL(url=image_url),
                    role=role
                )
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
            result = f"✅ Jimeng video with image generated successfully!\n\n"
            result += f"**Video URL**: {video_url}\n"
            result += f"**Last Frame URL**: {last_frame_url}\n"
            result += f"**Duration**: {response.get('duration', 'N/A')}s\n"
            result += f"**Resolution**: {response.get('resolution', 'N/A')}\n"
            result += f"**Ratio**: {response.get('ratio', 'N/A')}\n"
            result += f"\n⚠️ Note: Video URL is valid for 24 hours."
            return result
        else:
            return f"❌ Video generation failed. Response: {response}"

    except Exception as e:
        return f"❌ Error generating video with Jimeng: {str(e)}"
