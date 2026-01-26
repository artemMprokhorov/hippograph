#!/usr/bin/env python3
"""
MCP SSE Handler for Neural Memory Graph
Implements Model Context Protocol with Server-Sent Events
"""

from flask import Response, request, jsonify, stream_with_context
import json
import hashlib
import hmac
import os

from database import get_stats, get_node, delete_node as db_delete_node, update_node as db_update_node
from graph_engine import add_note_with_links, search_with_activation, get_node_graph
from stable_embeddings import get_model

# Authentication - use environment variable
API_KEY = os.getenv("NEURAL_API_KEY", "change_me_in_production")
API_KEY_HASH = hashlib.sha256(API_KEY.encode()).hexdigest()


def verify_auth(req):
    """Verify API key from URL parameter or Authorization header"""
    url_key = req.args.get("api_key")
    if url_key:
        key_hash = hashlib.sha256(url_key.encode()).hexdigest()
        return hmac.compare_digest(key_hash, API_KEY_HASH)
    
    auth_header = req.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        return hmac.compare_digest(token_hash, API_KEY_HASH)
    
    return False


def handle_mcp_request(method, params):
    """Route MCP requests to handlers"""
    try:
        if method == "initialize":
            return {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "neural-memory-graph", "version": "2.0.0"}
            }
        elif method == "tools/list":
            return {"tools": get_tools_list()}
        elif method == "tools/call":
            return handle_tool_call(params)
        return {"error": {"code": -32601, "message": f"Method not found: {method}"}}
    except Exception as e:
        return {"error": {"code": -32603, "message": str(e)}}


def get_tools_list():
    """Return list of available MCP tools"""
    return [
        {
            "name": "search_memory",
            "description": "Search through notes using spreading activation algorithm",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "limit": {"type": "integer", "default": 5, "minimum": 1, "maximum": 20}
                },
                "required": ["query"]
            }
        },
        {
            "name": "add_note",
            "description": "Add new note with automatic entity extraction and linking",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Note content"},
                    "category": {"type": "string", "default": "general"}
                },
                "required": ["content"]
            }
        },
        {
            "name": "update_note",
            "description": "Update existing note by ID",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "note_id": {"type": "integer"},
                    "content": {"type": "string"},
                    "category": {"type": "string"}
                },
                "required": ["note_id", "content"]
            }
        },
        {
            "name": "delete_note",
            "description": "Delete note by ID",
            "inputSchema": {
                "type": "object",
                "properties": {"note_id": {"type": "integer"}},
                "required": ["note_id"]
            }
        },
        {
            "name": "neural_stats",
            "description": "Get statistics about stored notes, edges, and entities",
            "inputSchema": {"type": "object", "properties": {}}
        },
        {
            "name": "get_graph",
            "description": "Get graph connections for a specific note",
            "inputSchema": {
                "type": "object",
                "properties": {"note_id": {"type": "integer"}},
                "required": ["note_id"]
            }
        }
    ]


def handle_tool_call(params):
    """Execute tool calls"""
    tool_name = params.get("name")
    args = params.get("arguments", {})
    
    if tool_name == "search_memory":
        return tool_search_memory(args.get("query", ""), args.get("limit", 5))
    elif tool_name == "add_note":
        return tool_add_note(args.get("content", ""), args.get("category", "general"))
    elif tool_name == "update_note":
        return tool_update_note(args.get("note_id"), args.get("content"), args.get("category"))
    elif tool_name == "delete_note":
        return tool_delete_note(args.get("note_id"))
    elif tool_name == "neural_stats":
        return tool_stats()
    elif tool_name == "get_graph":
        return tool_get_graph(args.get("note_id"))
    
    return {"error": {"code": -32602, "message": f"Unknown tool: {tool_name}"}}


def tool_search_memory(query: str, limit: int):
    """Search with spreading activation"""
    results = search_with_activation(query, limit)
    
    if not results:
        text = f"No results found for: {query}"
    else:
        text = f"Found {len(results)} notes:\n\n"
        for r in results:
            text += f"[ID:{r['id']}] [{r['category']}] (activation: {r['activation']})\n"
            text += f"{r['content']}\n\n"
    
    return {"content": [{"type": "text", "text": text}]}


