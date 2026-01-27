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
from ann_index import rebuild_index
from database import get_all_nodes, get_all_edges
from graph_cache import rebuild_graph_cache


def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    CORS(app)
    
    # Initialize database
    init_database()
    
    # Build ANN index for fast search
    nodes = get_all_nodes()
    vector_count = rebuild_index(nodes)
    print(f"📊 Built ANN index with {vector_count} vectors")
    
    # Build graph cache for fast edge traversal
    edges = get_all_edges()
    edge_count = rebuild_graph_cache(edges)
    print(f"🔗 Built graph cache with {edge_count} edges")
    
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
    mcp_endpoint = os.getenv("MCP_ENDPOINT", "/sse")
    
    print(f"\n🚀 Server starting on port {port}")
    print(f"   Debug mode: {debug}")
    print(f"   MCP endpoint: {mcp_endpoint}")
    print(f"   Health check: /health")
    print("=" * 60)
    
    app.run(host="0.0.0.0", port=port, debug=debug)


if __name__ == "__main__":
    main()
