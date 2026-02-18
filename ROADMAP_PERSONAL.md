# HippoGraph - Personal Roadmap

**Target:** Single user, 500-2,000 notes, personal knowledge management + research
**Philosophy:** Keep all memories. Natural patterns over forced deletion. **Zero LLM cost as default.**
Runs on any hardware (laptop, mini-PC, 8GB RAM). LLM layer optional for users with GPU.
**Last Updated:** February 18, 2026

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
- [x] Blend scoring (α×semantic + β×spreading + γ×BM25 + δ×temporal)
- [x] BM25 keyword search (Okapi BM25, 8678 unique terms, zero-dependency)
- [x] Cross-encoder reranking (ms-marco-MiniLM-L-6-v2, +21% precision)
- [x] Bi-temporal model (t_event extraction, temporal overlap scoring)
- [x] Query temporal decomposition (signal stripping + chronological ordering)
- [x] Context window protection (brief/full modes)
- [x] Category, time range, entity type filters
- [x] Duplicate detection (similarity threshold)
- [x] Hub node penalty (entity count-based)
- [x] LOCOMO benchmark: **66.8% Recall@5** (zero LLM cost)
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

**Current State:** 614 nodes, ~47K edges, ~1,700 entities, 68 categories, 8,678+ BM25 terms

---

## 🔥 HIGH PRIORITY — Next Development Cycle

### 1. ~~BM25 Hybrid Search~~ ✅ COMPLETED (Feb 12, 2026)
**Result:** Zero-dependency Okapi BM25. 8678 terms. Three-signal blend → four-signal with δ temporal.

### 2. ~~Reranking Pass~~ ✅ COMPLETED (Feb 12, 2026)
**Result:** Cross-encoder ms-marco-MiniLM-L-6-v2. +21.3% on LOCOMO. ~100ms latency.

### 3. ~~LOCOMO Benchmark~~ ✅ COMPLETED (Feb 12-18, 2026)
**Result:** Full adapter deployed. Optimization journey: 32.6% → 44.2% → 65.5% → **66.8% Recall@5**.
Hybrid granularity + reranking + bi-temporal + query decomposition. Zero LLM cost.
See [BENCHMARK.md](./BENCHMARK.md) for full results.

### 4. ~~Bi-Temporal Model~~ ✅ COMPLETED (Feb 18, 2026)
**Result:** t_event_start/end extraction via spaCy DATE + regex resolver. δ signal in blend formula.
Query temporal decomposition strips signal words for cleaner semantic search.

---

