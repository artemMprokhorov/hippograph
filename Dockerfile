FROM python:3.11-slim

WORKDIR /app

# Install system dependencies and ngrok
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    wget \
    unzip \
    && wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz \
    && tar xvzf ngrok-v3-stable-linux-arm64.tgz -C /usr/local/bin \
    && rm ngrok-v3-stable-linux-arm64.tgz \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model for entity extraction
RUN python -m spacy download en_core_web_sm

# Copy source code and startup script
COPY src/ ./
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Create data directory
RUN mkdir -p /app/data

# Environment variables
ENV DB_PATH=/app/data/memory.db
ENV FLASK_PORT=5000
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

CMD ["/app/start.sh"]
