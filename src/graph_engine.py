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

# Configuration from environment
ACTIVATION_ITERATIONS = int(os.getenv("ACTIVATION_ITERATIONS", "3"))
ACTIVATION_DECAY = float(os.getenv("ACTIVATION_DECAY", "0.7"))
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.5"))
HALF_LIFE_DAYS = float(os.getenv("HALF_LIFE_DAYS", "30"))
MAX_SEMANTIC_LINKS = int(os.getenv("MAX_SEMANTIC_LINKS", "5"))


def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors"""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def recency_factor(timestamp_str, half_life_days=HALF_LIFE_DAYS):
    """Calculate temporal decay factor based on age"""
    if not timestamp_str:
        return 0.5
    try:
        timestamp = datetime.fromisoformat(timestamp_str)
        age_days = (datetime.now() - timestamp).days
        # Exponential decay: factor halves every half_life_days
        return 0.5 ** (age_days / half_life_days)
    except:
        return 0.5


def add_note_with_links(content, category="general"):
    """
    Add note with automatic entity extraction and linking.
    
    1. Create embedding for the note
    2. Extract entities (people, concepts, projects)
    3. Link to other notes sharing same entities
    4. Find semantically similar notes and create edges
    
    Returns dict with node_id and link statistics
    """
    model = get_model()
    embedding = model.encode(content)[0]
    
    # Create the node
    node_id = create_node(content, category, embedding.tobytes())
    
    # Extract entities and create entity-based links
    entities = extract_entities(content)
    entity_links = []
    
    for entity_name, entity_type in entities:
        entity_id = get_or_create_entity(entity_name, entity_type)
        link_node_to_entity(node_id, entity_id)
        
        # Find other nodes with the same entity
        related_nodes = get_nodes_by_entity(entity_id)
        for related in related_nodes:
            if related["id"] != node_id:
                # Create bidirectional edges
                create_edge(node_id, related["id"], weight=0.6, edge_type="entity")
                create_edge(related["id"], node_id, weight=0.6, edge_type="entity")
                entity_links.append(related["id"])
    
    # Find semantically similar notes
    all_nodes = get_all_nodes()
    semantic_links = []
    
    similarities = []
    for node in all_nodes:
        if node["id"] == node_id or node["embedding"] is None:
            continue
        
        node_emb = np.frombuffer(node["embedding"], dtype=np.float32)
        sim = cosine_similarity(embedding, node_emb)
        
        if sim >= SIMILARITY_THRESHOLD:
            similarities.append((node["id"], sim))
    
    # Create edges for top similar nodes
    similarities.sort(key=lambda x: x[1], reverse=True)
    for related_id, sim in similarities[:MAX_SEMANTIC_LINKS]:
        create_edge(node_id, related_id, weight=sim, edge_type="semantic")
        create_edge(related_id, node_id, weight=sim, edge_type="semantic")
        semantic_links.append((related_id, sim))
    
    return {
        "node_id": node_id,
        "entities": entities,
        "entity_links": len(set(entity_links)),
        "semantic_links": len(semantic_links)
    }


def search_with_activation(query, limit=5, iterations=ACTIVATION_ITERATIONS, decay=ACTIVATION_DECAY):
    """
    Search using spreading activation algorithm.
    
    1. Compute initial activation from query similarity
    2. Spread activation through graph edges
    3. Apply temporal decay (recent notes score higher)
    4. Return top activated nodes
    
    This finds notes that are:
    - Semantically similar to query
    - Connected to similar notes through shared entities
    - Recently accessed (recency boost)
    """
    model = get_model()
    query_emb = model.encode(query)[0]
    
    all_nodes = get_all_nodes()
    
    # Step 1: Initialize activation from semantic similarity
    activations = {}
    for node in all_nodes:
        if node["embedding"] is None:
            continue
        
        node_emb = np.frombuffer(node["embedding"], dtype=np.float32)
        sim = cosine_similarity(query_emb, node_emb)
        
        # Only activate nodes with minimum similarity
        if sim >= 0.3:
            activations[node["id"]] = sim
    
    # Step 2: Spreading activation
    for _ in range(iterations):
        new_activations = activations.copy()
        
        for node_id, activation in activations.items():
            if activation < 0.1:  # Skip weakly activated nodes
                continue
            
            connected = get_connected_nodes(node_id)
            for neighbor in connected:
                neighbor_id = neighbor["id"]
                edge_weight = neighbor.get("weight", 0.5)
                
                # Spread activation through edge
                spread = activation * edge_weight * decay
                
                if neighbor_id in new_activations:
                    # Combine with existing activation (not replace)
                    new_activations[neighbor_id] = max(
                        new_activations[neighbor_id],
                        new_activations[neighbor_id] + spread * 0.5
                    )
                else:
                    new_activations[neighbor_id] = spread
        
        activations = new_activations

    
    # Step 3: Apply temporal decay
    node_map = {n["id"]: n for n in all_nodes}
    for node_id in activations:
        if node_id in node_map:
            timestamp = node_map[node_id].get("timestamp")
            activations[node_id] *= recency_factor(timestamp)
    
    # Step 4: Sort and return top results
    sorted_nodes = sorted(activations.items(), key=lambda x: x[1], reverse=True)
    
    results = []
    for node_id, activation in sorted_nodes[:limit]:
        node = node_map.get(node_id)
        if node:
            # Update access tracking
            touch_node(node_id)
            results.append({
                "id": node_id,
                "content": node["content"],
                "category": node["category"],
                "activation": round(activation, 4),
                "timestamp": node.get("timestamp")
            })
    
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
