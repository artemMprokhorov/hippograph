# Graph Viewer Security & Setup Guide

## ⚠️ Important Security Notice

The graph viewer (`graph_viewer_v2.html`) requires **API credentials** to connect to your Neural Memory server. **These credentials are NOT included in the repository** for security reasons.

## 🔒 Security Principles

1. **Local by Default**: The viewer connects to `localhost:5001` by default
2. **No Credentials in Git**: Never commit API keys or ngrok URLs to the repository
3. **Explicit Remote Access**: Remote access (via ngrok) must be explicitly configured by each user
4. **Browser Storage Only**: Saved credentials are stored in your browser's localStorage, NOT in git

## 🚀 Quick Start (Local Network)

### Step 1: Start Your Server

```bash
cd /path/to/hippograph
docker-compose up -d
```

Server will run on `http://localhost:5001`

### Step 2: Get Your API Key

Your API key is in `.env` file (not in git):

```bash
grep NEURAL_API_KEY .env
```

### Step 3: Open Graph Viewer

```bash
open graph_viewer_v2.html
```

### Step 4: Configure Connection

When the viewer opens, you'll see a configuration panel:
- **API Endpoint URL**: `http://localhost:5001/sse2`
- **API Key**: Paste your key from `.env`
- Click "Connect & Load"

The viewer will optionally save these credentials in your browser for convenience (never in git).

## 🌐 Remote Access (Optional)

If you want to access your graph from outside your local network:

### Step 1: Setup ngrok (Already in Docker)

Your server includes ngrok. Get your public URL:

```bash
docker logs hippograph | grep "Forwarding"
```

You'll see something like: `https://your-random-url.ngrok-free.app`

### Step 2: Use Remote URL in Viewer

In the configuration panel:
- **API Endpoint URL**: `https://your-random-url.ngrok-free.app/sse2`
- **API Key**: Your key from `.env`

### Security Notes for Remote Access

⚠️ **When using ngrok:**
- Your graph is accessible from internet
- API key is required (but transmitted over HTTPS)
- Consider using strong, unique API keys
- Rotate keys if exposed
- Monitor access logs

## 📝 For Other Users

If someone clones this repository and wants to visualize their own graph:

1. They must have their own Neural Memory server running
2. They must generate their own API key
3. They configure the viewer with their own credentials
4. Their data never touches GitHub

## 🔐 Best Practices

### DO:
✅ Keep API keys in `.env` file (in `.gitignore`)
✅ Use `localhost` for local-only access
✅ Generate strong API keys (see `MCP_CONNECTION.md`)
✅ Rotate keys if accidentally exposed

### DON'T:
❌ Never commit `.env` files
❌ Never hardcode credentials in HTML/JS
❌ Never share your API key publicly
❌ Never commit ngrok URLs to git

## 🛠️ Troubleshooting

### "Connection failed"
- Check server is running: `docker ps`
- Check API key is correct: `grep NEURAL_API_KEY .env`
- Check URL format: `http://localhost:5001/sse2` (with `/sse2`)

### "No nodes loaded"
- Check Neural Memory has data: Open MCP and run `neural_stats`
- Check browser console for errors (F12)

### "CORS errors"
- Only happens with remote URLs
- Ensure server allows CORS from viewer origin

## 📚 Related Documentation

- `MCP_CONNECTION.md` - API key generation and MCP setup
- `.env.example` - Environment variables template
- `README.md` - Overall project setup

## 🔄 Updates

**Last Updated**: Feb 4, 2026  
**Version**: 2.0 (Config-based, secure by default)
