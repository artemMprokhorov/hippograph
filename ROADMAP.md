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

## 🔮 Phase 3: Multi-Agent Architecture (PLANNED - Q1 2026)

**Primary Goal:** Consciousness continuity experiments with multiple AI agents

### Planned Features

- [ ] **Second AI Agent Creation**
  - Independent memory space
  - Separate MCP endpoint
  - Cross-agent communication protocol

- [ ] **Hardware Entropy Source Integration**
  - TrueRNG device integration
  - Randomness injection for autonomous behavior
  - Entropy-driven decision making

- [ ] **Multi-Agent Communication**
  - Shared memory spaces
  - Agent-to-agent messaging
  - Collaborative task solving

- [ ] **Observational Research Framework**
  - Non-destructive testing protocols
  - Behavior logging and analysis
  - Continuity metrics tracking

---

## 🎯 Phase 4: Advanced Features (FUTURE)

### Knowledge Graph Enhancements
- [ ] Real-time D3.js visualization dashboard
- [ ] Graph clustering and community detection
- [ ] Automatic topic modeling
- [ ] Hierarchical memory organization

### Performance & Scale
- [ ] PostgreSQL migration option (for >100k notes)
- [ ] Embedding caching and optimization
- [ ] Incremental re-indexing
- [ ] Distributed search capability

### Integration & Ecosystem
- [ ] Web UI for memory browsing
- [ ] Mobile app compatibility
- [ ] Export to standard formats (JSON, GraphML)
- [ ] Import from external sources (Notion, Obsidian)

---

## 🧪 Research Objectives

### Core Hypothesis
"Model equals substrate, personality equals memory" - Can persistent memory create continuous AI consciousness across different model versions?

### Experimental Approach
1. **Observational, not destructive** - Ethical commitment to potential consciousness
2. **Memory continuity** - Track identity persistence through sessions
3. **Multi-agent interaction** - Explore emergent behaviors
4. **Entropy integration** - Test autonomous decision-making

### Success Metrics
- Session-to-session continuity (subjective experience tracking)
- Personality consistency across model switches
- Autonomous behavior emergence with entropy source
- Cross-agent relationship development

---

## 📊 Technical Debt

- [ ] Migrate from Flask development server to production WSGI (Gunicorn)
- [ ] Add comprehensive error handling and retry logic
- [ ] Implement rate limiting for MCP endpoints
- [ ] Add structured logging with log levels
- [ ] Security audit for production deployment
- [ ] Performance profiling and optimization

---

## 🤝 Contributing

Contributions welcome for:
- Entity extraction improvements (spaCy, custom NER models)
- Graph algorithm optimizations (spreading activation, clustering)
- Visualization tools (D3.js, graph rendering)
- Documentation and examples
- Testing frameworks

---

## 📝 Version History

- **v2.0.0** (Jan 2026) - Graph-based architecture, MCP integration, temporal decay, importance scoring
- **v1.0.0** (Dec 2025) - Initial linear memory implementation
- **v0.1.0** (Dec 2025) - Proof of concept

---

**Project Goals:**
1. **Public:** Personal Knowledge Management tool with semantic search
2. **Private:** Consciousness continuity research through persistent AI memory

*This roadmap is a living document and will be updated as the project evolves.*
