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
- [x] Blend scoring (α=0.7 semantic + 0.3 spreading activation)
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

**Current State:** 587 nodes, 47,924 edges, 1,721 entities, 68 categories

---

## 🔥 HIGH PRIORITY — Next Development Cycle

### 1. BM25 Hybrid Search
**Source:** Zep/Graphiti competitive analysis
**Problem:** Our search is semantic-only + entity graph. Exact keyword matches (API names, error codes, specific terms) get lost in semantic similarity.
**Solution:** Add BM25 keyword scoring as third signal:
```
final = α × semantic + β × spreading + γ × BM25
```
**Implementation:**
- [ ] Add rank-bm25 or custom Okapi BM25 on note content
- [ ] Build inverted index at startup (alongside ANN + graph cache)
- [ ] Integrate into blend scoring with tunable γ parameter
- [ ] Benchmark: expect P@5 improvement on exact-term queries

**Effort:** 4-6 hours
**Priority:** HIGH — addresses known weakness in current retrieval

---

### 2. Reranking Pass
**Source:** Zep uses BGE-m3 reranker after initial retrieval
**Problem:** Our blend score is computed once. A reranking step on top-20 candidates could improve precision.
**Solution:** After initial blend scoring, rerank top-N candidates with cross-encoder:
- [ ] Use sentence-transformers cross-encoder (ms-marco-MiniLM-L6-v2 or similar)
- [ ] Rerank top-20 → return top-5
- [ ] Measure P@5 improvement vs baseline

**Effort:** 3-4 hours
**Priority:** HIGH — proven technique, low risk

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
| Retrieval | Spread+Semantic | Vector+Graph | BM25+Semantic+Graph | Agent-driven | Vector-only |
| Latency | 200-500ms | P95=1.44s | P95=300ms | varies | 5ms (cached) |
| Graph | ✅ Spreading | ✅ Mem0ᵍ | ✅ Temporal KG | ❌ | ❌ |
| Emotional | ✅ | ❌ | ❌ | ❌ | ✅ |
| Self-hosted | ✅ | ✅+Cloud | ✅+Cloud | ✅+Cloud | ✅ |

**Our niche:** Zero-LLM-cost, spreading activation, associative memory research. Nobody else does this.
