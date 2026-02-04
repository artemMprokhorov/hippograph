# HippoGraph - Personal Use Roadmap

**Target:** Single user, 200-2,000 notes, personal knowledge management + consciousness research

**Philosophy:** Practical improvements over theoretical perfection. Keep all memories, focus on quality over scale.

---

## 🎯 HIGH PRIORITY - Personal Use Blockers

### 1. Entity Extraction Quality ✅ COMPLETE
**Completed:** Feb 3, 2026
**Goal:** Better signal-to-noise ratio for personal memory context

**Implemented:**
- [x] Filter out generic/common words (GENERIC_STOPWORDS set)
- [x] Filter standalone numbers (isdigit() check)
- [x] MIN_ENTITY_LENGTH = 2 (skip single chars)
- [x] Fixed entity type mappings (ANN: tech, LLM: concept)
- [x] Skip NUMBER types from spaCy (CARDINAL/ORDINAL)

**Result:** Noise significantly reduced - test showed filtering of "first", "second", "thing", "stuff", digits 1-42
**Files:** `src/entity_extractor.py`

---

### 2. Note Versioning (Simple) ✅ COMPLETE
**Completed:** Feb 3-4, 2026
**Goal:** Basic version history for important notes

**Implemented:**
- [x] Timestamp-based snapshots on update (auto-save before each update)
- [x] Store last N versions (default: 5, configurable in database)
- [x] View version history for a note (get_note_history MCP tool)
- [x] Restore from previous version (restore_note_version MCP tool)
- [x] Database migration: note_versions table with full metadata

**Success Metric:** Can recover accidentally overwritten notes ✅ VERIFIED
**Files:** `src/database.py`, `src/mcp_sse_handler.py`, migration script

---

### 3. Security Tiers Implementation ✅ Spec Complete
**Current Issue:** Server runs on 0.0.0.0 with public ngrok by default
**Goal:** Secure by default, opt-in for exposure

**Tasks:**
- [ ] Change default SERVER_HOST to 127.0.0.1
- [ ] Add .env.example with security warnings
- [ ] README security section
- [ ] Startup console warning about current security tier
- [ ] Validate strong API key if public access enabled

**Success Metric:** New users start with localhost-only
**Estimated:** 1-2 hours

---

### 4. Graph Visualization Web Service
**Current Issue:** No easy way to see memory graph structure
**Goal:** Simple web UI to explore connections

**Tasks:**
- [ ] Standalone HTML + D3.js viewer
- [ ] Fetch graph data from MCP endpoints
- [ ] Interactive node exploration
- [ ] Filter by category, entity type, time

**Success Metric:** Can visually explore memory graph in browser
**Estimated:** 3-4 hours

---

### 5. Retrieval Quality Testing
**Current Issue:** No systematic testing of search accuracy
**Goal:** Measure and improve search relevance

**Tasks:**
- [ ] Test dataset of queries + expected results
- [ ] Measure precision@k and recall@k
- [ ] Benchmark latency (target: <500ms for 2000 notes)

**Success Metric:** >80% precision@5 on test queries
**Estimated:** 2-3 hours

---

## 🎯 MEDIUM PRIORITY - Quality of Life

### Batch Operations
- [ ] Bulk add notes from JSON/markdown
- [ ] Bulk update categories/importance
- [ ] Bulk delete with confirmation

### Saved Searches
- [ ] Save frequent search queries with names
- [ ] Quick access to saved searches

### Note Templates
- [ ] Session summary template
- [ ] Breakthrough insight template

---

## ❌ OUT OF SCOPE - Personal Use

NOT needed for personal knowledge management:

- Multi-tenancy, user auth, permissions
- GraphSAGE / Neo4j indices (overkill for <10k nodes)
- PageRank normalization (current damping works for <2k notes)
- Active auto-forgetting (philosophy: keep all memories!)
- Horizontal scaling / sharding
- Rate limiting (single user doesn't need)

---

## 🤝 Development Philosophy

1. **Keep All Memories** - No auto-deletion, pruning is optional
2. **Secure by Default** - Localhost unless explicitly opened
3. **Quality over Scale** - 2000 notes well-organized > 10k poorly organized
4. **Practical over Perfect** - Working solution > theoretically optimal
5. **Iterative** - Ship, use, learn, improve

---

**Last Updated:** Feb 3, 2026
