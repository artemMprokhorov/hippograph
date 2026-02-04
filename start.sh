#!/bin/bash
set -e

echo "🚀 Starting HippoGraph..."

# Start nginx for web viewer
echo "🌐 Starting nginx for graph viewer..."
service nginx start

# Configure ngrok with authtoken (from environment)
if [ -n "$NGROK_AUTHTOKEN" ]; then
    echo "🔑 Configuring ngrok authtoken..."
    ngrok config add-authtoken $NGROK_AUTHTOKEN
fi

# Start ngrok in background
echo "🔗 Starting ngrok tunnel..."
ngrok http --url=grand-beagle-reliably.ngrok-free.app 5000 > /dev/null 2>&1 &

# Wait for ngrok to start
sleep 3

echo "📊 Graph viewer available at:"
echo "   - Local: http://localhost:5002"
echo "   - Network: http://192.168.0.212:5002"
echo "🧠 API server:"
echo "   - Local: http://localhost:5001"
echo "   - Network: http://192.168.0.212:5001"
echo "   - Internet: https://grand-beagle-reliably.ngrok-free.app"

# Start Flask server
echo "▶️  Starting Flask MCP server..."
exec python server.py
