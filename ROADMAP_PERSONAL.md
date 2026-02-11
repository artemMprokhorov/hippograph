# HippoGraph - Personal Use Roadmap

**Target:** Single user, 200-2,000 notes, personal knowledge management

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
- [x] REST API endpoints (`/api/graph-data`, `/api/node/<id>`)
- [x] Full graph loading (all 593 nodes via REST, not search)
- [x] Click-to-detail (load full note content on demand)
- [x] Performance cap (5000 links max for browser)
- [x] Timeline animation with autoplay

**Success Metric:** ✅ Can visually explore full 593-node, 48K-edge graph
**URL:** http://localhost:5002  
**Files:** `web/index.html`, `nginx.conf`, `src/server.py`

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
**Status:** Blend scoring implemented and deployed, formal testing remaining  
**Goal:** Measure and improve search relevance

**Root Cause Found (Feb 6):**
Hub nodes (project-status, milestones with many entities) accumulate activation
from many neighbors via spreading activation, dominating results regardless of
query semantics. Query "spaCy NER" returned 0 relevant results in top-5 despite
sim=0.71 for correct note.

**Blend Scoring Implemented (Feb 11):**
`final_score = α × semantic_similarity + (1-α) × spreading_activation`
- Default α=0.6 (semantic-heavy)
- Spreading activation normalized to 0-1 range before blending
- All scores now ≤1.0 (previously 2.5+ from raw activation)
- MCP-verified: relevant results for targeted queries

**Tasks:**
- [x] Identify root cause: hub dominance in spreading activation
- [x] Tune importance boost (critical 2.0→1.5, access boost 50%→20%)
- [x] Implement blend scoring: final = α×semantic + (1-α)×spreading (α=0.6 default)
- [x] Deploy and verify through MCP (scores ≤1.0, relevant results)
- [ ] Add BLEND_ALPHA env var for tuning
- [ ] Create test dataset (queries + expected results)
- [ ] Measure precision@k before/after blend
- [ ] Benchmark latency (target: <500ms for 2000 notes)

**Success Metric:** >80% precision@5 on test queries  
**Estimated:** 1-2 hours remaining

---

### 6. Context Window Protection ✅ COMPLETE
**Completed:** Feb 6, 2026  
**Problem:** MCP returns full activation paths → Claude context overflow at ~500+ nodes

**Implemented:**
- [x] `max_results` parameter (hard limit, default: 10, Top-K truncation)
- [x] `detail_mode` parameter ("brief" first line + metadata / "full" complete content)
- [x] `estimate_tokens` (~4 chars per token rough estimation)
- [x] Metadata with `truncated` flag
- [x] `search_with_activation_protected()` in graph_engine.py
- [x] Brief mode: first line + metadata (chars, lines, importance, emotional context)
- [x] Fixed `total_activated`: shows real activated count before truncation
- [x] Fixed `truncated` logic: `total_activated > returned` (was `limit > max_results`)

**Success Metric:** ✅ Brief mode ~224 tokens for 3 results vs ~1500 for full mode
**Files:** `src/graph_engine.py`, `src/mcp_sse_handler.py`

---

### 7. CLI/TUI Interface ⏳ PLANNED
**Status:** Not started  
**Problem:** Web viewer + MCP only, no quick terminal access

**Tasks:**
- [ ] Simple Python CLI: `hippograph add/search/stats`
- [ ] Uses same MCP endpoint (no new backend code)
- [ ] Optional: Rich TUI for interactive browsing

**Estimated:** 2-3 hours

---

## 🎯 MEDIUM PRIORITY - Quality of Life

### Retrieval Quality Monitoring
- [ ] Query logs (timestamp, query, results count, top activations)
- [ ] Basic metrics: hit rate, avg results, latency
- [ ] CSV export for analysis

### Connection Quality (Natural Patterns)
- [ ] Track activation frequency per edge
- [ ] Automatic weight decay for unused connections
- [ ] Boost frequently co-activated edges
- [ ] "Dormant connection" state (very low weight, not deleted)

### Batch Operations
- [ ] Bulk add notes from JSON/markdown
- [ ] Bulk update categories/importance

### Saved Searches & Note Templates
- [ ] Save frequent search queries with names
- [ ] Session summary template
- [ ] Breakthrough insight template

---

## ❌ OUT OF SCOPE - Personal Use

**Moved to ROADMAP_ENTERPRISE.md:**
- Bulk delete operations
- Graph-wide rollback
- Context window trimming by deletion
- Smart chain trimming by removal
- Multi-tenancy, user auth, permissions
- GraphSAGE / Neo4j indices
- PageRank normalization
- Horizontal scaling / sharding

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

## 📊 Current Status (Feb 11, 2026)

- **Nodes:** 603+
- **Edges:** 51,582
- **Entities:** 1,017
- **MCP Tools:** 10/10 verified
- **Graph Viewer:** REST API loading all nodes
- **Completed:** 5/7 HIGH PRIORITY
- **In Progress:** Retrieval Quality (#5) — blend scoring deployed, formal testing remaining
- **DeepWiki:** https://deepwiki.com/artemMprokhorov/hippograph

---

**Last Updated:** Feb 11, 2026
