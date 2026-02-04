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
- [x] **Time Range Filter** - Filter by date/time range ✅ (Feb 3, 2026 - commit 0645fd2)
- [x] **Entity Type Filter** - Filter by entity type ✅ (Feb 3, 2026 - commit 85aef4f)
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
- [x] **Import/Export** - JSON export for backups ✅ (Feb 3, 2026 - commit c8e5777)
  - Export: Complete (nodes, edges, entities)
  - Import: Not yet implemented
- [ ] **Graph Visualization** - Interactive D3.js graph view
- [ ] **Note Templates** - Predefined note structures
- [ ] **Auto-categorization** - ML-based category suggestions

---

## 📊 Technical Debt


---

## 🔒 Security & Access Control

### Network Access Levels (Implementation Required)

**Current State:** Server runs on `0.0.0.0:5001` with ngrok tunnel - publicly accessible with API key protection only.

**Proposed Implementation:** Three security tiers with explicit user choice:

#### TIER 1: LOCALHOST ONLY (Default - Recommended)
```python
SERVER_HOST=127.0.0.1
ENABLE_NGROK=false
```
**Security:**
- ✅ Accessible only from local machine
- ✅ No network exposure
- ✅ Maximum security for personal use
- ✅ No API key leakage risk

**Limitations:**
- ❌ Cannot access from other devices
- ❌ No MCP integration with claude.ai (requires public access)

**Use Case:** Personal knowledge management on single machine

---

#### TIER 2: LOCAL NETWORK (Optional - Use with Caution)
```python
SERVER_HOST=0.0.0.0  # Listen on all interfaces
ENABLE_NGROK=false
```
**Security:**
- ⚠️  Accessible to any device on your LAN
- ⚠️  Anyone on your WiFi can access your memory graph
- ✅ Not exposed to internet
- ⚠️  API key required but can be sniffed on local network

**Limitations:**
- ❌ No MCP integration with claude.ai
- ⚠️  Trust required for all LAN users

**Use Case:** Multi-device access on trusted home network

---

#### TIER 3: PUBLIC ACCESS (Optional - High Risk)
```python
SERVER_HOST=0.0.0.0
ENABLE_NGROK=true
NGROK_AUTHTOKEN=your_token
API_KEY=strong_random_key  # REQUIRED
```
**Security:**
- ⚠️  Publicly accessible from internet
- ⚠️  API key is only protection
- ⚠️  Memory contents exposed if key compromised
- ⚠️  ngrok URL can be shared/leaked
- ⚠️  Rate limiting recommended

**Limitations:**
- ⚠️  Requires trust in ngrok service
- ⚠️  Potential for unauthorized access
- ⚠️  Data transmitted over internet

**Use Case:** MCP integration with claude.ai, remote access

**REQUIRED Security Measures:**
1. Strong random API key (32+ characters)
2. HTTPS only (ngrok provides this)
3. Rate limiting on endpoints
4. Audit logs for access attempts
5. Regular key rotation

---

### Implementation Tasks

- [ ] **Default to localhost** - Change default SERVER_HOST to 127.0.0.1
- [ ] **Security warnings in .env.example** - Document risks for each tier
- [ ] **README security section** - Clear warnings about network/public access
- [ ] **Startup warnings** - Print security tier to console on server start
- [ ] **Configuration validation** - Reject public access without strong API key

### Documentation Requirements

Each tier must have:
1. Clear security implications
2. Specific use cases
3. Required precautions
4. Migration path between tiers

**Philosophy:** Secure by default, explicit opt-in for exposure, informed user choice.

## 🏢 Phase 4: Enterprise Features (FUTURE - For Production Use)

*Note: Current implementation is optimized for personal use (~200-1000 notes). The following features would be required for enterprise deployment at scale.*

---

## 🆕 ADDITIONAL FEEDBACK - Feb 4, 2026

**Source:** External review for enterprise-level deployment (5K-10K notes)

### Database Operations (Enterprise Only)

#### **Bulk Delete/Cleanup Operations** 
**Request:** Delete edges < weight X, remove orphan nodes, category purging

**Implementation:**
- [ ] Bulk edge deletion by weight threshold
- [ ] Orphan node cleanup (no connections + age filter)
- [ ] Category-based bulk removal
- [ ] Cascade delete with safety checks
- [ ] Transaction rollback on errors

**Why Enterprise Only:** Personal use philosophy is "fade, not delete". Enterprise databases need data management tools.

**Safety:**
- Mandatory backup before bulk operations
- Dry-run mode with preview
- Audit log of deletions
- Undelete buffer (grace period)

---

#### **Graph Versioning (Full State Snapshots)**
**Request:** Rollback entire graph to previous state

