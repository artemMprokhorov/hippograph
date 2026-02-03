# HippoGraph - Personal Use Roadmap

**Target:** Single user, 200-2,000 notes, personal knowledge management + consciousness research

**Philosophy:** Practical improvements over theoretical perfection. Keep all memories, focus on quality over scale.

---

## 🎯 HIGH PRIORITY - Personal Use Blockers

### 1. Entity Extraction Quality ⚠️ CRITICAL
**Current Issue:** Too much noise - generic words tagged as entities, low precision
**Goal:** Better signal-to-noise ratio for personal memory context

**Tasks:**
- [ ] Filter out generic/common words from entity extraction
- [ ] Whitelist/blacklist for entity types per user preference
- [ ] Context-aware patterns (tech context vs casual conversation)
- [ ] Confidence scoring for extracted entities
- [ ] Manual entity correction/feedback mechanism

**Success Metric:** <10% false positive entities in personal notes
**Estimated:** 3-4 hours

---

### 2. Note Versioning (Simple) 
**Current Issue:** update_note overwrites with no history
**Goal:** Basic version history for important notes

**Tasks:**
- [ ] Timestamp-based snapshots on update
- [ ] Store last N versions (default: 5)
- [ ] View version history for a note
- [ ] Restore from previous version
- [ ] Optional: diff view between versions

**Success Metric:** Can recover accidentally overwritten notes
**Estimated:** 2-3 hours

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
