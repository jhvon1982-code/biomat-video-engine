"""
Vercel Python Serverless Entry Point
"""
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# 尝试导入原有应用（如果依赖满足）
try:
    from api.index import app as application
    # Vercel uses this variable name
    app = application
except ImportError as e:
    print(f"Warning: Failed to import api.index: {e}")
    print("Using upload_api as fallback")
    from api.upload_api import app as application
    app = application

# Vercel serverless handler
def handler(request):
    """Vercel serverless handler"""
    return app(request.environ, lambda status, headers: None)
