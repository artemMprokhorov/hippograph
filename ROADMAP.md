# Neural Memory Graph - Development Roadmap

## Current Status: Phase 2 - Performance & Quality (In Progress)

**Last Updated:** January 27, 2026  
**Deployment:** Production-ready implementation  
**Current Stats:** 267 nodes, 17,500+ edges, in-memory graph cache, activation normalized

---

## 🔥 HIGH PRIORITY (Expert Feedback - Jan 27, 2026)

### ✅ 1. ANN Indexing (COMPLETE)
**Status:** Implemented and deployed  
**Commit:** dcb7d32  
**Achievement:** O(log n) similarity search using FAISS IndexFlatIP  
- Replaced linear O(n) scan with approximate nearest neighbor search
- IndexFlatIP for normalized vectors (Inner Product = cosine similarity)
- Auto-rebuild index on server startup
- Fallback to linear scan if ANN disabled
- **Result:** Faster search, especially for 500+ nodes

### ✅ 2. Activation Normalization + Damping (COMPLETE)
**Status:** Implemented and deployed  
**Commit:** 6b4b9e9  
**Problem:** Activation scores grew unbounded (2520+) causing poor ranking  
**Solution:** Normalize to 0-1 range after each spreading iteration
- Scale all activations by max value → max always = 1.0
- Apply decay factor before spreading
- Debug logging for iteration diagnostics
- **Result:** Scores bounded (2.5 vs 2520), stable across iterations

### ✅ 3. Enhanced spaCy Entity Extraction (COMPLETE)
**Status:** Implemented and deployed  
**Commit:** 781f5b3  
**Achievement:** 3-6x more entities detected with confidence scores
- Expanded KNOWN_ENTITIES from 12 to 80+ terms
- Added 60+ tech terms: PyTorch, FAISS, Docker, PostgreSQL, etc
- Added 15+ AI/ML concepts: embeddings, attention, RAG, etc
- Enhanced SPACY_LABEL_MAP with 13 entity types (was 8)
- Confidence scores: 1.0 for known, 0.8 for spaCy NER
- Improved deduplication with normalize_entity()
- Graceful fallback: spaCy → regex on error
**Result:** Test showed 18 entities vs 3-5 before
**Files:** `src/entity_extractor.py`

### ✅ 4. In-Memory Graph Cache (COMPLETE)
**Status:** Implemented  
**Commit:** TBD  
**Problem:** SQLite JOIN bottleneck in graph traversal (Step 2-3 of spreading)
- get_connected_nodes() did SQL JOIN on every hop
- On 10-20K edges, SQLite becomes bottleneck
**Solution:** Load all edges into RAM at startup
- Created graph_cache.py with GraphCache singleton
- Structure: {node_id: [(neighbor_id, weight, edge_type), ...]}
- O(1) dict lookup instead of O(n) SQL JOIN
- Auto-rebuild on server startup alongside ANN index
**Performance:** ~100,000x faster neighbor lookup
- OLD: 10-50ms per SQL JOIN
- NEW: 0.0002ms per dict lookup
**Result:** Spreading activation fully in-memory, SQLite only for cold storage
**Files:** `src/graph_cache.py`, `src/database.py`, `src/graph_engine.py`, `src/server.py`

### ✅ 5. Tests Infrastructure (pytest) (COMPLETE)
**Status:** Implemented and deployed  
**Commit:** Various commits in Jan 28, 2026  
**Achievement:** Comprehensive test suite with 17 tests
- Unit tests for graph_engine.py (spreading activation, ANN, graph cache)
- Integration tests for MCP tools (search, CRUD, performance)
- Test fixtures with sample graph data
- pytest configuration with markers (unit, integration, slow)
- **Result:** All 17 tests passing, test coverage for core functionality
**Files:** `tests/test_graph_engine.py`, `tests/test_integration.py`

