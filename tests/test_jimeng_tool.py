"""
Test Jimeng Video Generation Tool
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from tools.jimeng_video_tool import generate_jimeng_video

# Test with a simple prompt
test_prompt = "A futuristic city with flying vehicles at sunset"

print("=" * 60)
print("Testing Jimeng Video Generation Tool")
print("=" * 60)
print(f"Prompt: {test_prompt}")
print()

try:
    result = generate_jimeng_video(
        prompt=test_prompt,
        duration=5,
        resolution="720p",
        ratio="16:9"
    )
    print("Result:")
    print(result)
    print()
    print("=" * 60)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    print()
    print("=" * 60)
