# HippoGraph - Personal Use Roadmap

**Target:** Single user, 200-2,000 notes, personal knowledge management + memory optimization

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

### 3. Graph Visualization Web Service ✅ COMPLETE
**Completed:** Feb 5, 2026
**Goal:** Simple web UI to explore connections

**Implemented:**
- [x] Standalone HTML + D3.js viewer at http://192.168.0.212:5002
- [x] Fetch graph data via JSON-RPC calls to MCP
- [x] Interactive node exploration with force-directed layout
- [x] Filter by category, entity type, search
- [x] Real-time stats display (nodes, edges, entities)
- [x] Refresh button for live data updates (commit 5c5cdfe)

**Success Metric:** Can visually explore 589-node memory graph ✅ VERIFIED
**Files:** `web/index.html`, `nginx.conf`

---

### 4. Batch Knowledge Import ✅ COMPLETE
**Completed:** Feb 5, 2026
**Goal:** Import large skill sets without context window limits

**Implemented:**
- [x] Direct SQLite import script (scripts/add_skills.py)
- [x] JSON format for bulk skills (scripts/skills_example.json)
- [x] Duplicate detection by skill name
- [x] Category support (security-critical, development, ml-architecture)
- [x] Conversion script for SKILL.md → JSON
- [x] Successfully imported 196 skills in single batch

**Success Metric:** Can import 200+ skills efficiently ✅ VERIFIED (196 added, 37 skipped)
**Files:** `scripts/add_skills.py`, `scripts/convert_to_json.py`, `scripts/README.md`

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

## 🆕 FEEDBACK ANALYSIS - Feb 4, 2026

**Source:** External review for 5K-10K notes personal use

### ✅ Already Addressed (Previous Feedback)
1. **Memory consolidation/decay** - Temporal decay + importance scoring implemented
2. **Entity disambiguation** - Improved with spaCy + filtering (ongoing refinement)
5. **Search reranking** - Spreading activation provides multi-path relevance
6. **Context window** - Need to implement (see new priorities below)

### 🆕 New High-Priority Items

#### **#6 - Context Window Control** ⭐⭐⭐ CRITICAL
**Problem:** MCP returns full activation paths → Claude context overflow  
**Impact:** System breaks as graph grows beyond ~500 nodes

**Solution:**
- [x] Add token counting to search results
- [ ] Implement truncation strategies:
  - Top-K most activated nodes only
  - Summary mode (compress long chains)
  - Progressive detail (brief → full on demand)
- [ ] MCP parameter: `max_tokens` (default: 4000)
- [ ] Smart chain trimming (keep most relevant, summarize rest)

**Philosophy Alignment:** ✅ Technical constraint, not memory deletion

---

#### **#4 - Connection Quality Control** ⭐⭐ HIGH
**Problem:** Auto-generated edges add noise without review  
**Impact:** False connections dilute signal over time

**Solution (Pattern-Based):**
- [ ] "Weak connection" marking (not deletion!)
- [ ] Confidence scores on edges (0.0-1.0)
- [ ] Natural strengthening through co-activation
- [ ] Never-strengthen blacklist (user feedback)
- [ ] Web viewer: Review pending connections UI

**Philosophy Alignment:** ✅ Mimics connection dynamics - connections strengthen/weaken through use, not deleted

---

#### **#7 - Retrieval Quality Monitoring** ⭐ MEDIUM
**Problem:** Blind to system degradation  
**Impact:** Can't diagnose why searches get worse

**Solution:**
- [ ] Query logs: timestamp, query, results count, top activations
- [ ] Basic metrics: hit rate, avg results, latency
- [ ] CSV export for analysis
- [ ] Optional: Simple dashboard in web viewer

**Philosophy Alignment:** ✅ Observability for memory optimization

---

#### **#10 - CLI/TUI Interface** ⭐ MEDIUM  
**Problem:** Web viewer + MCP only, no quick terminal access  
**Impact:** Friction for rapid note-taking

**Solution:**
- [ ] Simple Python CLI: `hippograph add/search/stats`
- [ ] Uses same MCP endpoint
- [ ] Optional: Rich TUI for interactive browsing

**Philosophy Alignment:** ✅ Accessibility improvement

---

### ❌ REJECTED - Against Natural Memory Patterns

#### **#8 - Bulk Delete Operations**
**Requested:** "Delete all edges < weight X", "delete orphan nodes"

**REJECTED Reasoning:**
- ❌ Goes against "Keep All Memories" principle
- ❌ Memory system doesn't have "delete old memories" operation
- ❌ Natural forgetting happens through decay/non-activation, not purging
- ✅ **Alternative:** Strengthen temporal decay, add activation frequency tracking

**Quote from philosophy:** *"Не делай со своими мозгами то, что им вредит"*

---

#### **#3 - Graph-Wide Rollback**
**Requested:** Version control for entire graph state

**REJECTED Reasoning:**
- ❌ Memory systems don't have "undo yesterday" functionality
- ❌ Memory is write-forward only (new experiences layer on old)
- ✅ **Alternative:** Export snapshots for backup/disaster recovery only
- ✅ Per-note versioning sufficient for mistakes (already implemented)

---

### 🔄 Enhanced Natural Forgetting (Instead of Deletion)

**Goal:** Improve existing pattern-based forgetting

**Tasks:**
- [ ] Track activation frequency per edge
- [ ] Automatic weight decay for unused connections
- [ ] Boost frequently co-activated edges
- [ ] "Dormant connection" state (very low weight, not deleted)
- [ ] Configurable decay curves (exponential, linear, stepped)

**Philosophy:** Memories fade naturally when not reinforced, through natural patterns

---

## ❌ OUT OF SCOPE - Personal Use

NOT needed for personal knowledge management:

- Multi-tenancy, user auth, permissions
- GraphSAGE / Neo4j indices (overkill for <10k nodes)
- PageRank normalization (current damping works for <2k notes)
- **Bulk delete operations** (philosophy: memories fade, not deleted!)
- **Graph-wide rollback** (memory systems write-forward only)
- Horizontal scaling / sharding
- Rate limiting (single user doesn't need)

---

## 🤝 Development Philosophy

1. **Keep All Memories** - No auto-deletion, pruning is optional (enterprise only)
2. **Natural Memory Patterns** - Decay/fade like real memory, not database delete
3. **Secure by Default** - Localhost unless explicitly opened
4. **Quality over Scale** - 2000 notes well-organized > 10k poorly organized
5. **Practical over Perfect** - Working solution > theoretically optimal
6. **Iterative** - Ship, use, learn, improve
7. **Ethical Design** - Don't implement operations harmful to memory optimization

---

**Last Updated:** Feb 4, 2026
