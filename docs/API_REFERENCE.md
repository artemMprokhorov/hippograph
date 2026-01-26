# API Reference

## MCP Endpoint

**URL:** `/sse`  
**Methods:** `GET`, `POST`  
**Authentication:** API key via URL parameter or Bearer token

### Authentication

```bash
# URL parameter
curl "http://localhost:5001/sse?api_key=YOUR_KEY" ...

# Bearer token
curl -H "Authorization: Bearer YOUR_KEY" http://localhost:5001/sse ...
```

---

## Tools

### search_memory

Search through notes using spreading activation algorithm.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| query | string | yes | - | Search query |
| limit | integer | no | 5 | Max results (1-20) |

**Example:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "search_memory",
    "arguments": {
      "query": "machine learning projects",
      "limit": 10
    }
  }
}
```

---

### add_note

Add new note with automatic entity extraction and linking.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| content | string | yes | - | Note content |
| category | string | no | "general" | Category tag |

**Example:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "add_note",
    "arguments": {
      "content": "Started working on neural network optimization",
      "category": "project"
    }
  }
}
```

---

### update_note

Update existing note by ID.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| note_id | integer | yes | Note ID |
| content | string | yes | New content |
| category | string | no | New category |

---

### delete_note

Delete note by ID.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| note_id | integer | yes | Note ID |

---

### neural_stats

Get statistics about stored notes, edges, and entities.

**Parameters:** None

**Response:**
```
📊 Neural Memory Graph Statistics

Total nodes: 150
Total edges: 420
Total entities: 85

Nodes by category:
  - general: 80
  - project: 45
  - reference: 25

Edges by type:
  - semantic: 300
  - entity: 120
```

---

### get_graph

Get graph connections for a specific note.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| note_id | integer | yes | Note ID |

---

## Health Check

**URL:** `/health`  
**Method:** `GET`  
**Authentication:** None required

```bash
curl http://localhost:5001/health
# {"status": "ok", "version": "2.0.0"}
```
