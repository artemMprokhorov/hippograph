# Setup Guide

Complete guide to setting up Neural Memory Graph on your own infrastructure.

## Prerequisites

- **Docker** & **Docker Compose** v2.0+
- **4GB+ RAM** (embedding model requires ~2GB)
- **3GB+ disk space** (Docker image + model cache)
- **ngrok account** (for remote access) or reverse proxy setup

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/neural-memory-graph.git
cd neural-memory-graph
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and set a strong API key:

```bash
NEURAL_API_KEY=your_strong_random_key_here_32chars_minimum
```

### 3. Build and Start

```bash
docker-compose up -d
```

First start takes 2-5 minutes to download the embedding model.

### 4. Verify Installation

```bash
# Check container status
docker-compose ps

# Check logs
docker-compose logs -f

# Test health endpoint
curl http://localhost:5001/health
```

## Remote Access Setup

### Option A: ngrok (Easiest)

1. Install ngrok: https://ngrok.com/download
2. Start tunnel:
   ```bash
   ngrok http 5001
   ```
3. Use the HTTPS URL in Claude.ai

### Option B: Cloudflare Tunnel

1. Install cloudflared
2. Create tunnel:
   ```bash
   cloudflared tunnel create neural-memory
   cloudflared tunnel route dns neural-memory your-subdomain.yourdomain.com
   ```
3. Configure `~/.cloudflared/config.yml`:
   ```yaml
   tunnel: your-tunnel-id
   credentials-file: /path/to/credentials.json
   ingress:
     - hostname: your-subdomain.yourdomain.com
       service: http://localhost:5001
     - service: http_status:404
   ```

### Option C: Reverse Proxy (Caddy)

```
your-domain.com {
    reverse_proxy localhost:5001
}
```

## Connecting to Claude.ai

1. Go to Claude.ai → Settings → Integrations
2. Click "Add Remote MCP Server"
3. Enter URL: `https://your-domain/sse?api_key=YOUR_API_KEY`
4. Test connection

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues.

## Security Recommendations

1. **Use strong API keys** (32+ random characters)
2. **Rotate keys periodically**
3. **Use HTTPS** (never expose HTTP publicly)
4. **Firewall rules** to restrict access
5. **Regular backups** using `scripts/backup.sh`