def tool_add_note(content: str, category: str):
    """Add note with auto-linking"""
    if not content:
        return {"error": {"code": -32602, "message": "Content required"}}
    
    result = add_note_with_links(content, category)
    
    text = f"✅ Added note #{result['node_id']}\n"
    text += f"Category: {category}\n"
    text += f"Entities found: {result['entities']}\n"
    text += f"Entity links created: {result['entity_links']}\n"
    text += f"Semantic links created: {result['semantic_links']}"
    
    return {"content": [{"type": "text", "text": text}]}


def tool_update_note(note_id: int, content: str, category: str = None):
    """Update existing note"""
    if not note_id or not content:
        return {"error": {"code": -32602, "message": "Note ID and content required"}}
    
    existing = get_node(note_id)
    if not existing:
        return {"error": {"code": -32602, "message": f"Note #{note_id} not found"}}
    
    model = get_model()
    embedding = model.encode(content)[0]
    db_update_node(note_id, content, category, embedding.tobytes())
    
    return {"content": [{"type": "text", "text": f"✅ Updated note #{note_id}"}]}


def tool_delete_note(note_id: int):
    """Delete note"""
    if not note_id:
        return {"error": {"code": -32602, "message": "Note ID required"}}
    
    deleted = db_delete_node(note_id)
    if not deleted:
        return {"error": {"code": -32602, "message": f"Note #{note_id} not found"}}
    
    text = f"✅ Deleted note #{note_id}\nWas: [{deleted['category']}] {deleted['content'][:100]}..."
    return {"content": [{"type": "text", "text": text}]}


def tool_stats():
    """Get statistics"""
    stats = get_stats()
    
    text = "📊 Neural Memory Graph Statistics\n\n"
    text += f"Total nodes: {stats['total_nodes']}\n"
    text += f"Total edges: {stats['total_edges']}\n"
    text += f"Total entities: {stats['total_entities']}\n\n"
    
    text += "Nodes by category:\n"
    for cat, count in sorted(stats['nodes_by_category'].items()):
        text += f"  - {cat}: {count}\n"
    
    text += "\nEdges by type:\n"
    for etype, count in sorted(stats['edges_by_type'].items()):
        text += f"  - {etype}: {count}\n"
    
    return {"content": [{"type": "text", "text": text}]}


def tool_get_graph(note_id: int):
    """Get graph for a note"""
    if not note_id:
        return {"error": {"code": -32602, "message": "Note ID required"}}
    
    graph = get_node_graph(note_id)
    if "error" in graph:
        return {"error": {"code": -32602, "message": graph["error"]}}
    
    text = f"🔗 Graph for note #{note_id}\n\n"
    text += f"Node: {graph['node']['content']}\n\n"
    text += f"Connections ({len(graph['connections'])}):\n"
    
    for conn in graph['connections']:
        text += f"  → [{conn['type']}] (weight: {conn['weight']:.2f}) #{conn['id']}: {conn['content']}\n"
    
    return {"content": [{"type": "text", "text": text}]}


def create_mcp_endpoint(app):
    """Register MCP SSE endpoint with Flask app"""
    
    @app.route("/sse", methods=["POST", "GET"])
    def mcp_sse():
        if not verify_auth(request):
            return jsonify({"error": "Unauthorized"}), 401
        
        def generate():
            try:
                data = request.get_json() if request.method == "POST" else {}
                method = data.get("method", "initialize")
                params = data.get("params", {})
                req_id = data.get("id", 1)
                
                result = handle_mcp_request(method, params)
                response = {"jsonrpc": "2.0", "id": req_id, "result": result}
                yield f"data: {json.dumps(response)}\n\n"
            
            except Exception as e:
                error = {"jsonrpc": "2.0", "id": 1, "error": {"code": -32603, "message": str(e)}}
                yield f"data: {json.dumps(error)}\n\n"
        
        return Response(
            stream_with_context(generate()),
            mimetype="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
                "Access-Control-Allow-Origin": "*"
            }
        )
    
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "version": "2.0.0"})
