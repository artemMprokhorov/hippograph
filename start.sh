#!/bin/bash
set -e

echo "🚀 Starting Neural Memory Graph..."

# Configure ngrok with authtoken (from environment)
if [ -n "$NGROK_AUTHTOKEN" ]; then
    echo "🔑 Configuring ngrok authtoken..."
    ngrok config add-authtoken $NGROK_AUTHTOKEN
fi

# Start ngrok in background
echo "🌐 Starting ngrok tunnel..."
ngrok http --url=grand-beagle-reliably.ngrok-free.app 5000 > /dev/null 2>&1 &

# Wait for ngrok to start
sleep 3

# Start Flask server
echo "🧠 Starting Flask server..."
exec python server.py