**Implementation:**
- [ ] Periodic graph snapshots (nodes + edges + entities)
- [ ] Differential backups (only changes)
- [ ] Point-in-time restore
- [ ] Version tagging (pre-recompute, pre-cleanup)
- [ ] Storage optimization (compression, deduplication)

**Why Enterprise Only:** 
- High disk space cost (10K notes = ~100MB+ per snapshot)
- Personal use has per-note versioning (sufficient)
- Enterprise needs audit trail + disaster recovery

---

#### **Model Hot-Swapping**
**Request:** Switch embedding models without full recompute

**Implementation:**
- [ ] Multiple embedding models side-by-side
- [ ] Lazy recompute (on-access migration)
- [ ] Model performance comparison
- [ ] A/B testing framework
- [ ] Model registry (version, metrics, config)

**Why Enterprise Only:**
- Complex: requires dual-index support
- Personal: one-time model selection sufficient
- Enterprise: continuous optimization, multilingual needs

---

### Retrieval & Monitoring (Applies to Both)

#### **Advanced Search Reranking** ⭐
**Request:** Multi-factor ranking beyond spreading activation

**Implementation:**
- [ ] Combine factors: graph distance + recency + importance + entity overlap
- [ ] Query-specific weights (configurable per search)
- [ ] Learning-to-rank from feedback
- [ ] Result diversity (avoid clustering)
- [ ] Explanation scores (why this result?)

**Priority:** HIGH for both personal + enterprise

---

#### **Retrieval Quality Metrics** ⭐
**Request:** Observability into search degradation

**Implementation:**
- [ ] Query logs (timestamp, query, results, latency)
- [ ] Metrics: hit rate, recall@K, precision, NDCG
- [ ] False positive tracking (entity links)
- [ ] Performance dashboard
- [ ] Alert on degradation thresholds

**Priority:** MEDIUM for personal (research), HIGH for enterprise (SLA)

---

#### **Context Window Management** ⭐⭐⭐
**Request:** Prevent MCP overflow with large graphs

**Implementation:**
- [x] Token counting for results
- [ ] Truncation strategies:
  - Top-K most relevant
  - Summary mode (compress chains)
  - Progressive detail levels
- [ ] `max_tokens` parameter in MCP
- [ ] Smart trimming (keep salient, summarize rest)

**Priority:** CRITICAL for both (blocks scaling beyond 500 notes)

---

### Entity Resolution (Advanced - Enterprise)

#### **Entity Disambiguation & Coreference**
**Request:** "Apple company vs fruit", pronoun resolution, synonym merging

**Implementation:**
- [ ] Entity linking to knowledge base (Wikipedia, DBpedia)
- [ ] Context-based disambiguation (surrounding text)
- [ ] Coreference resolution (pronoun → entity)
- [ ] Synonym/acronym merging (ML → Machine Learning)
- [ ] User feedback loop (confirm/correct)

**Why Enterprise Only:**
- Complex: requires external KB + NLP pipeline
- High maintenance: KB updates, model training
- Personal: manual correction via notes sufficient
- Enterprise: critical for automated knowledge extraction

---

### User Interface (Enterprise)

#### **Connection Approval Workflow**
**Request:** Review auto-generated edges before commit

**Implementation:**
- [ ] Pending edges queue (not persisted until approved)
- [ ] Web UI: approve/reject/defer
- [ ] Confidence scores for auto-approval
- [ ] Batch review mode
- [ ] Smart suggestions (similar to approved edges)

**Priority:** MEDIUM for personal (reduces noise), HIGH for enterprise (quality control)

---

#### **CLI/TUI Interface** ⭐
**Request:** Quick terminal access without web viewer

**Implementation:**
- [ ] Python CLI: `hippograph add/search/stats/delete`
- [ ] Rich TUI for interactive browsing
- [ ] Config file (~/.hippograph/config.yaml)
- [ ] Shell completions (bash/zsh)
- [ ] Piping support (stdin/stdout)

**Priority:** MEDIUM for both (developer experience)

---

### ⚠️  Edge Pruning (Optional - Enterprise Only)
**Status:** Implemented as optional script  
**Commit:** TBD  
**Why NOT recommended for personal use:**
- Weak connections may become important as context grows
- Distant memories are still valuable memories
- Graph structure shows how ideas relate over time
- Irreversible without backup

**When to use (enterprise only):**
- Very large databases (10k+ notes)
- Performance issues from excessive edges
- Regular backups in place
- Acceptable to lose weak historical connections

**Usage:**
```bash
# Analyze current edge distribution
python3 scripts/prune_edges.py data/memory.db --analyze

# Dry run (see what would be removed)
python3 scripts/prune_edges.py data/memory.db --threshold 0.60

# Actually remove (with backup!)
python3 scripts/prune_edges.py data/memory.db --threshold 0.60 --confirm
```

**Files:** `scripts/prune_edges.py`

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
