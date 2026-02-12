#!/usr/bin/env python3
"""
Neural Memory Graph Server
Flask application with MCP SSE endpoint
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys

# Add src to path (must be first to ensure volume-mounted src/ takes priority)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, '/app/src')

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
    
    # Compute graph metrics (PageRank, communities)
    from graph_metrics import get_graph_metrics
    node_ids = [n["id"] for n in nodes]
    edge_tuples = [(e["source_id"], e["target_id"], e["weight"]) for e in edges]
    get_graph_metrics().compute(edge_tuples, node_ids)
    
    # Build BM25 keyword index
    from bm25_index import get_bm25_index
    bm25_docs = [(n["id"], n.get("content", "")) for n in nodes]
    get_bm25_index().build(bm25_docs)
    
    # Register MCP endpoint
    create_mcp_endpoint(app)
    

    # ===== REST API for Graph Viewer =====
    
    @app.route("/api/graph-data", methods=["GET"])
    def graph_data():
        """Return all nodes and edges for visualization.
        Query params:
            - api_key: required for authentication
            - brief: if 'true', return truncated content (first 200 chars)
        """
        # Auth check
        api_key = request.args.get('api_key', '')
        expected_key = os.getenv('NEURAL_API_KEY', '')
        if not expected_key or api_key != expected_key:
            return jsonify({"error": "unauthorized"}), 401
        
        brief = request.args.get('brief', 'true').lower() == 'true'
        
        nodes = get_all_nodes()
        edges = get_all_edges()
        
        # Format nodes for viewer
        formatted_nodes = []
        for n in nodes:
            node = {
                "id": n["id"],
                "category": n.get("category", "general"),
                "importance": n.get("importance", "normal"),
                "timestamp": n.get("timestamp", ""),
                "emotional_tone": n.get("emotional_tone", ""),
                "emotional_intensity": n.get("emotional_intensity", 5),
            }
            if brief:
                content = n.get("content", "")
                # First line + truncate
                first_line = content.split("\n")[0][:200]
                node["preview"] = first_line
                node["full_length"] = len(content)
            else:
                node["content"] = n.get("content", "")
            formatted_nodes.append(node)
        
        # Format edges
        formatted_edges = []
        for e in edges:
            formatted_edges.append({
                "source": e["source_id"],
                "target": e["target_id"],
                "weight": e.get("weight", 0.5),
                "type": e.get("edge_type", "semantic")
            })
        
        return jsonify({
            "nodes": formatted_nodes,
            "edges": formatted_edges,
            "stats": {
                "total_nodes": len(formatted_nodes),
                "total_edges": len(formatted_edges)
            }
        })
    
    @app.route("/api/node/<int:node_id>", methods=["GET"])
    def get_node_detail(node_id):
        """Return full content for a single node"""
        api_key = request.args.get('api_key', '')
        expected_key = os.getenv('NEURAL_API_KEY', '')
        if not expected_key or api_key != expected_key:
            return jsonify({"error": "unauthorized"}), 401
        
        from database import get_node
        node = get_node(node_id)
        if not node:
            return jsonify({"error": "not found"}), 404
        return jsonify(dict(node))

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
