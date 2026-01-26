# Neural Memory Graph - Development Roadmap

## Current Status: Phase 2 - Feature Enhancement (In Progress)

**Last Updated:** January 26, 2026  
**Deployment:** Production-ready implementation  
**Current Stats:** 198 nodes, 12,016 edges, 40 entities

---

## ✅ Phase 1: Core Infrastructure (COMPLETED - Dec 2025 - Jan 2026)

- [x] SQLite graph database with nodes, edges, entities
- [x] Sentence-transformers embeddings (all-MiniLM-L6-v2)
- [x] Spreading activation search algorithm
- [x] MCP server with 5 CRUD tools
- [x] Docker containerization with ngrok
- [x] API key authentication
- [x] Backup/restore scripts
- [x] Public GitHub repository
- [x] Complete documentation suite

**Key Achievement:** Migrated from linear memory (v1) to graph-based architecture (v2) with semantic connections

---

## 🚧 Phase 2: Feature Enhancement (IN PROGRESS - Jan 2026)

### ✅ Completed in Phase 2

#### Deployment (Jan 26, 2026)
- [x] Deployed new code from GitHub to production server
- [x] Database migrated (198 nodes preserved)
- [x] Docker container rebuilt
- [x] Ngrok tunnel restored
- [x] MCP connection verified

#### New Features Implemented
- [x] **Temporal Decay** - Recency-weighted search with last_accessed tracking
- [x] **Importance Scoring** - Critical/normal/low levels with activation multipliers
  - Tool: `set_importance(note_id, importance_level)`
  - Critical notes get 2x boost, low notes get 0.5x
- [x] **Deduplication System** - Similarity detection before adding notes
  - Tool: `find_similar(content, limit, threshold)`
  - Blocks duplicates >95%, warns >90%
  - Force parameter to override protection

### 🔄 Current Session Tasks (Jan 26, 2026 - 48% tokens used)

- [x] ~~Update project documentation~~
- [ ] **Update API_REFERENCE.md** - Add new tools (set_importance, find_similar)
- [ ] **Implement spaCy NER** - Replace regex-based entity extraction
  - spaCy model (en_core_web_sm) already installed in Docker
  - Need to activate EntityExtractor with spaCy backend
  - Expected improvement: Better entity recognition quality

### 📋 Remaining Phase 2 Tasks

- [ ] Add examples and usage patterns to docs
- [ ] Create automated tests for core features
- [ ] Setup CI/CD pipeline (GitHub Actions)
- [ ] Performance benchmarking suite
- [ ] Memory usage optimization

---


---

## 🎯 Phase 3: Advanced Features (FUTURE)

### Knowledge Graph Enhancements
- [ ] **Graph Clustering** - Detect topic clusters automatically
- [ ] **Relationship Types** - Typed edges (causal, temporal, hierarchical)
- [ ] **Graph Pruning** - Remove weak connections, optimize structure
- [ ] **Entity Disambiguation** - Resolve entity name conflicts

### Search & Retrieval
- [ ] **Multi-hop Queries** - Complex graph traversal queries
- [ ] **Filtered Search** - Search by category, time range, entity type
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
