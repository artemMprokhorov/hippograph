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
                "serverInfo": {"name": "hippograph", "version": "2.0.0"}
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
                    "limit": {"type": "integer", "default": 5, "minimum": 1, "maximum": 20},
                    "category": {"type": "string", "description": "Optional: filter results by category (e.g., 'breakthrough', 'technical')"},
                    "time_after": {"type": "string", "description": "Optional: only return notes created after this datetime (ISO format: '2026-01-01T00:00:00')"},
                    "time_before": {"type": "string", "description": "Optional: only return notes created before this datetime (ISO format: '2026-02-01T00:00:00')"},
                    "entity_type": {"type": "string", "description": "Optional: only return notes containing entities of this type (e.g., 'person', 'organization', 'concept', 'location', 'tech')"}
                },
                "required": ["query"]
            }
        },
        {
            "name": "add_note",
            "description": "Add new note with automatic entity extraction, linking, and emotional context. Checks for duplicates.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Note content"},
                    "category": {"type": "string", "default": "general"},
                    "importance": {"type": "string", "enum": ["critical", "normal", "low"], "default": "normal", "description": "Note importance level"},
                    "force": {"type": "boolean", "default": False, "description": "Force add even if duplicate exists"},
                    "emotional_tone": {"type": "string", "description": "Keywords describing emotional tone (e.g., 'joy, validation, trust')"},
                    "emotional_intensity": {"type": "integer", "default": 5, "minimum": 0, "maximum": 10, "description": "Emotional intensity from 0 (none) to 10 (very strong)"},
                    "emotional_reflection": {"type": "string", "description": "Narrative reflection on emotional context"}
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
        },
        {
            "name": "set_importance",
            "description": "Set importance level for a note: 'critical' (2x boost), 'normal', or 'low' (0.5x)",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "note_id": {"type": "integer"},
                    "importance": {"type": "string", "enum": ["critical", "normal", "low"]}
                },
                "required": ["note_id", "importance"]
            }
        },
        {
            "name": "find_similar",
            "description": "Find notes similar to given content. Useful for checking before adding new notes.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Content to find similar notes for"},
                    "threshold": {"type": "number", "default": 0.7, "description": "Minimum similarity (0-1)"},
                    "limit": {"type": "integer", "default": 5}
                },
                "required": ["content"]
            }
        }
    ]


def handle_tool_call(params):
    """Execute tool calls"""
    tool_name = params.get("name")
    args = params.get("arguments", {})
    
    if tool_name == "search_memory":
        return tool_search_memory(
            args.get("query", ""), 
            args.get("limit", 5),
            args.get("category", None),
            args.get("time_after", None),
            args.get("time_before", None),
            args.get("entity_type", None)
        )
    elif tool_name == "add_note":
        return tool_add_note(
            args.get("content", ""), 
            args.get("category", "general"),
            args.get("importance", "normal"),
            args.get("force", False)
        )
    elif tool_name == "update_note":
        return tool_update_note(args.get("note_id"), args.get("content"), args.get("category"))
    elif tool_name == "delete_note":
        return tool_delete_note(args.get("note_id"))
    elif tool_name == "neural_stats":
        return tool_stats()
    elif tool_name == "get_graph":
        return tool_get_graph(args.get("note_id"))
    elif tool_name == "set_importance":
        return tool_set_importance(args.get("note_id"), args.get("importance"))
    elif tool_name == "find_similar":
        return tool_find_similar(args.get("content", ""), args.get("threshold", 0.7), args.get("limit", 5))
    
    return {"error": {"code": -32602, "message": f"Unknown tool: {tool_name}"}}


