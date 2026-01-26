<p align="center">
  <img src="logo.svg" width="200" alt="Neural Memory Graph Logo">
</p>

# Neural Memory Graph

**Personal Knowledge Management with Semantic Graph Memory**

A self-hosted MCP (Model Context Protocol) server that adds persistent, graph-based semantic memory to AI assistants. Store notes, discover connections automatically, and search by meaning across your knowledge base.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)

---

## ✨ Features

**Graph-Based Memory Architecture:**
- 🕸️ **Automatic Entity Extraction** — Identifies people, concepts, projects from your notes (regex + spaCy NER)
- 🔗 **Semantic Connections** — Discovers related notes through shared entities
- 📊 **Knowledge Graph** — View how your ideas connect and relate
- 🎯 **Spreading Activation Search** — Find notes through association chains, not just keywords

**Technical Features:**
- 384-dimensional semantic embeddings (all-MiniLM-L6-v2)
- SQLite graph database with nodes, edges, and entities
- Automatic relationship detection between notes
- MCP protocol integration for AI assistants
- **Temporal decay** for recency-weighted search
- **Importance scoring** (critical/normal/low) with activation boost
- **Duplicate detection** with similarity thresholds (blocks >95%, warns >90%)
- **spaCy NER** for advanced entity extraction (people, organizations, locations)
- Docker-ready deployment

---

## 🎯 Use Cases

- 📚 **Long-term Projects** — Remember architectural decisions, preferences, context across sessions
- 🔬 **Research Workflows** — Build semantic knowledge base, connect related findings automatically
- 💼 **Business Context** — Maintain understanding of workflows, track project relationships
- 🧠 **Personal Knowledge Management** — Second brain with automatic idea connections
- 🛠️ **Developer Productivity** — Track codebase details, related bugs and solutions

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- ngrok account (for remote access) or reverse proxy
- Python 3.9+ (for local development only)

### 1. Clone & Configure

```bash
git clone https://github.com/artemMprokhorov/neural-memory-graph.git
cd neural-memory-graph
cp .env.example .env
# Edit .env and set a strong NEURAL_API_KEY
```

### 2. Start with Docker

```bash
docker-compose up -d
```

The server will:
- Download embedding models (~2GB on first run)
- Download spaCy model for entity extraction
- Initialize SQLite database
- Start on port 5001

### 3. Setup Remote Access

```bash
# Using ngrok (recommended for testing)
ngrok http 5001
# Note your https://xxx.ngrok-free.app URL
```

### 4. Connect to Claude.ai

1. Go to Settings → Integrations
2. Add Remote MCP Server
3. Enter: `https://your-subdomain.ngrok-free.app/sse?api_key=YOUR_API_KEY`
4. Test: Ask Claude "What tools do you have available?"

---

## 📋 System Requirements

### Minimum
- **RAM:** 4GB (embedding model ~2GB)
- **Disk:** 3GB free (Docker image + models)
- **CPU:** Modern x64/ARM64 processor
- **OS:** Linux, macOS, Windows (with Docker)

### Recommended
- **RAM:** 8GB+
- **Disk:** 5GB+ for larger knowledge bases
- **SSD:** Faster embedding operations

---

## 🛠️ Available MCP Tools

| Tool | Description |
|------|-------------|
| `search_memory` | Semantic search with spreading activation |
| `add_note` | Save note with auto-embedding, entity extraction, and duplicate detection |
| `update_note` | Modify existing note, recompute connections |
| `delete_note` | Remove note and its graph relationships |
| `set_importance` | Set note importance (critical/normal/low) for search ranking |
| `find_similar` | Check for similar notes before adding (deduplication) |
| `neural_stats` | View memory statistics and graph metrics |
| `get_graph` | Get connections for a specific note |

---

## 🏗️ Architecture

### Graph Database Schema

```
nodes (notes)
├── id, content, category
├── timestamp, embedding
├── importance, last_accessed
└── temporal decay tracking

edges (connections)
├── source_id → target_id
├── weight, edge_type
└── created_at

entities (extracted concepts)
├── name, entity_type
└── linked to multiple nodes

node_entities (relationships)
└── many-to-many linking
```

### How It Works

```
┌─────────────┐
│   Add Note  │
└──────┬──────┘
       │
       ├─→ Generate Embedding (384D vector)
       ├─→ Extract Entities (spaCy NER + regex)
       ├─→ Find Related Notes (similarity + shared entities)
       ├─→ Check Duplicates (>95% blocks, >90% warns)
       └─→ Create Graph Edges (semantic connections)

Search Query
       ↓
    Embedding → Similarity Search → Spreading Activation
       ↓              ↓                      ↓
    Vector DB    Related Nodes      Connection Chains
                                           ↓
                                  Temporal Decay + Importance Boost
```

---

## 🔧 Configuration

Edit `.env` to customize behavior:

```bash
# Entity extraction mode
ENTITY_EXTRACTOR=spacy  # Options: regex, spacy

# Spreading activation
ACTIVATION_ITERATIONS=3
ACTIVATION_DECAY=0.7

# Temporal decay (days)
HALF_LIFE_DAYS=30

# Deduplication threshold
SIMILARITY_THRESHOLD=0.5
```

---

## 🔒 Security

**⚠️ Research/Personal Project Notice:**  
This is not audited for production use with sensitive data.

**Best Practices:**
- Use strong API keys (32+ characters, alphanumeric + symbols)
- Rotate keys periodically
- Use HTTPS (never expose HTTP publicly)
- Restrict server access (firewall/VPN)
- Review [SECURITY.md](SECURITY.md) for details

---

## 📖 Documentation

- [Setup Guide](docs/SETUP_GUIDE.md) — Detailed installation and configuration
- [API Reference](docs/API_REFERENCE.md) — Complete MCP tools documentation
- [MCP Integration](docs/MCP_INTEGRATION.md) — Connect to Claude.ai and other clients
- [Graph Features](docs/GRAPH_FEATURES.md) — Spreading activation and entity linking
- [Troubleshooting](docs/TROUBLESHOOTING.md) — Common issues and solutions

---

## 📦 Project Structure

```
neural-memory-graph/
├── src/
│   ├── server.py              # Flask app entry
│   ├── database.py            # Graph database layer
│   ├── graph_engine.py        # Spreading activation
│   ├── entity_extractor.py    # spaCy NER + regex extraction
│   ├── stable_embeddings.py   # Embedding model
│   └── mcp_sse_handler.py     # MCP protocol
├── scripts/
│   ├── backup.sh              # Database backup
│   ├── restore.sh             # Database restore
│   └── recompute_embeddings.py
├── docs/                      # Documentation
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

---

## 🤝 Contributing

Contributions welcome! This project explores semantic memory systems and knowledge graphs.

**Areas for Contribution:**
- Additional entity extraction methods (LLM-based)
- Graph visualization tools
- Performance optimizations
- Documentation improvements

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👥 Authors

**Artem Prokhorov** — System architecture, infrastructure, research direction  
**Claude** (Anthropic) — Co-developer, graph algorithms, documentation

*Built through human-AI collaboration*

---

**Made with 🧠 by Artem Prokhorov & Claude**
