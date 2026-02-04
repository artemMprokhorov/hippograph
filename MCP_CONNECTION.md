# MCP Connection Configuration

## Current Setup (Updated: Feb 3-4, 2026)

### API Key
**Location:** Server only (`/Volumes/Balances/semantic-memory-v2/.env`)  
**Format:** `NEURAL_API_KEY=your_secure_key_here`  
**Note:** NEVER commit API keys to git - get from server .env file

### MCP Endpoint
```
https://grand-beagle-reliably.ngrok-free.app/sse2?api_key=[INSERT_KEY_HERE]
```

### Server Details
- **Local:** http://192.168.0.212:5001
- **SSH:** `ssh -i ~/.ssh/studio_key apple.holder.accgmail.com@192.168.0.212`
- **Docker:** `/usr/local/bin/docker-compose` in `/Volumes/Balances/semantic-memory-v2/`

### Available Tools (10)
1. search_memory
2. add_note
3. update_note
4. delete_note
5. neural_stats
6. get_graph
7. set_importance
8. find_similar
9. get_note_history ✨ NEW
10. restore_note_version ✨ NEW

### Security Notes
- Old key `neural_secure_key_2026_v2` was leaked briefly (Jan 26, 2026) and deactivated
- Current key deployed Feb 3-4, 2026
- All SESSION_*.md files in .gitignore
- Never commit .env or keys to repository

### Testing Connection
```bash
curl -s "https://grand-beagle-reliably.ngrok-free.app/sse2?api_key=[KEY]" \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}'
```