def tool_search_memory(query: str, limit: int, category: str = None, 
                      time_after: str = None, time_before: str = None, entity_type: str = None):
    """Search with spreading activation and optional filters (category, time range, entity type)"""
    results = search_with_activation(query, limit, 
                                     category_filter=category,
                                     time_after=time_after, 
                                     time_before=time_before,
                                     entity_type_filter=entity_type)
    
    if not results:
        filters = []
        if category:
            filters.append(f"category: {category}")
        if time_after:
            filters.append(f"after: {time_after[:10]}")
        if time_before:
            filters.append(f"before: {time_before[:10]}")
        if entity_type:
            filters.append(f"entity_type: {entity_type}")
        
        if filters:
            text = f"No results found for: {query} ({', '.join(filters)})"
        else:
            text = f"No results found for: {query}"
    else:
        filters_desc = []
        if category:
            filters_desc.append(f"category '{category}'")
        if time_after or time_before:
            if time_after and time_before:
                filters_desc.append(f"{time_after[:10]} to {time_before[:10]}")
            elif time_after:
                filters_desc.append(f"after {time_after[:10]}")
            elif time_before:
                filters_desc.append(f"before {time_before[:10]}")
        if entity_type:
            filters_desc.append(f"entity_type '{entity_type}'")
        
        if filters_desc:
            text = f"Found {len(results)} notes ({', '.join(filters_desc)}):\n\n"
        else:
            text = f"Found {len(results)} notes:\n\n"
            
        for r in results:
            text += f"[ID:{r['id']}] [{r['category']}] (activation: {r['activation']})\n"
            text += f"{r['content']}\n\n"
    
    return {"content": [{"type": "text", "text": text}]}


def tool_add_note(content: str, category: str, importance: str = "normal", force: bool = False,
                  emotional_tone: str = None, emotional_intensity: int = 5, emotional_reflection: str = None):
    """Add note with auto-linking, duplicate detection, and emotional context"""
    if not content:
        return {"error": {"code": -32602, "message": "Content required"}}
    
    result = add_note_with_links(content, category, importance, force,
                                 emotional_tone, emotional_intensity, emotional_reflection)
    
    # Handle duplicate error
    if "error" in result and result["error"] == "duplicate":
        text = f"⚠️ {result['message']}\n"
        text += f"Existing note #{result['existing_id']}: {result['existing_content']}...\n"
        text += f"Use force=true to add anyway."
        return {"content": [{"type": "text", "text": text}]}
    
    text = f"✅ Added note #{result['node_id']}\n"
    text += f"Category: {category}\n"
    text += f"Importance: {importance}\n"
    if emotional_tone:
        text += f"Emotional tone: {emotional_tone}\n"
        text += f"Intensity: {emotional_intensity}/10\n"
    text += f"Entities found: {result['entities']}\n"
    text += f"Entity links created: {result['entity_links']}\n"
    text += f"Semantic links created: {result['semantic_links']}"
    
    # Add warning about similar notes
    if "warning" in result:
        text += f"\n\n⚠️ {result['warning']}:"
        for sim in result.get("similar_notes", []):
            text += f"\n  - Note #{sim['id']} (similarity: {sim['similarity']:.0%})"
    
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


def tool_set_importance(note_id: int, importance: str):
    """Set importance level for a note"""
    if not note_id or not importance:
        return {"error": {"code": -32602, "message": "Note ID and importance required"}}
    
    if importance not in ('critical', 'normal', 'low'):
        return {"error": {"code": -32602, "message": "Importance must be 'critical', 'normal', or 'low'"}}
    
    from database import set_importance
    success = set_importance(note_id, importance)
    
    if success:
        multipliers = {'critical': '2.0x', 'normal': '1.0x', 'low': '0.5x'}
        text = f"✅ Note #{note_id} importance set to '{importance}' ({multipliers[importance]} activation)"
    else:
        text = f"❌ Note #{note_id} not found"
    
    return {"content": [{"type": "text", "text": text}]}


def tool_find_similar(content: str, threshold: float = 0.7, limit: int = 5):
    """Find notes similar to given content"""
    if not content:
        return {"error": {"code": -32602, "message": "Content required"}}
    
    from graph_engine import find_similar_notes
    similar = find_similar_notes(content, threshold, limit)
    
    if not similar:
        text = f"No similar notes found (threshold: {threshold:.0%})"
    else:
        text = f"Found {len(similar)} similar notes:\n\n"
        for s in similar:
            text += f"[ID:{s['id']}] [{s['category']}] (similarity: {s['similarity']:.0%})\n"
            text += f"{s['content']}...\n\n"
    
    return {"content": [{"type": "text", "text": text}]}


def create_mcp_endpoint(app):
    """Register MCP SSE endpoint with Flask app"""
    
    @app.route("/sse", methods=["POST", "GET"])
    @app.route("/sse2", methods=["POST", "GET"])
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