### ✅ 6. Semantic Links Bug Fix (COMPLETE - Feb 3, 2026)
**Status:** Critical bug discovered and fixed  
**Commit:** d4f0b90  
**Problem:** New notes weren't getting semantic links after note #201
- add_note_with_links() used O(n) linear scan for both duplicate check and semantic link creation
- On 325+ notes, this became too slow
- New notes got entity links but ZERO semantic links
**Solution:** Replace linear scan with ANN index search
- Duplicate check: ann_index.search(k=5, min_similarity=DUPLICATE_THRESHOLD)
- Semantic links: ann_index.search(k=MAX_SEMANTIC_LINKS*2, min_similarity=SIMILARITY_THRESHOLD)
- Fallback to linear scan if ANN disabled
**Result:** O(log n) performance, new notes now get semantic links automatically
**Files:** `src/graph_engine.py`

### ✅ 7. Filtered Search by Category (COMPLETE - Feb 3, 2026)
**Status:** Implemented and deployed  
**Commit:** e8168ba  
**Achievement:** Add category filtering to search_memory tool
- Added category_filter parameter to search_with_activation()
- Filter applied after spreading activation but before limit
- MCP tool updated with category parameter
- Example: search_memory(query="bug fix", category="breakthrough")
**Result:** Can now search within specific categories
**Files:** `src/graph_engine.py`, `src/mcp_sse_handler.py`

---

## 🎯 MEDIUM PRIORITY

### 6. Incremental Updates
- Update existing nodes without full rebuild
- Add single vectors to ANN index without recreation

### 7. Edge Pruning
- Remove weak semantic connections (similarity < threshold)
- Optimize graph structure for better spreading

### 8. Graph Metrics
- PageRank for node importance
- Community detection (Louvain algorithm)
- Centrality measures

### 9. Search Quality Metrics
- Recall@k measurement
- Precision tracking
- User feedback collection

### 10. LLM-based Entity Extraction (Optional)
**Note:** Moved from HIGH to MEDIUM priority  
**Reason:** Massive overhead for personal use case
- Ollama requires 3-7GB Docker image
- 4-12GB RAM constant usage
- 2-5 seconds per note (vs 100ms with spaCy)
- For 200-500 notes, spaCy is pragmatic choice
**Alternative:** Remote Claude API for critical cases only

---

### Search Enhancement
- [x] **Filtered Search** - Search by category ✅ (Feb 3, 2026 - commit e8168ba)
- [ ] **Time Range Filter** - Filter by date/time range
- [ ] **Entity Type Filter** - Filter by entity type
- [ ] **Saved Searches** - Store frequent search patterns
- [ ] **Search History** - Track and replay past searches

### Entity Extraction
- [ ] **LLM-based Extraction** - More accurate entity detection
- [ ] **Custom Entity Types** - User-defined entity categories
- [ ] **Entity Relationships** - Extract relationships between entities
- [ ] **Multi-language Support** - Non-English entity extraction

### Performance & Scale
- [ ] **Batch Operations** - Bulk add/update/delete
- [ ] **Incremental Embeddings** - Compute embeddings on-demand
- [ ] **Caching Layer** - Redis for frequent queries
- [ ] **Horizontal Scaling** - Multi-instance deployment

### User Experience
- [ ] **Graph Visualization** - Interactive D3.js graph view
- [ ] **Import/Export** - JSON, Markdown, CSV formats
- [ ] **Note Templates** - Predefined note structures
- [ ] **Auto-categorization** - ML-based category suggestions

---

## 📊 Technical Debt


---

## 🏢 Phase 4: Enterprise Features (FUTURE - For Production Use)

*Note: Current implementation is optimized for personal use (~200-1000 notes). The following features would be required for enterprise deployment at scale.*

### Graph Analytics & Intelligence
- [ ] **Centrality Analysis** - Identify key nodes using PageRank, betweenness centrality
- [ ] **Community Detection** - Automatic clustering of related knowledge domains
- [ ] **Path Scoring** - Weighted pathfinding between concepts
- [ ] **Graph Metrics Dashboard** - Network density, diameter, clustering coefficient
- [ ] **Anomaly Detection** - Identify orphaned or over-connected nodes

**Why:** At enterprise scale (10k+ notes), understanding network structure becomes critical for knowledge discovery and organization.

