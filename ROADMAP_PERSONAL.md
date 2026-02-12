# HippoGraph - Personal Roadmap

**Target:** Single user, 500-2,000 notes, personal knowledge management + research
**Philosophy:** Keep all memories. Natural patterns over forced deletion. Zero LLM cost.
**Last Updated:** February 12, 2026

---

## ✅ COMPLETED

### Core Infrastructure (Phase 1-2)
- [x] Graph-based architecture (nodes, edges, entities)
- [x] MCP protocol integration (Claude.ai)
- [x] ANN indexing (hnswlib) — O(log n) similarity search
- [x] In-memory graph cache — O(1) neighbor lookup
- [x] Activation normalization + damping
- [x] spaCy entity extraction + multilingual NER (EN + RU)
- [x] Test infrastructure (30 real tests)
- [x] Docker deployment on Mac Studio M3 Ultra

### Search & Retrieval
- [x] Blend scoring (α=0.6 semantic + β=0.25 spreading + γ=0.15 BM25)
- [x] BM25 keyword search (Okapi BM25, 8678 unique terms, zero-dependency)
- [x] Context window protection (brief/full modes)
- [x] Category, time range, entity type filters
- [x] Duplicate detection (similarity threshold)
- [x] Hub node penalty (entity count-based)
- [x] P@5 = 82%, Top-1 = 100% on internal benchmark

### Memory Features
- [x] Note versioning (5 versions, history, restore)
- [x] Importance scoring (critical/normal/low)
- [x] Emotional context (tone, intensity, reflection)
- [x] Batch knowledge import (196 skills imported)

### Visualization & Analytics
- [x] D3.js force-directed graph viewer + timeline
- [x] Graph metrics: PageRank + community detection (5 communities)
- [x] neural_stats: top PageRank nodes, community sizes, isolated count

### Memory Hygiene (All 5 Phases)
- [x] Phase 1: Test cleanup (24 notes deleted)
- [x] Phase 2: Session-end deduplication (24→14)
- [x] Phase 3: Skill isolation (58K entity edges removed)
- [x] Phase 4: Multilingual NER deployment
- [x] Phase 4.5: Entity re-extraction (587 notes)
- [x] Phase 5: Category normalization (93→68 categories)

**Current State:** 588 nodes, 48,338 edges, 1,721 entities, 68 categories, 8,678 BM25 terms

---

## 🔥 HIGH PRIORITY — Next Development Cycle

### 1. ~~BM25 Hybrid Search~~ ✅ COMPLETED (Feb 12, 2026)
**Source:** Zep/Graphiti competitive analysis
**Result:** Zero-dependency Okapi BM25 implementation. 8678 unique terms indexed in 10ms at startup. Three-signal blend scoring: `final = α×semantic + β×spreading + γ×BM25` where β = 1-α-γ. Backward compatible (γ=0 by default). Incremental updates for new notes. Production deployed with γ=0.15.
**Files:** `src/bm25_index.py`, updated `graph_engine.py` blend scoring

---

### 2. ~~Reranking Pass~~ ✅ COMPLETED (Feb 12, 2026)
**Source:** Zep uses BGE-m3 reranker after initial retrieval
**Result:** Cross-encoder reranking with ms-marco-MiniLM-L-6-v2. Reranks top-20 blend candidates, blends reranker score with original score (RERANK_WEIGHT=0.3). Lazy model loading, backward compatible (disabled by default). Adds ~100ms latency when enabled.
**Files:** `src/reranker.py`, updated `graph_engine.py` Step 6.5

---

### 3. LOCOMO Benchmark Adapter
**Source:** Competitive analysis — all competitors report on standard benchmarks
**Problem:** Our P@5=82% is internal-only. Can't compare directly with Mem0 (LOCOMO J=66.9%), Zep (DMR=94.8%), Letta (LoCoMo=74.0%).
**Solution:** Adapt our search to LOCOMO benchmark format:
- [ ] Load LOCOMO dataset (multi-session conversation pairs)
- [ ] Map LOCOMO queries to our search_with_activation API
- [ ] Report J-score, F1, accuracy in standardized format
- [ ] Compare with published results

**Effort:** 6-8 hours (dataset integration + evaluation script)
**Priority:** HIGH — required for any publication or credible comparison

---

## 🎯 MEDIUM PRIORITY — Quality of Life

### 4. Sleep-Time Compute (Phase 3 Foundation)
**Source:** Letta's innovation — memory refinement during idle
**Idea:** When system is idle, run background processes:
- [ ] Consolidate similar notes (suggest merges)
- [ ] Detect stale connections (decay unused edges)
- [ ] Refresh community detection periodically
- [ ] Pre-compute embeddings for new content patterns

**Relevance:** Directly feeds into Phase 3 multi-agent architecture. The "sleeping" agent could be our second agent with TrueRNG entropy source.

**Effort:** 1-2 weeks (design + implementation)
**Priority:** MEDIUM — research value, not urgent for daily use

---

### 5. CLI/TUI Interface
**Problem:** Web viewer + MCP only, no quick terminal access
**Tasks:**
- [ ] Simple Python CLI: `hippograph add/search/stats`
- [ ] Uses REST API (no new backend code)
- [ ] Optional: Rich TUI for interactive browsing

**Effort:** 2-3 hours
**Priority:** MEDIUM

---

### 6. Search Quality Monitoring
- [ ] Query logs (timestamp, query, results, latency)
- [ ] Automated P@5 regression testing on deploy
- [ ] Latency tracking (P50, P95, P99)

**Effort:** 3-4 hours
**Priority:** MEDIUM

---

## 🔬 RESEARCH — Phase 3 & Beyond

### Multi-Agent Architecture
- [ ] Second AI agent with TrueRNG hardware entropy
- [ ] Autonomous multi-agent experiments
- [ ] Cross-agent memory sharing protocol
- [ ] Sleep-time compute integration

### Academic Publication
- [ ] LOCOMO benchmark results (see #3 above)
- [ ] Methodology paper: spreading activation for AI memory
- [ ] Comparative analysis: zero-LLM-cost vs LLM-dependent approaches
- [ ] Identity continuity experiments documentation

### Real-Time Graph Visualization
- [ ] Live graph updates via WebSocket
- [ ] Community highlighting in viewer
- [ ] PageRank-based node sizing
- [ ] Temporal playback improvements

---

## ❌ OUT OF SCOPE (Personal)

Moved to ROADMAP_ENTERPRISE.md:
- Multi-tenant isolation
- Cloud managed service
- SSO/OAuth
- Horizontal scaling
- SOC2/GDPR compliance
- Multi-framework integration (LangChain, CrewAI)
- Bulk delete/cleanup operations
- Graph-wide rollback

---

## 📊 Competitive Position (Feb 2026)

| Metric | HippoGraph | Mem0 | Zep | Letta | doobidoo |
|--------|-----------|------|-----|-------|----------|
| LLM Cost | **$0** | ~$0.01/note | ~$0.02/note | ~$0.05/note | $0 |
| Retrieval | Spread+Semantic+BM25 | Vector+Graph | BM25+Semantic+Graph | Agent-driven | Vector-only |
| Latency | 200-500ms | P95=1.44s | P95=300ms | varies | 5ms (cached) |
| Graph | ✅ Spreading | ✅ Mem0ᵍ | ✅ Temporal KG | ❌ | ❌ |
| Emotional | ✅ | ❌ | ❌ | ❌ | ✅ |
| Self-hosted | ✅ | ✅+Cloud | ✅+Cloud | ✅+Cloud | ✅ |

**Our niche:** Zero-LLM-cost, spreading activation, associative memory research. Nobody else does this.
