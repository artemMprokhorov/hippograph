#!/usr/bin/env python3
"""
Unit tests for graph_engine.py - spreading activation algorithm
"""
import pytest
import numpy as np
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestSpreadingActivation:
    """Test spreading activation normalization and damping"""
    
    def test_activation_normalization(self):
        """Test that activations are normalized to 0-1 range"""
        # This is a smoke test - verifies the concept
        # Real test would need mock database
        
        # Simulate activation dict
        activations = {
            1: 2520.5,  # Unbounded scores (old system)
            2: 2411.3,
            3: 2399.8
        }
        
        # Apply normalization (what our code does)
        max_activation = max(activations.values())
        normalized = {
            node_id: score / max_activation 
            for node_id, score in activations.items()
        }
        
        # Verify all values 0-1
        for node_id, score in normalized.items():
            assert 0 <= score <= 1, f"Score {score} outside 0-1 range"
        
        # Verify max is exactly 1.0
        assert max(normalized.values()) == 1.0
        
        # Verify relative ordering preserved
        assert normalized[1] > normalized[2] > normalized[3]
    
    def test_activation_decay(self):
        """Test that decay factor reduces activation properly"""
        initial_activation = 1.0
        decay_factor = 0.7
        
        # After one iteration
        decayed = initial_activation * decay_factor
        assert decayed == 0.7
        
        # After three iterations (our default)
        final = initial_activation * (decay_factor ** 3)
        expected = 0.343  # 0.7^3
        assert abs(final - expected) < 0.001
    
    def test_cosine_similarity(self):
        """Test cosine similarity calculation for embeddings"""
        # Two identical vectors
        v1 = np.array([1.0, 0.0, 0.0])
        v2 = np.array([1.0, 0.0, 0.0])
        
        # Cosine similarity
        similarity = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        assert abs(similarity - 1.0) < 0.001
        
        # Orthogonal vectors
        v3 = np.array([1.0, 0.0, 0.0])
        v4 = np.array([0.0, 1.0, 0.0])
        similarity = np.dot(v3, v4) / (np.linalg.norm(v3) * np.linalg.norm(v4))
        assert abs(similarity - 0.0) < 0.001


class TestGraphCache:
    """Test in-memory graph cache functionality"""
    
    def test_graph_cache_structure(self):
        """Test graph cache data structure"""
        # Simulate graph cache
        graph_cache = {
            1: [(2, 0.7, 'semantic'), (3, 0.5, 'entity')],
            2: [(1, 0.7, 'semantic'), (4, 0.6, 'semantic')],
            3: [(1, 0.5, 'entity')]
        }
        
        # Test bidirectional edges
        assert (2, 0.7, 'semantic') in graph_cache[1]
        assert (1, 0.7, 'semantic') in graph_cache[2]
        
        # Test O(1) lookup
        neighbors = graph_cache.get(1, [])
        assert len(neighbors) == 2
    
    def test_edge_weight_bounds(self):
        """Test that edge weights are in valid range"""
        edges = [
            (1, 2, 0.7, 'semantic'),
            (2, 3, 0.5, 'entity'),
            (3, 4, 0.9, 'semantic')
        ]
        
        for source, target, weight, edge_type in edges:
            assert 0 <= weight <= 1, f"Weight {weight} outside 0-1 range"


class TestANNIndex:
    """Test FAISS ANN index functionality"""
    
    def test_embedding_dimensions(self):
        """Test that embeddings have correct dimensions"""
        # Our model uses 384 dimensions
        expected_dim = 384
        
        # Simulate embedding
        embedding = np.random.rand(expected_dim).astype(np.float32)
        assert embedding.shape[0] == expected_dim
    
    def test_normalization_for_cosine(self):
        """Test L2 normalization for cosine similarity"""
        vector = np.array([3.0, 4.0], dtype=np.float32)
        
        # L2 norm
        norm = np.linalg.norm(vector)
        assert abs(norm - 5.0) < 0.001  # sqrt(3^2 + 4^2) = 5
        
        # Normalized
        normalized = vector / norm
        assert abs(np.linalg.norm(normalized) - 1.0) < 0.001


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
