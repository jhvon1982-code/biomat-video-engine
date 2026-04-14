"""
Vercel Python Serverless Entry Point
"""
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from api.index import app as application

# Vercel uses this variable name
app = application

# Vercel serverless handler
def handler(request):
    """Vercel serverless handler"""
    return app(request.environ, lambda status, headers: None)
