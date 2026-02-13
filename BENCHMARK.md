# HippoGraph — LOCOMO Benchmark Results

## February 2026

### Overview

HippoGraph was evaluated on the [LOCOMO benchmark](https://github.com/snap-research/locomo) — a standardized dataset for testing long-conversation memory systems. LOCOMO contains 10 multi-session conversations (272 sessions, 5,882 dialogue turns) with 1,986 QA pairs across multiple reasoning categories.

**Key result:** HippoGraph achieves **44.2% Recall@5** on retrieval with **zero LLM cost** — all processing runs locally using spaCy NER, sentence-transformers embeddings, and BM25 keyword search.

---

### Setup

| Parameter | Value |
|-----------|-------|
| Dataset | LOCOMO-10 (10 conversations, 272 sessions, 5,882 turns) |
| Queries evaluated | 1,540 (excluding adversarial) |
| Metric | Recall@5, MRR (Mean Reciprocal Rank) |
| Infrastructure | Docker container, isolated benchmark DB |
| LLM calls | **0** (zero — fully local processing) |
| Embedding model | paraphrase-multilingual-MiniLM-L12-v2 |
| Entity extraction | spaCy (en\_core\_web\_sm + xx\_ent\_wiki\_sm) |
| Retrieval pipeline | Semantic + Spreading Activation + BM25 blend |
| Blend weights | α=0.6 (semantic), β=0.25 (spreading activation), γ=0.15 (BM25) |
| Reranking | Disabled for this run |

---

### Results: Turn-Level Granularity (5,870 notes)

| Category | Queries | Hits | Recall@5 | MRR |
|----------|---------|------|----------|-----|
| **Overall** | **1,540** | **681** | **44.2%** | **0.304** |
| Single-hop | 282 | 107 | 37.9% | 0.227 |
| Multi-hop | 321 | 169 | **52.6%** | 0.394 |
| Temporal | 96 | 22 | 22.9% | 0.139 |
| Open-domain | 841 | 383 | 45.5% | 0.314 |

### Results: Session-Level Granularity (272 notes)

| Category | Queries | Hits | Recall@5 | MRR |
|----------|---------|------|----------|-----|
| **Overall** | **1,540** | **502** | **32.6%** | **0.223** |
| Single-hop | 282 | 142 | 50.4% | 0.315 |
| Multi-hop | 321 | 88 | 27.4% | 0.207 |
| Temporal | 96 | 34 | 35.4% | 0.236 |
| Open-domain | 841 | 238 | 28.3% | 0.196 |

---

### Granularity Impact Analysis

| Category | Session → Turn | Delta |
|----------|---------------|-------|
| Overall | 32.6% → 44.2% | **+11.6%** |
| Multi-hop | 27.4% → 52.6% | **+25.2%** |
| Open-domain | 28.3% → 45.5% | **+17.2%** |
| Single-hop | 50.4% → 37.9% | -12.5% |
| Temporal | 35.4% → 22.9% | -12.5% |

**Key finding:** Turn-level granularity dramatically improves multi-hop retrieval (+25.2%), validating that spreading activation works best on fine-grained memory nodes. However, single-hop and temporal queries benefit from broader session context. A hybrid approach (3-5 turns per note) is expected to capture the best of both.

---

### Important Notes on Comparability

⚠️ **These results measure retrieval quality only, not end-to-end QA accuracy.**

Our Recall@5 measures whether the correct evidence document appears in the top-5 retrieved results. Other systems report different metrics:

| System | Metric | Score | What It Measures |
|--------|--------|-------|-----------------|
| **HippoGraph** | **Recall@5** | **44.2%** | Retrieved correct document in top-5 |
| Mem0 | LOCOMO J-score | 66.9% | LLM-judged answer accuracy |
| Letta (MemGPT) | LoCoMo accuracy | 74.0% | LLM-generated answer accuracy |
| GPT-4 (no memory) | F1 | 32.1% | Answer text overlap with ground truth |
| Human ceiling | F1 | 87.9% | Human-generated answers |

**Direct numerical comparison across these metrics is not valid.** An end-to-end evaluation (retrieval + LLM answer generation) would be needed for apples-to-apples comparison.

However, one comparison is meaningful: **HippoGraph achieves its results at $0 LLM infrastructure cost**, while Mem0, Zep, and Letta all require LLM API calls for entity extraction, fact consolidation, or memory management during both ingestion and retrieval.

---

### Retrieval Pipeline

```
Query → Embedding → ANN Search (HNSW)
                         ↓
              Spreading Activation (3 iterations, decay=0.7)
                         ↓
              BM25 Keyword Search (Okapi BM25, k1=1.5, b=0.75)
                         ↓
              Blend Scoring: α×semantic + β×spreading + γ×BM25
                         ↓
              Temporal Decay (half-life=30 days)
                         ↓
              Top-K Results
```

### Next Steps

- [ ] Hybrid granularity (3-5 turns per note) to balance multi-hop and single-hop performance
- [ ] Enable cross-encoder reranking (ms-marco-MiniLM-L-6-v2) and measure impact
- [ ] Tune blend weights (α, β, γ) per category
- [ ] Add LLM generation layer for end-to-end F1 comparison with Mem0/Letta
- [ ] Evaluate on LongMemEval and DMR benchmarks

---

### Reproduce

```bash
# 1. Start isolated benchmark container
docker-compose -f docker-compose.benchmark.yml up -d --build

# 2. Load dataset and run evaluation
python3 benchmark/locomo_adapter.py --all \
  --api-url http://localhost:5003 \
  --api-key benchmark_key_locomo_2026 \
  --granularity turn

# Results saved to benchmark/results/locomo_results.json
```

---

*HippoGraph is a self-hosted, zero-LLM-cost, graph-based associative memory system. [github.com/artemMprokhorov/hippograph](https://github.com/artemMprokhorov/hippograph)*