### Memory Hierarchy & Lifecycle
- [ ] **Short-term Memory** - Session-based working memory (24h retention)
- [ ] **Long-term Memory** - Permanent storage with reinforcement learning
- [ ] **Working Memory Cache** - Recently accessed nodes in fast storage
- [ ] **Memory Consolidation** - Automated archival of stale content
- [ ] **Access-based Promotion** - Frequently used short-term → long-term

**Why:** Mimics human memory architecture; improves performance by tiering storage based on access patterns.

### Architectural Improvements
- [ ] **Layer Separation** - Clean boundaries between ingestion/storage/retrieval/reasoning
- [ ] **Service-Oriented Architecture** - Separate microservices for each layer
- [ ] **Event-Driven Processing** - Async message queues for note processing
- [ ] **CQRS Pattern** - Separate read/write models for scaling
- [ ] **API Gateway** - Unified entry point with rate limiting, auth

**Why:** Current architecture mixes concerns for simplicity; enterprise needs clean separation for maintainability and scaling.

### Security & Compliance
- [ ] **Multi-tenancy** - Isolated memory spaces per user/organization
- [ ] **Role-based Access Control** - Granular permissions on notes/categories
- [ ] **Audit Logging** - Track all changes with timestamp/user
- [ ] **Encryption at Rest** - Database-level encryption
- [ ] **SOC 2 Compliance** - Security controls and audits

**Why:** Enterprise data governance and regulatory requirements.

### Observability & Operations
- [ ] **Distributed Tracing** - Request flow across services
- [ ] **Prometheus Metrics** - Query latency, throughput, cache hit rates
- [ ] **Structured Logging** - Centralized log aggregation (ELK stack)
- [ ] **Health Checks** - Deep health monitoring beyond simple ping
- [ ] **Auto-scaling** - Horizontal pod autoscaling based on load

**Why:** Production operations require deep visibility into system behavior.

### Performance at Scale
- [ ] **Vector Index Optimization** - HNSW/IVF-PQ for large-scale similarity search
- [ ] **Read Replicas** - Database replication for read-heavy workloads
- [ ] **Connection Pooling** - Efficient database connection management
- [ ] **Materialized Views** - Pre-computed graph metrics
- [ ] **CDN for Static Assets** - Distributed caching

**Why:** Current SQLite + in-memory FAISS works for personal use but won't scale to millions of notes.

### Estimated Effort
- **Graph Analytics**: 2-3 weeks
- **Memory Hierarchy**: 3-4 weeks
- **Architecture Refactor**: 4-6 weeks
- **Security/Compliance**: 2-3 weeks
- **Observability**: 1-2 weeks
- **Performance Optimization**: 2-3 weeks

**Total: ~3-4 months** for enterprise-ready production deployment


- [ ] Migrate from Flask development server to production WSGI (Gunicorn)
- [ ] Add comprehensive error handling and retry logic
- [ ] Implement rate limiting for MCP endpoints
- [ ] Add structured logging with log levels
- [ ] Security audit for production deployment
- [ ] Performance profiling and optimization
- [ ] Automated testing suite (unit + integration)
- [ ] CI/CD pipeline

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

**Code:**
- Entity extraction methods (spaCy improvements, custom NER)
- Graph algorithms (spreading activation, clustering)
- Performance optimizations (caching, batching)
- Security hardening (rate limiting, authentication)

**Documentation:**
- Usage examples and tutorials
- Architecture deep-dives
- API client libraries (Python, TypeScript)
- Video walkthroughs

**Testing:**
- Unit tests for core components
- Integration tests for MCP protocol
- Load testing for scaling
- Security testing

See [Contributing Guidelines](CONTRIBUTING.md) for details.

---

## 📝 Version History

### v2.0.0 (January 2026)
- Graph-based architecture with nodes, edges, entities
- MCP protocol integration
- Temporal decay for recency weighting
- Importance scoring (critical/normal/low)
- Duplicate detection
- spaCy NER entity extraction

### v1.0.0 (December 2025)
- Initial linear memory implementation
- Semantic search with embeddings
- Basic CRUD operations
- Docker deployment

### v0.1.0 (December 2025)
- Proof of concept
- SQLite storage
- Sentence transformers

---

## 📜 License

MIT License - see [LICENSE](LICENSE)

---

**Questions or suggestions?** Open an issue or discussion on GitHub!
