# HippoGraph - Enterprise Roadmap

**Target:** Multi-user deployment, 10K-100K+ notes, production workloads
**Philosophy:** Performance at scale. Proven techniques from competitors. LLM-optional.
**Last Updated:** February 12, 2026

> ⚠️ This roadmap is aspirational. Current focus is personal/research use.
> Enterprise features are documented for completeness based on competitive analysis.

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

### 4. Bi-Temporal Model
**Source:** Zep/Graphiti tracks "when fact was true" vs "when ingested"
**Tasks:**
- [ ] Add t_valid, t_invalid columns to edges
- [ ] Temporal queries: "what was true on date X?"
- [ ] Fact invalidation without deletion
- [ ] Historical graph reconstruction

**Effort:** 1-2 weeks

---

### 5. Advanced Reranking Pipeline
**Source:** Zep uses BGE-m3 for reranking after retrieval
**Tasks:**
- [ ] Cross-encoder reranker (BGE-m3 or ms-marco)
- [ ] Multi-factor scoring: graph distance + recency + importance + entity overlap
- [ ] Learning-to-rank from user feedback
- [ ] Result diversity (avoid clustering)

**Effort:** 1 week

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
| Tier 3 | Operations & security | 4-6 weeks |
| Tier 4 | Advanced features | 4-6 weeks |
| **Total** | **Full enterprise** | **~4 months** |

---

## Competitive Gaps to Close for Enterprise

| Feature | Status | Competitor Reference |
|---------|--------|---------------------|
| Multi-tenant | ❌ Missing | Mem0, Zep, Letta |
| BM25 hybrid | ❌ Missing (Personal roadmap #1) | Zep |
| Standard benchmarks | ❌ Missing (Personal roadmap #3) | All |
| Cloud deployment | ❌ Missing | Mem0 Cloud, Zep Cloud |
| LLM entity extraction | ❌ Optional | Mem0, Zep |
| Framework integrations | ❌ MCP only | All competitors |

**Our enterprise differentiator:** Zero-LLM-cost base + optional LLM enhancement. Nobody else offers this hybrid approach.
