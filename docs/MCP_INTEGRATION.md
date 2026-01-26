# MCP Integration Guide

How to connect Neural Memory Graph to Claude.ai and other MCP clients.

## What is MCP?

Model Context Protocol (MCP) is Anthropic's standard for connecting AI assistants to external tools and data sources. Neural Memory Graph implements MCP via Server-Sent Events (SSE).

## Connecting to Claude.ai

### Prerequisites
- Running Neural Memory Graph server
- Public HTTPS URL (via ngrok, Cloudflare Tunnel, or reverse proxy)
- Your API key

### Steps

1. **Get your public URL**
   ```bash
   # Using ngrok
   ngrok http 5001
   # Note the https://xxx.ngrok-free.app URL
   ```

2. **Go to Claude.ai Settings**
   - Click your profile icon
   - Select "Settings"
   - Navigate to "Integrations"

3. **Add Remote MCP Server**
   - Click "Add Integration" or "Add Remote MCP Server"
   - Enter URL: `https://your-url.ngrok-free.app/sse?api_key=YOUR_KEY`
   - Save

4. **Test Connection**
   - Start a new conversation
   - Ask Claude: "What tools do you have available?"
   - You should see `search_memory`, `add_note`, etc.

## MCP Protocol Details

### Endpoint
```
POST /sse?api_key=YOUR_KEY
Content-Type: application/json
```

### Request Format (JSON-RPC 2.0)
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search_memory",
    "arguments": {"query": "test"}
  }
}
```

### Response Format
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{"type": "text", "text": "..."}]
  }
}
```

## Available Methods

| Method | Description |
|--------|-------------|
| `initialize` | Initialize connection, get server info |
| `tools/list` | List available tools |
| `tools/call` | Execute a tool |

## Testing with curl

```bash
# Initialize
curl -X POST "http://localhost:5001/sse?api_key=YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}'

# List tools
curl -X POST "http://localhost:5001/sse?api_key=YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'

# Search
curl -X POST "http://localhost:5001/sse?api_key=YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_memory","arguments":{"query":"test"}}}'
```

## Troubleshooting Connection

### "MCP server not responding"
- Check server is running: `curl http://localhost:5001/health`
- Verify ngrok tunnel is active
- Check API key is correct

### "Tools not appearing in Claude"
- Refresh Claude.ai page
- Remove and re-add the integration
- Check for typos in URL

### "Authentication failed"
- API key in URL must match `.env` file
- Special characters need URL encoding
- Try using Bearer token header instead
