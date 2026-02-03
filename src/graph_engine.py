#!/usr/bin/env python3
"""
Graph Engine for Neural Memory Graph
Implements spreading activation search and automatic linking
"""

import numpy as np
import os
from datetime import datetime
from typing import List, Dict, Any

from database import (
    create_node, get_node, get_all_nodes, touch_node,
    create_edge, get_connected_nodes,
    get_or_create_entity, link_node_to_entity, get_nodes_by_entity
)
from stable_embeddings import get_model
from entity_extractor import extract_entities
from ann_index import get_ann_index
from graph_cache import get_graph_cache

# Configuration from environment
ACTIVATION_ITERATIONS = int(os.getenv("ACTIVATION_ITERATIONS", "3"))
ACTIVATION_DECAY = float(os.getenv("ACTIVATION_DECAY", "0.7"))
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.5"))
HALF_LIFE_DAYS = float(os.getenv("HALF_LIFE_DAYS", "30"))
MAX_SEMANTIC_LINKS = int(os.getenv("MAX_SEMANTIC_LINKS", "5"))


def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors"""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def recency_factor(last_accessed_str, created_str=None, half_life_days=HALF_LIFE_DAYS):
    """
    Calculate temporal decay factor based on last access time.
    
    Uses last_accessed primarily (when was this note last useful?).
    Falls back to created timestamp if last_accessed not available.
    
    Returns value between 0 and 1:
    - 1.0 = accessed today
    - 0.5 = accessed half_life_days ago
    - 0.25 = accessed 2*half_life_days ago
    """
    # Prefer last_accessed over created timestamp
    timestamp_str = last_accessed_str or created_str
    
    if not timestamp_str:
        return 0.5
    
    try:
        timestamp = datetime.fromisoformat(timestamp_str)
        age_days = (datetime.now() - timestamp).days
        
        # Minimum factor to prevent old notes from completely disappearing
        min_factor = 0.1
        decay = 0.5 ** (age_days / half_life_days)
        
        return max(min_factor, decay)
    except:
        return 0.5


def importance_factor(importance, access_count=0):
    """
    Calculate importance multiplier for activation.
    
    Base factors:
    - critical: 2.0x (anchor notes, identity, key decisions)
    - normal: 1.0x (default)
    - low: 0.5x (temporary, noise)
    
    Also applies small boost for frequently accessed notes.
    """
    base_factors = {
        'critical': 2.0,
        'normal': 1.0,
        'low': 0.5
    }
    base = base_factors.get(importance, 1.0)
    
    # Small boost for frequently accessed notes (max +50%)
    # access_count of 10 gives +25%, 20 gives +50%
    access_boost = min(0.5, (access_count or 0) * 0.025)
    
    return base + access_boost


# Deduplication thresholds
DUPLICATE_THRESHOLD = float(os.getenv("DUPLICATE_THRESHOLD", "0.95"))  # Block creation
SIMILAR_THRESHOLD = float(os.getenv("SIMILAR_THRESHOLD", "0.90"))  # Warn about similar


def find_similar_notes(content, threshold=SIMILAR_THRESHOLD, limit=5):
    """
    Find notes similar to given content.
    
    Returns list of (node_id, similarity, content_preview) tuples.
    Useful for deduplication and finding related notes.
    """
    model = get_model()
    query_emb = model.encode(content)[0]
    
    all_nodes = get_all_nodes()
    similarities = []
    
    for node in all_nodes:
        if node["embedding"] is None:
            continue
        
        node_emb = np.frombuffer(node["embedding"], dtype=np.float32)
        sim = cosine_similarity(query_emb, node_emb)
        
        if sim >= threshold:
            similarities.append({
                "id": node["id"],
                "similarity": round(sim, 4),
                "content": node["content"][:200],
                "category": node["category"]
            })
    
    similarities.sort(key=lambda x: x["similarity"], reverse=True)
    return similarities[:limit]


def add_note_with_links(content, category="general", importance="normal", force=False,
                        emotional_tone=None, emotional_intensity=5, emotional_reflection=None):
    """
    Add note with automatic entity extraction, linking, and emotional context.
    
    1. Check for duplicates (unless force=True)
    2. Create embedding (includes emotional context if provided)
    3. Extract entities (people, concepts, projects)
    4. Link to other notes sharing same entities
    5. Find semantically similar notes and create edges
    
    Returns dict with node_id and link statistics.
    If duplicate found, returns error with existing note info.
    """
    model = get_model()
    
    # Include emotional context in embedding if provided
    full_text = content
    if emotional_tone or emotional_reflection:
        emotional_context = []
        if emotional_tone:
            emotional_context.append(f"Emotional tone: {emotional_tone}")
        if emotional_reflection:
            emotional_context.append(emotional_reflection)
        full_text = f"{content}\n\n{'. '.join(emotional_context)}"
    
    embedding = model.encode(full_text)[0]
    
    # Get ANN index once (used for both duplicate check and semantic links)
    ann_index = get_ann_index()
    
    # Check for duplicates unless forced
    # OPTIMIZED: Use ANN index for O(log n) instead of O(n) linear scan
    if not force:
        if ann_index.enabled:
            # Fast duplicate check using ANN index
            d = ann_index.search(embedding, k=5, min_similarity=DUPLICATE_THRESHOLD)
            if d:
                eid,sim = d[0]
                en = get_node(eid)
                if en: return {"error": "duplicate", "message": f"Similar note exists ({sim:.2%})", "existing_id": eid, "existing_content": en["content"][:200], "similarity": round(sim, 4)}
        else:
            # Fallback to linear scan if ANN not enabled
            for n in get_all_nodes():
                if n["embedding"] is None: continue
                sim = cosine_similarity(embedding, np.frombuffer(n["embedding"], dtype=np.float32))
                if sim >= DUPLICATE_THRESHOLD: return {"error": "duplicate", "message": f"Similar note exists ({sim:.2%})", "existing_id": n["id"], "existing_content": n["content"][:200], "similarity": round(sim, 4)}
    
    # Create the node with emotional context
    node_id = create_node(content, category, embedding.tobytes(), importance, emotional_tone, emotional_intensity, emotional_reflection)
    
    # Add to ANN index incrementally (enables immediate search for this note)
    if ann_index.enabled: ann_index.add_vector(node_id, embedding)
    
    # Extract entities and create entity-based links
    entities = extract_entities(content)
    entity_links = []
    
    for en,et in entities:
        eid = get_or_create_entity(en, et)
        link_node_to_entity(node_id, eid)
        for r in get_nodes_by_entity(eid):
            if r["id"] != node_id:
                create_edge(node_id, r["id"], weight=0.6, edge_type="entity")
                create_edge(r["id"], node_id, weight=0.6, edge_type="entity")
                entity_links.append(r["id"])
    
    # Find semantically similar notes
    # OPTIMIZED: Use ANN index for O(log n) instead of O(n) linear scan
    semantic_links = []
    similar_warnings = []
    
    if ann_index.enabled:
        # Fast semantic search using ANN index
        # Request 2x candidates to account for self-reference filtering
        sims = [(n,s) for n,s in ann_index.search(embedding, k=MAX_SEMANTIC_LINKS*2, min_similarity=SIMILARITY_THRESHOLD) if n!=node_id]
    else:
        # Fallback to linear scan if ANN not enabled
        sims = []
        for n in get_all_nodes():
            if n["id"]==node_id or n["embedding"] is None: continue
            sim = cosine_similarity(embedding, np.frombuffer(n["embedding"], dtype=np.float32))
            if sim >= SIMILARITY_THRESHOLD: sims.append((n["id"], sim))
        sims.sort(key=lambda x: x[1], reverse=True)
    
    # Create edges for top MAX_SEMANTIC_LINKS similar nodes
    for rid,sim in sims[:MAX_SEMANTIC_LINKS]:
        create_edge(node_id, rid, weight=sim, edge_type="semantic")
        create_edge(rid, node_id, weight=sim, edge_type="semantic")
        semantic_links.append((rid, sim))
        if sim >= SIMILAR_THRESHOLD: similar_warnings.append({"id": rid, "similarity": round(sim, 4)})

    
    result = {
        "node_id": node_id,
        "entities": entities,
        "entity_links": len(set(entity_links)),
        "semantic_links": len(semantic_links)
    }
    
    if similar_warnings:
        result["warning"] = "Similar notes exist"
        result["similar_notes"] = similar_warnings
    
    return result


def search_with_activation(query, limit=5, iterations=ACTIVATION_ITERATIONS, decay=ACTIVATION_DECAY, category_filter=None):
    """
    Search using spreading activation algorithm.
    
    1. Compute initial activation from query similarity
    2. Spread activation through graph edges
    3. Apply temporal decay (recent notes score higher)
    4. Return top activated nodes
    
    Args:
        query: Search query string
        limit: Max results to return
        iterations: Spreading activation iterations  
        decay: Activation decay factor
        category_filter: Optional category to filter results (e.g., "breakthrough", "technical")
    
    This finds notes that are:
    - Semantically similar to query
    - Connected to similar notes through shared entities
    - Recently accessed (recency boost)
    - Optionally filtered by category
    """
    model = get_model()
    query_emb = model.encode(query)[0]
    
    all_nodes = get_all_nodes()
    
    # Step 1: Initialize activation from semantic similarity
    # Try ANN index first (O(log n)), fallback to linear scan (O(n))
    ann_index = get_ann_index()
    activations = {}
    
    if ann_index.enabled and len(ann_index.node_ids) > 0:
        # Fast ANN search
        results = ann_index.search(query_emb, k=limit*3, min_similarity=0.0)
        for node_id, sim in results:
            activations[node_id] = sim
        print(f"🚀 ANN search: {len(activations)} initial candidates")
    else:
        # Fallback: linear scan through all nodes
        for node in all_nodes:
            if node["embedding"] is None:
                continue
            node_emb = np.frombuffer(node["embedding"], dtype=np.float32)
            sim = cosine_similarity(query_emb, node_emb)
            if sim >= 0.3:
                activations[node["id"]] = sim
        print(f"⚠️  Linear search: {len(activations)} initial candidates (ANN disabled)")
    
    # Step 2: Spreading activation with normalization and damping
    for iteration in range(iterations):
        new_activations = {}
        
        # Spread from activated nodes
        for node_id, activation in activations.items():
            if activation < 0.01:  # Skip very weakly activated nodes
                continue
            
            # Keep original activation (with decay)
            new_activations[node_id] = new_activations.get(node_id, 0) + activation * decay
            
            # Spread to neighbors
            # Use in-memory graph cache (O(1) instead of SQL)
            graph_cache = get_graph_cache()
            neighbors = graph_cache.get_neighbors(node_id)
            for neighbor_id, edge_weight, edge_type in neighbors:
                
                # Spread activation through edge
                spread = activation * edge_weight * decay
                
                # Add to neighbor's activation
                new_activations[neighbor_id] = new_activations.get(neighbor_id, 0) + spread
        
        # Normalization: scale to 0-1 range based on max
        if new_activations:
            max_activation = max(new_activations.values())
            if max_activation > 0:
                for node_id in new_activations:
                    new_activations[node_id] /= max_activation
        
        activations = new_activations
        
        # Debug output
        if activations:
            print(f"  Iteration {iteration+1}: {len(activations)} nodes, max={max(activations.values()):.4f}, sum={sum(activations.values()):.4f}")

    
    # Step 3: Apply temporal decay and importance scoring
    node_map = {n["id"]: n for n in all_nodes}
    for node_id in activations:
        if node_id in node_map:
            node = node_map[node_id]
            last_accessed = node.get("last_accessed")
            created = node.get("timestamp")
            importance = node.get("importance", "normal")
            access_count = node.get("access_count", 0)
            
            # Apply both factors
            activations[node_id] *= recency_factor(last_accessed, created)
            activations[node_id] *= importance_factor(importance, access_count)
    
    # Step 4: Sort and return top results
    sorted_nodes = sorted(activations.items(), key=lambda x: x[1], reverse=True)
    
    results = []
    for node_id, activation in sorted_nodes:
        node = node_map.get(node_id)
        if not node:
            continue
            
        # Filter by category if specified
        if category_filter and node.get("category") != category_filter:
            continue
            
        # Update access tracking
        touch_node(node_id)
        results.append({
            "id": node_id,
            "content": node["content"],
            "category": node["category"],
            "activation": round(activation, 4),
            "timestamp": node.get("timestamp")
        })
        
        # Stop when we have enough results
        if len(results) >= limit:
            break
    
    return results


def get_node_graph(node_id):
    """Get graph visualization data for a specific node"""
    node = get_node(node_id)
    if not node:
        return {"error": "Node not found"}
    
    connected = get_connected_nodes(node_id)
    
    return {
        "node": {
            "id": node_id,
            "content": node["content"][:100],
            "category": node["category"]
        },
        "connections": [
            {
                "id": c["id"],
                "content": c["content"][:100] if c.get("content") else "",
                "weight": c.get("weight", 0.5),
                "type": c.get("edge_type", "unknown")
            }
            for c in connected
        ]
    }
