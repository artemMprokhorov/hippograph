# HippoGraph - Personal Use Roadmap

**Target:** Single user, 200-2,000 notes, personal knowledge management + consciousness research

**Philosophy:** Keep all memories. Natural patterns over forced deletion. Quality over scale.

---

## 🎯 HIGH PRIORITY - Critical for Personal Use

### 1. Entity Extraction Quality ✅ COMPLETE
**Completed:** Feb 3, 2026  
**Goal:** Better signal-to-noise ratio for personal memory context

**Implemented:**
- [x] Filter generic words (GENERIC_STOPWORDS set)
- [x] Filter standalone numbers (isdigit() check)
- [x] MIN_ENTITY_LENGTH = 2 (skip single chars)
- [x] Fixed entity type mappings (ANN: tech, LLM: concept)
- [x] Skip NUMBER types from spaCy (CARDINAL/ORDINAL)

**Success Metric:** ✅ Noise significantly reduced
**Files:** `src/entity_extractor.py`

---

### 2. Note Versioning ✅ COMPLETE
**Completed:** Feb 3-4, 2026  
**Goal:** Recover from accidental overwrites

**Implemented:**
- [x] Auto-save version before each update
- [x] Store last 5 versions (configurable)
- [x] View version history (get_note_history MCP tool)
- [x] Restore from previous version (restore_note_version MCP tool)
- [x] Database migration: note_versions table

**Success Metric:** ✅ Can recover accidentally overwritten notes
**Files:** `src/database.py`, `src/mcp_sse_handler.py`

---

### 3. Graph Visualization ✅ COMPLETE
**Completed:** Feb 5, 2026  
**Goal:** Visual exploration of memory connections

**Implemented:**
- [x] D3.js force-directed layout viewer
- [x] Interactive node exploration
- [x] Filter by category, entity type, search
- [x] Real-time stats (nodes, edges, entities)
- [x] Refresh button for live updates

**Success Metric:** ✅ Can visually explore 591-node graph
**URL:** http://192.168.0.212:5002  
**Files:** `web/index.html`, `nginx.conf`

---

### 4. Batch Knowledge Import ✅ COMPLETE
**Completed:** Feb 5, 2026  
**Goal:** Import large skill sets without context window limits

**Implemented:**
- [x] Direct SQLite import script (scripts/add_skills.py)
- [x] JSON format for bulk skills
- [x] Duplicate detection by skill name
- [x] Category support (security-critical, development, ml-architecture)
- [x] SKILL.md → JSON converter (scripts/convert_to_json.py)

**Success Metric:** ✅ Imported 196 skills (37 duplicates skipped)
**Files:** `scripts/add_skills.py`, `scripts/convert_to_json.py`, `scripts/README.md`

---

### 5. Retrieval Quality Testing ⏳ IN PROGRESS
**Status:** Not started  
**Goal:** Measure and improve search relevance

**Tasks:**
- [ ] Create test dataset (queries + expected results)
- [ ] Measure precision@k and recall@k
- [ ] Benchmark latency (target: <500ms for 2000 notes)
- [ ] Establish baseline before optimizations

**Success Metric:** >80% precision@5 on test queries  
**Estimated:** 2-3 hours

---

### 6. Context Window Protection ⭐⭐⭐ CRITICAL
**Status:** Partially implemented (25% complete)  
**Problem:** MCP returns full activation paths → Claude context overflow at ~500+ nodes

**Current State:**
- [x] Token counting in search results

**Still Needed:**
- [ ] MCP parameter: `max_tokens` (default: 4000)
- [ ] Top-K truncation (return only N most activated nodes)
- [ ] Summary mode (compress long content)
- [ ] Progressive detail (brief first, full on request)

**Philosophy:** ✅ Technical constraint, not memory deletion  
**Priority:** CRITICAL - system breaks without this as graph grows  
**Estimated:** 3-4 hours

---

### 7. CLI/TUI Interface ⏳ PLANNED
**Status:** Not started  
**Problem:** Web viewer + MCP only, no quick terminal access

**Tasks:**
- [ ] Simple Python CLI: `hippograph add/search/stats`
- [ ] Uses same MCP endpoint (no new backend code)
- [ ] Optional: Rich TUI for interactive browsing

**Philosophy:** ✅ Accessibility improvement  
**Estimated:** 2-3 hours

---

## 🎯 MEDIUM PRIORITY - Quality of Life

### Retrieval Quality Monitoring
**Goal:** Observability for search performance

**Tasks:**
- [ ] Query logs (timestamp, query, results count, top activations)
- [ ] Basic metrics: hit rate, avg results, latency
- [ ] CSV export for analysis
- [ ] Optional: Simple dashboard in web viewer

**Philosophy:** ✅ Observability without changing core behavior  
**Estimated:** 2-3 hours

---

### Connection Quality (Natural Patterns)
**Goal:** Strengthen good connections, weaken unused ones (like real memory)

**Tasks:**
- [ ] Track activation frequency per edge
- [ ] Automatic weight decay for unused connections
- [ ] Boost frequently co-activated edges
- [ ] "Dormant connection" state (very low weight, not deleted)
- [ ] Confidence scores on edges (0.0-1.0)

**Philosophy:** ✅ Natural strengthening/weakening through use, NO deletion  
**Estimated:** 4-5 hours

---

### Batch Operations
- [ ] Bulk add notes from JSON/markdown
- [ ] Bulk update categories/importance

**Note:** Bulk DELETE moved to ROADMAP_ENTERPRISE (not personal use)

---

### Saved Searches
- [ ] Save frequent search queries with names
- [ ] Quick access to saved searches

---

### Note Templates
- [ ] Session summary template
- [ ] Breakthrough insight template

---

## ❌ OUT OF SCOPE - Personal Use

**These belong in ROADMAP_ENTERPRISE:**

### Moved to Enterprise
- Bulk delete operations (delete edges < weight X, orphan nodes)
- Graph-wide rollback (undo yesterday)
- Context window trimming by deletion (use Top-K instead)
- Smart chain trimming by removal (use summarization instead)
- Weak connection deletion (use weight decay instead)

### Never Implement
- Multi-tenancy, user auth, permissions
- GraphSAGE / Neo4j indices (overkill for <10k nodes)
- PageRank normalization (current damping sufficient)
- Horizontal scaling / sharding
- Rate limiting

---

## 🤝 Development Philosophy

1. **Keep All Memories** - No deletion. Pruning is enterprise-only.
2. **Natural Memory Patterns** - Fade/decay like real memory, not database DELETE.
3. **Secure by Default** - Localhost unless explicitly opened.
4. **Quality over Scale** - 2000 notes well-organized > 10k poorly organized.
5. **Practical over Perfect** - Working solution > theoretically optimal.
6. **Iterative** - Ship, use, learn, improve.
7. **Ethical Design** - Don't implement operations harmful to memory integrity.

---

## 📊 Current Status (Feb 5, 2026)

- **Nodes:** 591 (189 development skills, 14 security-critical)
- **Edges:** 47,722 (45,226 entity, 2,496 semantic)
- **Entities:** 982
- **Commits:** 71bd7ce (latest: convert_to_json.py documentation)
- **Next Priority:** Context Window Protection (#6) - CRITICAL

---

**Last Updated:** Feb 5, 2026