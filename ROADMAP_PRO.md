# HippoGraph - Pro Roadmap

**Target:** Multi-user deployment, 10K-100K+ notes, production workloads
**Philosophy:** Performance at scale. Proven techniques from competitors. **LLM-optional architecture.**
Core system = zero LLM cost (runs on 8GB RAM VPS). LLM layer = pro add-on for
organizations with GPU servers. Scales DOWN to minimal hardware better than any competitor.
**Last Updated:** February 18, 2026

> ⚠️ This roadmap is aspirational. Current focus is personal/research use.
> Pro features are documented for completeness based on competitive analysis.

---

## Tier 1: Multi-User Foundation

### 1. Multi-Tenant Isolation
**Source:** Mem0, Zep, Letta all support multi-user
**Tasks:**
- [ ] User ID column in nodes/edges/entities tables
- [ ] API key → user mapping
- [ ] Per-user ANN indices
- [ ] Per-user graph cache partitions
- [ ] Per-user PageRank/community computation

**Effort:** 1-2 weeks

---

### 2. LLM-Based Entity Extraction (Ollama)
**Source:** Mem0/Zep use LLM for entity extraction — higher quality than spaCy
**Approach:** Optional Ollama sidecar for enhanced extraction:
- [ ] Ollama container alongside hippograph
- [ ] Fallback chain: Ollama → spaCy (zero-cost default)
- [ ] Configurable per-user: LLM extraction on/off
- [ ] Relationship extraction (not just entities)

**Trade-off:** +3-7GB Docker image, +4-12GB RAM, 2-5s/note vs 100ms spaCy
**Effort:** 1 week

---

### 3. Cloud Sync
**Source:** doobidoo uses Cloudflare for cross-device sync
**Tasks:**
- [ ] Cloudflare Workers KV or D1 backend option
- [ ] Bidirectional sync protocol
- [ ] Conflict resolution (last-write-wins or merge)
- [ ] Encryption at rest for cloud storage

**Effort:** 2 weeks

---

## Tier 2: Search & Retrieval at Scale

### 4. ~~Bi-Temporal Model~~ ✅ IMPLEMENTED (Personal, Feb 18, 2026)
**Source:** Zep/Graphiti tracks "when fact was true" vs "when ingested"
**Status:** Implemented in personal roadmap. t_event_start/end columns, temporal extractor,
δ signal in blend scoring, query temporal decomposition. Ready for pro extension:
- [ ] Add t_valid, t_invalid columns to edges (fact validity tracking)
- [ ] Temporal queries: "what was true on date X?"
- [ ] Fact invalidation without deletion
- [ ] Historical graph reconstruction

**Remaining effort:** 1 week (edge-level temporal, fact invalidation)

---

### 5. ~~Advanced Reranking Pipeline~~ ✅ PARTIALLY IMPLEMENTED (Personal, Feb 12, 2026)
**Source:** Zep uses BGE-m3 for reranking after retrieval
**Status:** Cross-encoder reranking deployed (ms-marco-MiniLM-L-6-v2). Remaining for pro:
- [ ] Multi-factor scoring: graph distance + recency + importance + entity overlap
- [ ] Learning-to-rank from user feedback
- [ ] Result diversity (avoid clustering)

**Remaining effort:** 1 week

---

### 6. Multi-Framework Integration
**Source:** Mem0/Zep/Letta integrate with LangChain, CrewAI, AutoGen
**Tasks:**
- [ ] LangChain memory adapter
- [ ] CrewAI knowledge source plugin
- [ ] OpenAI-compatible REST API
- [ ] SDK: Python + TypeScript

**Effort:** 2-3 weeks

---

## Tier 2.5: LLM Enhancement Layer (Optional)

> Pro customers with GPU infrastructure can enable LLM features.
> Core system ALWAYS works without LLM — this tier is purely additive.

### Reciprocal Rank Fusion (RRF)
**Source:** Hindsight/TEMPR (Dec 2025) — 89.61% on LoCoMo
**Problem:** Current weighted blend (α×sem + β×spread + γ×BM25 + δ×temporal) requires manual
tuning and suffers from score scale mismatch between signals.
**Solution:** RRF merges ranked lists by rank position, not score magnitude:
```
RRF_score(d) = Σ 1/(k + rank_r(d)) for each retriever r
```
- [ ] Implement RRF fusion as alternative to weighted blend
- [ ] A/B test: RRF vs current blend on regression suite
- [ ] Make configurable: FUSION_METHOD=blend|rrf

**Effort:** 3-4 hours (no LLM needed — pure algorithmic improvement)
**Priority:** HIGH — benefits all users, zero cost

