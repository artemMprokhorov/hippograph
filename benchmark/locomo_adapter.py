"""
LOCOMO Benchmark Adapter for HippoGraph

Evaluates HippoGraph retrieval quality against the LoCoMo benchmark
(Maharana et al., ACL 2024) — standard benchmark for long-term
conversational memory systems.

Approach: Retrieval-only evaluation (no LLM needed)
- Load LOCOMO conversations as notes into HippoGraph
- Run QA queries through our search pipeline
- Measure Recall@k and P@5 on retrieved passages vs ground truth evidence

Data source: https://github.com/snap-research/locomo
File: data/locomo10.json (10 conversations, ~300 QA pairs)

Usage:
    # Step 1: Download dataset
    python locomo_adapter.py --download

    # Step 2: Load conversations into HippoGraph (creates temp DB)
    python locomo_adapter.py --load

    # Step 3: Run evaluation
    python locomo_adapter.py --eval

    # Step 4: Full pipeline
    python locomo_adapter.py --all

Privacy: All processing is LOCAL. LOCOMO data is synthetic
(fictional characters). No real user data involved.
No LLM API calls needed for retrieval-only evaluation.
"""

import json
import os
import sys
import time
import argparse
from pathlib import Path

# Config
LOCOMO_DATA = "benchmark/locomo10.json"
LOCOMO_URL = "https://raw.githubusercontent.com/snap-research/locomo/main/data/locomo10.json"
RESULTS_DIR = "benchmark/results"


# ============================================================
# STEP 1: Download LOCOMO dataset
# ============================================================

def download_dataset():
    """Download locomo10.json from GitHub."""
    import urllib.request
    
    os.makedirs(os.path.dirname(LOCOMO_DATA), exist_ok=True)
    if os.path.exists(LOCOMO_DATA):
        print(f"✅ Dataset already exists: {LOCOMO_DATA}")
        return
    
    print(f"📥 Downloading LOCOMO dataset...")
    urllib.request.urlretrieve(LOCOMO_URL, LOCOMO_DATA)
    size = os.path.getsize(LOCOMO_DATA) / 1024 / 1024
    print(f"✅ Downloaded: {LOCOMO_DATA} ({size:.1f} MB)")


# ============================================================
# STEP 2: Parse dataset — extract conversations and QA pairs
# ============================================================

def parse_dataset():
    """Parse locomo10.json into conversations and QA pairs.
    
    Returns:
        conversations: list of dicts, each with:
            - id: conversation index
            - speaker_a, speaker_b: names
            - sessions: list of (session_key, timestamp, turns)
            - qa: list of QA annotations
        
        qa_pairs: flat list of all QA items with:
            - conversation_id, question, answer, category
            - evidence: list of dia_ids containing the answer
    """
    with open(LOCOMO_DATA, "r") as f:
        data = json.load(f)
    
    conversations = []
    qa_pairs = []
    
    for conv_idx, conv in enumerate(data):
        # Extract speaker names
        speaker_a = conv.get("speaker_a", f"Speaker_A_{conv_idx}")
        speaker_b = conv.get("speaker_b", f"Speaker_B_{conv_idx}")
        
        # Extract sessions
        sessions = []
        session_num = 1
        while f"session_{session_num}" in conv:
            session_key = f"session_{session_num}"
            timestamp = conv.get(f"session_{session_num}_date_time", "")
            turns = conv[session_key]
            sessions.append({
                "key": session_key,
                "timestamp": timestamp,
                "turns": turns
            })
            session_num += 1
        
        # Extract QA pairs
        qa_items = conv.get("qa", [])
        for qa in qa_items:
            qa_pairs.append({
                "conversation_id": conv_idx,
                "question": qa.get("question", ""),
                "answer": qa.get("answer", ""),
                "category": qa.get("category", 0),
                "evidence": qa.get("evidence", [])
            })
        
        conversations.append({
            "id": conv_idx,
            "speaker_a": speaker_a,
            "speaker_b": speaker_b,
            "sessions": sessions,
            "qa_count": len(qa_items)
        })
    
    print(f"📊 Parsed: {len(conversations)} conversations, {len(qa_pairs)} QA pairs")
    for conv in conversations:
        print(f"   Conv {conv['id']}: {conv['speaker_a']} & {conv['speaker_b']}, "
              f"{len(conv['sessions'])} sessions, {conv['qa_count']} QA")
    
    # QA category breakdown
    cats = {}
    for qa in qa_pairs:
        c = qa["category"]
        cats[c] = cats.get(c, 0) + 1
    print(f"   QA categories: {cats}")
    
    return conversations, qa_pairs


# ============================================================
# STEP 3: Load conversations into HippoGraph
# ============================================================

def load_into_hippograph(conversations, api_url="http://localhost:5001", api_key=None):
    """Load LOCOMO sessions as notes into HippoGraph.
    
    Granularity options (configurable):
    - "session": One note per session (recommended, ~20 notes per conversation)
    - "turn": One note per dialogue turn (fine-grained, ~600 per conversation)
    
    For benchmark, we use a SEPARATE database to not pollute personal memory.
    TODO: Implement temp DB switching or use direct database access.
    """
    # TODO: Next session — implement loading
    # Option A: Direct DB insert (bypass API, fastest, no entity extraction overhead)
    # Option B: REST API calls (uses full pipeline including NER)
    # Option C: Batch import script (like skills import)
    
    # For each conversation, for each session:
    #   content = f"[{speaker}] {timestamp}\n" + all turns concatenated
    #   category = f"locomo-conv{conv_id}"
    #   Add as note with metadata
    
    print("⚠️  Load not yet implemented — next session")
    pass


# ============================================================
# STEP 4: Run retrieval evaluation
# ============================================================

def evaluate_retrieval(qa_pairs, api_url="http://localhost:5001", api_key=None):
    """Run QA queries through HippoGraph search, measure retrieval quality.
    
    Metrics:
    - Recall@k: Does the ground truth evidence appear in top-k results?
    - P@k: What fraction of top-k results are relevant?
    - MRR: Mean Reciprocal Rank of first relevant result
    
    For each QA pair:
    1. Send question to search_memory
    2. Get top-5 results
    3. Check if any result contains ground truth evidence (by dia_id match)
    4. Record hit/miss
    """
    # TODO: Next session — implement evaluation
    print("⚠️  Evaluation not yet implemented — next session")
    pass


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="LOCOMO Benchmark Adapter for HippoGraph")
    parser.add_argument("--download", action="store_true", help="Download LOCOMO dataset")
    parser.add_argument("--parse", action="store_true", help="Parse and show dataset stats")
    parser.add_argument("--load", action="store_true", help="Load into HippoGraph")
    parser.add_argument("--eval", action="store_true", help="Run evaluation")
    parser.add_argument("--all", action="store_true", help="Full pipeline")
    parser.add_argument("--api-url", default="http://localhost:5001", help="HippoGraph API URL")
    parser.add_argument("--api-key", default=None, help="API key")
    
    args = parser.parse_args()
    
    if args.download or args.all:
        download_dataset()
    
    if args.parse or args.all:
        conversations, qa_pairs = parse_dataset()
    
    if args.load or args.all:
        conversations, qa_pairs = parse_dataset()
        load_into_hippograph(conversations, args.api_url, args.api_key)
    
    if args.eval or args.all:
        _, qa_pairs = parse_dataset()
        evaluate_retrieval(qa_pairs, args.api_url, args.api_key)


if __name__ == "__main__":
    main()
