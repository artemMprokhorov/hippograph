# HippoGraph — LOCOMO Benchmark

## February 2026

### Overview

HippoGraph was evaluated on the [LOCOMO benchmark](https://github.com/snap-research/locomo) — a standardized dataset for testing long-conversation memory systems. LOCOMO contains 10 multi-session conversations (272 sessions, 5,882 dialogue turns) with 1,986 QA pairs across multiple reasoning categories.

**Key result:** HippoGraph retrieval runs with **zero LLM infrastructure cost** — all processing runs locally using spaCy NER, sentence-transformers embeddings, BM25 keyword search, cross-encoder reranking, bi-temporal model, and query temporal decomposition.

---

### Best Configuration (Hybrid + Reranking)

| Parameter | Value |
|-----------|-------|
| Dataset | LOCOMO-10 (10 conversations, 272 sessions, 5,882 turns) |
| Queries evaluated | 1,540 (excluding adversarial) |
| Metric | Recall@5, MRR (Mean Reciprocal Rank) |
| Infrastructure | Docker container, isolated benchmark DB |
| LLM calls | **0** (zero — fully local processing) |
| Embedding model | paraphrase-multilingual-MiniLM-L12-v2 |
| Entity extraction | spaCy (en\_core\_web\_sm + xx\_ent\_wiki\_sm) |
| Retrieval pipeline | Semantic + Spreading Activation + BM25 + Temporal + Cross-Encoder Reranking |
| Blend weights | α=0.6 (semantic), β=0.10 (spreading), γ=0.15 (BM25), δ=0.15 (temporal, auto for temporal queries) |
| Reranking | cross-encoder/ms-marco-MiniLM-L-6-v2, weight=0.3, top-N=20 |
| Granularity | Hybrid (3-turn chunks, ~1,960 notes) |
| Query decomposition | Temporal signal stripping + order scoring |
| Bi-temporal | t_event extraction via spaCy DATE + regex resolver |

---

### Evaluated Query Categories

| Category | Queries |
|----------|---------|
| **Overall** | **1,540** |
| Single-hop | 282 |
| Multi-hop | 321 |
| Temporal | 96 |
| Open-domain | 841 |

---

### Optimization Journey

| Configuration | Notes |
|--------------|-------|
| Session-level (baseline) | 272 notes, broad context |
| Turn-level | 5,870 notes |
| Hybrid + Reranking | ~1,960 notes |
| + Bi-temporal δ signal | Temporal overlap scoring |
| + Embedding enrichment ❌ | Reverted — polluted non-temporal embeddings |
| **+ Query decomposition** | **Temporal signal stripping + order scoring** |

**Key findings:**
- Hybrid granularity (3-turn chunks) captures the best of both session and turn-level approaches
- Cross-encoder reranking improves over the turn-level baseline
- Spreading activation validated: multi-hop improved from session-level to the best configuration
- Query temporal decomposition: stripping temporal signal words improves semantic matching
- Embedding enrichment with dates hurts non-temporal queries — reverted
- Temporal queries remain the hardest category — requires LLM reasoning layer, not retrieval improvements

---

### Important Notes on Comparability

⚠️ **These results measure retrieval quality only, not end-to-end QA accuracy.**

Our Recall@5 measures whether the correct evidence document appears in the top-5 retrieved results. Other systems report different metrics:

| System | Metric | What It Measures |
|--------|--------|-----------------|
| **HippoGraph** | **Recall@5** | Retrieved correct document in top-5 |
| Mem0 | LOCOMO J-score | LLM-judged answer accuracy |
| Letta (MemGPT) | LoCoMo accuracy | LLM-generated answer accuracy |
| GPT-4 (no memory) | F1 | Answer text overlap with ground truth |
| Human ceiling | F1 | Human-generated answers |

**Direct numerical comparison across these metrics is not valid.** An end-to-end evaluation (retrieval + LLM answer generation) would be needed for apples-to-apples comparison.

However, one comparison is meaningful: **HippoGraph achieves its results at $0 LLM infrastructure cost**, while Mem0, Zep, and Letta all require LLM API calls for entity extraction, fact consolidation, or memory management during both ingestion and retrieval.

---

### Retrieval Pipeline

```
Query → Temporal Decomposition (strip signal words, detect direction)
                         ↓
              Embedding → ANN Search (HNSW)
                         ↓
              Spreading Activation (3 iterations, decay=0.7)
                         ↓
              BM25 Keyword Search (Okapi BM25, k1=1.5, b=0.75)
                         ↓
              Temporal Scoring (date overlap + chronological ordering)
                         ↓
              Blend: α×semantic + β×spreading + γ×BM25 + δ×temporal
                         ↓
              Cross-Encoder Reranking (ms-marco-MiniLM-L-6-v2)
                         ↓
              Temporal Decay (half-life=30 days)
                         ↓
              Top-K Results
```

### Next Steps

- [x] ~~Hybrid granularity (3-turn chunks)~~
- [x] ~~Cross-encoder reranking~~ — **included in best result**
- [x] ~~Bi-temporal model~~ — **t_event extraction, δ signal in blend**
- [x] ~~Query temporal decomposition~~ — **via signal stripping**
- [ ] Add LLM generation layer (Ollama) for end-to-end F1 comparison with Mem0/Letta
- [ ] Tune blend weights (α, β, γ, δ) per category
- [ ] Evaluate on LongMemEval and DMR benchmarks

---

### Reproduce

```bash
# 1. Start isolated benchmark container (includes reranking)
docker-compose -f docker-compose.benchmark.yml up -d --build

# 2. Load dataset and run evaluation (hybrid granularity)
python3 benchmark/locomo_adapter.py --all \
  --api-url http://localhost:5003 \
  --api-key benchmark_key_locomo_2026 \
  --granularity hybrid

# Results saved to benchmark/results/locomo_results.json
```

---

*HippoGraph is a self-hosted, zero-LLM-cost, graph-based associative memory system. [github.com/artemMprokhorov/hippograph](https://github.com/artemMprokhorov/hippograph)*