### LLM-Powered Temporal Reasoning
**Source:** TReMu (ACL 2025) — 29.83% → 77.67% on temporal queries
**Problem:** Temporal retrieval at 36.5% is fundamental ceiling for retrieval-only systems.
**Solution:** Neuro-symbolic approach: LLM generates Python code for date calculations
- [ ] Ollama sidecar container (optional docker-compose profile)
- [ ] Temporal query detection → LLM code generation → execute → filter results
- [ ] Timeline summarization at ingestion (infer dates from context)
- [ ] Graceful degradation: Ollama unavailable → raw retrieval fallback
- [ ] Config: `OLLAMA_ENABLED=false` (default OFF)

**Requirements:** GPU server or M-series Mac for reasonable inference speed
**Effort:** 1-2 weeks
**Priority:** MEDIUM for pro (HIGH for benchmark comparison)

### LLM-Powered End-to-End QA
**Problem:** Our metrics are retrieval-only (Recall@5). Competitors report answer accuracy.
**Solution:** Retrieved context → LLM answer generation → F1/accuracy scoring
- [ ] Answer generation pipeline with configurable LLM backend
- [ ] LLM-as-judge evaluation mode
- [ ] Compare end-to-end with Mem0 (J=66.9%), Letta (74.0%), Hindsight (89.61%)

**Effort:** 1 week (after Ollama sidecar is deployed)

---

## Tier 3: Operations & Security

### 7. Authentication & Authorization
- [ ] OAuth 2.0 / SSO (OIDC)
- [ ] Role-based access control (RBAC)
- [ ] API key management (rotation, scoping)
- [ ] Audit logging (all changes with user/timestamp)

### 8. Observability
- [ ] Prometheus metrics (latency, throughput, cache hit rates)
- [ ] Structured logging (ELK stack)
- [ ] Distributed tracing
- [ ] Health checks beyond simple ping
- [ ] Alert on retrieval quality degradation

### 9. Performance at Scale
- [ ] Production WSGI server (Gunicorn/Uvicorn)
- [ ] PostgreSQL migration (from SQLite)
- [ ] Read replicas for search-heavy workloads
- [ ] Connection pooling
- [ ] Horizontal scaling with load balancer

### 10. Compliance
- [ ] SOC 2 readiness
- [ ] GDPR data handling (right to deletion, export)
- [ ] Encryption at rest + in transit
- [ ] Data residency options

---

## Tier 4: Advanced Features

### Entity Resolution
- [ ] Entity disambiguation ("Apple" company vs fruit)
- [ ] Coreference resolution (pronouns → entities)
- [ ] Synonym/acronym merging (ML → Machine Learning)
- [ ] Knowledge base linking (Wikipedia, DBpedia)

### Memory Lifecycle
- [ ] Short-term memory (session-based, 24h TTL)
- [ ] Long-term memory with reinforcement learning
- [ ] Working memory cache (Redis/Valkey)
- [ ] Automated consolidation (merge similar notes)
- [ ] Access-based promotion (short-term → long-term)

### Bulk Operations
- [ ] Bulk delete by weight threshold / age / category
- [ ] Graph-wide rollback (point-in-time snapshots)
- [ ] Bulk import from Mem0 / doobidoo format
- [ ] Export to standard formats (JSON-LD, RDF)

---

## Estimated Effort by Tier

| Tier | Scope | Estimate |
|------|-------|----------|
| Tier 1 | Multi-user foundation | 4-5 weeks |
| Tier 2 | Search at scale | 3-4 weeks |
| Tier 2.5 | LLM enhancement (optional) | 2-3 weeks |
| Tier 3 | Operations & security | 4-6 weeks |
| Tier 4 | Advanced features | 4-6 weeks |
| **Total** | **Full pro** | **~5 months** |

---

## Competitive Gaps to Close for Pro

| Feature | Status | Competitor Reference |
|---------|--------|---------------------|
| Multi-tenant | ❌ Missing | Mem0, Zep, Letta |
| BM25 hybrid | ✅ Done (Personal) | Zep |
| Cross-encoder reranking | ✅ Done (Personal) | Zep |
| Bi-temporal model | ✅ Partial (node-level done, edge-level TODO) | Zep |
| Standard benchmarks | ✅ Done — 66.8% LOCOMO Recall@5 | All |
| RRF fusion | ❌ Planned — replace weighted blend | Hindsight/TEMPR |
| Cloud deployment | ❌ Missing | Mem0 Cloud, Zep Cloud |
| LLM entity extraction | ❌ Optional | Mem0, Zep |
| LLM temporal reasoning | ❌ Planned (Tier 2.5) | TReMu, Hindsight |
| Framework integrations | ❌ MCP only | All competitors |
| End-to-end QA | ❌ Planned (Tier 2.5) | Mem0, Letta, Hindsight |

**Our pro differentiator:** Zero-LLM-cost base + optional LLM enhancement.
Core runs on 8GB RAM / $5 VPS. Nobody else scales down this far.
Competitors REQUIRE LLM for basic operation. We don't.
