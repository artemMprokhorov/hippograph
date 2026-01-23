# Neural Memory MCP v2

**Advanced Personal Knowledge Management with Semantic Graph Memory**

A self-hosted MCP (Model Context Protocol) server that adds persistent, graph-based semantic memory to Claude and other AI assistants. Store notes, discover connections automatically, and search by meaning across your knowledge base.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)

---

## ✨ What's New in v2

**Graph-Based Memory Architecture:**
- 🕸️ **Automatic Entity Extraction** — Identifies people, concepts, projects from your notes
- 🔗 **Semantic Connections** — Discovers related notes through shared entities
- 📊 **Knowledge Graph** — View how your ideas connect and relate
- 🎯 **Spreading Activation Search** — Find notes through association chains, not just keywords

**Enhanced Features:**
- 384-dimensional semantic embeddings (all-MiniLM-L6-v2)
- SQLite graph database with nodes, edges, and entities
- Automatic relationship detection between notes
- MCP protocol integration for Claude.ai

---

## 🎯 Real-World Use Cases

- 📚 **Long-term Projects** — AI remembers architectural decisions, coding preferences, context across sessions
- 🔬 **Research Workflows** — Build semantic knowledge base from papers, connect related findings automatically
- 💼 **Business Context** — Maintain understanding of workflows, track project relationships
- 🧠 **Personal Knowledge Management** — Second brain with automatic idea connections
- 🛠️ **Developer Productivity** — Remember codebase details, track related bugs and solutions

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- ngrok account (for remote access)
- Python 3.9+ (for local development)

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

### 3. Setup ngrok Tunnel

```bash
ngrok http 5000
```

### 4. Connect to Claude.ai

1. Go to Claude.ai → Settings → Integrations
2. Add Remote MCP Server
3. Enter: `https://your-subdomain.ngrok-free.app/sse2?api_key=YOUR_KEY`

---

## 📋 System Requirements

### Minimum
- **RAM:** 4GB (embedding model ~2GB)
- **Disk:** 3GB free (Docker image + models)
- **CPU:** Modern x64/ARM64 processor
- **OS:** Linux, macOS, Windows (Docker required)

### Recommended
- **RAM:** 8GB+
- **Disk:** 5GB+ for larger knowledge bases
- **SSD:** Faster embedding operations

### Tested On
- macOS Apple Silicon (M3 Ultra)

### Should Work On
- Linux with Docker support
- Windows 11 + WSL2 + Docker Desktop
- macOS Intel/ARM

---

## 🛠️ Available MCP Tools

| Tool | Description |
|------|-------------|
| `search_memory` | Semantic search through knowledge graph |
| `add_note` | Save note with auto-embedding and entity extraction |
| `update_note` | Modify existing note, recompute connections |
| `delete_note` | Remove note and its graph relationships |
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

## 🔒 Security Note

This is a research project. While it runs on your infrastructure, it's not audited for production use with sensitive data. Use at your own risk.

**Best Practices:**
- Use strong API keys (32+ characters)
- Rotate keys periodically
- Restrict server access (firewall/VPN)
- Monitor access logs

---

## 📖 Documentation

- [Graph Features Guide](docs/GRAPH_FEATURES.md)
- [MCP Integration](docs/MCP_INTEGRATION.md)
- [API Reference](docs/API_REFERENCE.md)
- [Docker Setup](docs/DOCKER_SETUP.md)

---

## 📦 Project Structure

```
neural-memory-mcp-v2/
├── src/
│   ├── server.py              # Flask app entry
│   ├── database.py            # Graph database layer
│   ├── graph_engine.py        # Spreading activation
│   ├── entity_extractor.py    # NER for entities
│   ├── stable_embeddings.py   # Embedding model
│   └── mcp_sse_handler.py     # MCP protocol
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
