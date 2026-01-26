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
- 🕸️ **Automatic Entity Extraction** — Identifies people, concepts, projects from your notes
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
git clone https://github.com/YOUR_USERNAME/neural-memory-graph.git
cd neural-memory-graph
cp .env.example .env
# Edit .env with your API key
```

### 2. Start with Docker

```bash
docker-compose up -d
```

### 3. Setup Remote Access

```bash
# Using ngrok
ngrok http 5001
```

### 4. Connect to AI Assistant

For Claude.ai:
1. Go to Settings → Integrations
2. Add Remote MCP Server
3. Enter: `https://your-subdomain.ngrok-free.app/sse?api_key=YOUR_KEY`

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
└── access tracking

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
       ├─→ Extract Entities (people, concepts, tech)
       ├─→ Find Related Notes (similarity + shared entities)
       └─→ Create Graph Edges (semantic connections)

Search Query
       ↓
    Embedding → Similarity Search → Spreading Activation
       ↓              ↓                      ↓
    Vector DB    Related Nodes      Connection Chains
```

---

## 🔒 Security

This is a research/personal project. Not audited for production use with sensitive data.

**Best Practices:**
- Use strong API keys (32+ characters)
- Rotate keys periodically
- Use HTTPS (never expose HTTP publicly)
- Restrict server access (firewall/VPN)

---

## 📖 Documentation

- [Setup Guide](docs/SETUP_GUIDE.md)
- [API Reference](docs/API_REFERENCE.md)
- [MCP Integration](docs/MCP_INTEGRATION.md)
- [Graph Features](docs/GRAPH_FEATURES.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

---

## 📦 Project Structure

```
neural-memory-graph/
├── src/
│   ├── server.py              # Flask app entry
│   ├── database.py            # Graph database layer
│   ├── graph_engine.py        # Spreading activation
│   ├── entity_extractor.py    # Entity extraction
│   ├── stable_embeddings.py   # Embedding model
│   └── mcp_sse_handler.py     # MCP protocol
├── scripts/
│   ├── backup.sh              # Database backup
│   ├── restore.sh             # Database restore
│   └── recompute_embeddings.py
├── docs/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

---

## 🤝 Contributing

Contributions welcome! This project explores semantic memory systems and knowledge graphs.

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