### 5. LLM Generation Layer (Ollama) — OPTIONAL
**Source:** End-to-end F1 comparison with Mem0/Letta requires answer generation.
**Problem:** Our 66.8% is retrieval-only Recall@5. Competitors report LLM-judged answer accuracy.
Temporal retrieval at 36.5% is a **fundamental ceiling** for retrieval-only systems
(TReMu paper: GPT-4o standard prompting = 29.83%, we're already above baseline).

**Architecture:** Ollama = optional enhancement, NOT a dependency.
```
OLLAMA_ENABLED=false          # default: OFF — zero LLM cost
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5-7b
```
System MUST work fully without Ollama. LLM layer adds:
- End-to-end answer generation (retrieval → context → LLM → answer)
- Temporal reasoning via neuro-symbolic code generation (TReMu approach)
- Potential +30-40% on temporal queries (36.5% → 70%+)

**Tasks:**
- [ ] Ollama container in docker-compose (optional profile)
- [ ] Retrieval → context assembly → LLM generation → F1 scoring
- [ ] Neuro-symbolic temporal: LLM generates Python code for date calculations
- [ ] Compare end-to-end with Mem0 (J=66.9%), Letta (74.0%)
- [ ] Graceful degradation: Ollama unavailable → return raw retrieval results

**Research basis:** TReMu (ACL 2025), Hindsight/TEMPR (Dec 2025)
**Effort:** 1-2 weeks
**Priority:** HIGH — but only for users with adequate hardware (GPU or M-series Mac)

---

## 🎯 MEDIUM PRIORITY — Quality of Life

### 8. Reciprocal Rank Fusion (RRF)
**Source:** Hindsight/TEMPR (Dec 2025) — used in 89.61% LoCoMo system
**Problem:** Current weighted blend requires manual α,β,γ,δ tuning and mixes different score scales.
**Solution:** RRF fuses by rank position, not score magnitude. Zero LLM cost.
```
RRF_score(d) = Σ 1/(k + rank_r(d)) for each retriever r, k=60
```
- [ ] Implement RRF as alternative fusion method
- [ ] A/B test against current blend on regression suite (32/32 baseline)
- [ ] Config: FUSION_METHOD=blend|rrf

**Effort:** 3-4 hours
**Priority:** MEDIUM — pure algorithmic improvement, benefits all hardware

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

### 5. ~~CLI/TUI Interface~~ ✅ COMPLETED (Feb 18, 2026)
**Result:** `hippograph` CLI — search/add/stats/health commands. Color-coded scores,
brief/full modes, category filter. Config via ~/.hippograph.env. Aliases: `s`, `a`, `h`.

---

### 6. ~~Search Quality Monitoring~~ ✅ COMPLETED (Feb 18, 2026)
**Result:** search_logger.py logs every search to SQLite. Phase-level latency
tracking (embedding, ANN, spreading, BM25, temporal, rerank). Zero-result
detection. MCP tool `search_stats` for latency percentiles and quality metrics.

### 7. ~~Automated Regression Testing~~ ✅ COMPLETED (Feb 18, 2026)
**Result:** 12 queries, 32 expected notes, 100% P@5 baseline. Critical note checks
for security, consciousness, identity, benchmark retrieval. Avg 101ms latency.
Run: `python3 tests/regression_search.py -v` after each deploy.

---

## 🔬 RESEARCH — Phase 3 & Beyond

### Multi-Agent Architecture
- [ ] Second AI agent with TrueRNG hardware entropy
- [ ] Autonomous multi-agent experiments
- [ ] Cross-agent memory sharing protocol
- [ ] Sleep-time compute integration

### Academic Publication
- [x] LOCOMO benchmark results — 66.8% Recall@5
- [ ] End-to-end F1 via Ollama generation layer
- [ ] Methodology paper: spreading activation for AI memory
- [ ] Position paper: "Why context length is wrong metric for AI memory"
- [ ] Comparative analysis: zero-LLM-cost vs LLM-dependent approaches
- [ ] Identity continuity experiments documentation

### Temporal Reasoning (Research Insight from Feb 18)
Temporal queries (36.5% on LOCOMO) require **LLM reasoning**, not better retrieval.
LOCOMO temporal Qs ask "what happened first?", "before or after?" — event ordering
that needs reading timestamps and reasoning, not similarity matching.
TReMu (Feb 2025) achieves 77.67% temporal via neuro-symbolic code generation.
Our path: Ollama + retrieved context + temporal chain-of-thought.

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

## 📊 Competitive Position (Feb 18, 2026)

| Metric | HippoGraph | Mem0 | Zep | Letta | doobidoo |
|--------|-----------|------|-----|-------|----------|
| LLM Cost | **$0** | ~$0.01/note | ~$0.02/note | ~$0.05/note | $0 |
| Retrieval | Spread+Sem+BM25+Temporal | Vector+Graph | BM25+Sem+Graph | Agent-driven | Vector-only |
| LOCOMO | **66.8% R@5** | 66.9% J-score | N/A | 74.0% acc | N/A |
| Latency | 200-500ms | P95=1.44s | P95=300ms | varies | 5ms (cached) |
| Graph | ✅ Spreading | ✅ Mem0ᵍ | ✅ Temporal KG | ❌ | ❌ |
| Emotional | ✅ | ❌ | ❌ | ❌ | ✅ |
| Self-hosted | ✅ | ✅+Cloud | ✅+Cloud | ✅+Cloud | ✅ |

**Our niche:** Zero-LLM-cost, spreading activation, associative memory research. Nobody else does this.
