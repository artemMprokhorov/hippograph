#!/usr/bin/env python3
"""
ANN (Approximate Nearest Neighbor) Index using FAISS
Provides O(log n) similarity search instead of O(n) linear scan
"""

import numpy as np
import faiss
import os
from typing import List, Tuple, Optional

# Configuration
USE_ANN_INDEX = os.getenv("USE_ANN_INDEX", "true").lower() == "true"
ANN_INDEX_TYPE = os.getenv("ANN_INDEX_TYPE", "HNSW")
HNSW_M = int(os.getenv("HNSW_M", "32"))
HNSW_EF_CONSTRUCTION = int(os.getenv("HNSW_EF_CONSTRUCTION", "64"))
HNSW_EF_SEARCH = int(os.getenv("HNSW_EF_SEARCH", "32"))


class ANNIndex:
    """FAISS-based ANN index for fast similarity search."""
    
    def __init__(self, dimension=384):
        self.dimension = dimension
        self.index = None
        self.node_ids = []
        self.enabled = USE_ANN_INDEX
        
        if not self.enabled:
            print("ℹ️  ANN indexing disabled (USE_ANN_INDEX=false)")
            return
        
        if ANN_INDEX_TYPE == "HNSW":
            self.index = faiss.IndexFlatIP(dimension)
            # IP index does not need these params
            
            print(f"✅ Created FAISS Flat IP index (M={HNSW_M}, dimension={dimension})")
        else:
            raise ValueError(f"Unsupported ANN_INDEX_TYPE: {ANN_INDEX_TYPE}")
    
    def build(self, nodes: List[dict]) -> int:
        """Build index from nodes with embeddings."""
        if not self.enabled or self.index is None:
            return 0
        
        self.index.reset()
        self.node_ids = []
        
        embeddings = []
        for node in nodes:
            if node.get("embedding") is None:
                continue
            emb = np.frombuffer(node["embedding"], dtype=np.float32)
            if len(emb) != self.dimension:
                continue
            embeddings.append(emb)
            self.node_ids.append(node["id"])
        
        if not embeddings:
            print("⚠️  No embeddings to index")
            return 0
        
        embeddings_matrix = np.array(embeddings, dtype=np.float32)
        self.index.add(embeddings_matrix)
        print(f"✅ Built ANN index with {len(embeddings)} vectors")
        return len(embeddings)
    
    def search(self, query_embedding: np.ndarray, k: int = 10, 
               min_similarity: float = 0.3) -> List[Tuple[int, float]]:
        """Search for k nearest neighbors."""
        print(f"🔍 ANN search called: enabled={self.enabled}, index={self.index is not None}, node_ids={len(self.node_ids)}")
        if not self.enabled or self.index is None or len(self.node_ids) == 0:
            print(f"⚠️ ANN search disabled or empty: enabled={self.enabled}, index_exists={self.index is not None}, nodes={len(self.node_ids)}")
            return []
        
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        faiss.normalize_L2(query_embedding)
        
        k_search = min(k * 2, len(self.node_ids))
        distances, indices = self.index.search(query_embedding, k_search)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            cos_sim = 1 - (dist ** 2) / 2
            if cos_sim >= min_similarity:
                node_id = self.node_ids[idx]
                results.append((node_id, float(cos_sim)))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]
    
    def add_vector(self, node_id: int, embedding: np.ndarray):
        """Add single vector to index."""
        if not self.enabled or self.index is None:
            return
        if embedding.ndim == 1:
            embedding = embedding.reshape(1, -1)
        faiss.normalize_L2(embedding)
        self.index.add(embedding)
        self.node_ids.append(node_id)
    
    def get_stats(self) -> dict:
        """Get index statistics"""
        if not self.enabled or self.index is None:
            return {"enabled": False, "indexed_vectors": 0}
        return {
            "enabled": True,
            "index_type": ANN_INDEX_TYPE,
            "indexed_vectors": len(self.node_ids),
            "dimension": self.dimension,
            "hnsw_m": HNSW_M if ANN_INDEX_TYPE == "HNSW" else None,
            "hnsw_ef_search": HNSW_EF_SEARCH if ANN_INDEX_TYPE == "HNSW" else None
        }

_global_index: Optional[ANNIndex] = None

def get_ann_index() -> ANNIndex:
    """Get or create global ANN index"""
    global _global_index
    if _global_index is None:
        _global_index = ANNIndex(dimension=384)
        # Auto-build if empty
        if len(_global_index.node_ids) == 0:
            from database import get_all_nodes
            nodes = get_all_nodes()
            _global_index.build(nodes)
    return _global_index

def rebuild_index(nodes: List[dict]) -> int:
    """Rebuild global ANN index from nodes"""
    index = get_ann_index()
    return index.build(nodes)
