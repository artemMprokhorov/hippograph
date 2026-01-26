#!/usr/bin/env python3
"""
Neural Memory Graph Server
Flask application with MCP SSE endpoint
"""

from flask import Flask
from flask_cors import CORS
import os
import sys

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_database
from mcp_sse_handler import create_mcp_endpoint


def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    CORS(app)
    
    # Initialize database
    init_database()
    
    # Register MCP endpoint
    create_mcp_endpoint(app)
    
    return app


def main():
    """Run the server"""
    print("=" * 60)
    print("🧠 Neural Memory Graph - Knowledge Graph Memory System")
    print("=" * 60)
    
    app = create_app()
    
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    
    print(f"\n🚀 Server starting on port {port}")
    print(f"   Debug mode: {debug}")
    print(f"   MCP endpoint: /sse")
    print(f"   Health check: /health")
    print("=" * 60)
    
    app.run(host="0.0.0.0", port=port, debug=debug)


if __name__ == "__main__":
    main()
