#!/bin/bash
# NEXUS Quick Start Script

echo ""
echo "  ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗"
echo "  ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝"
echo "  ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗"
echo "  ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║"
echo "  ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║"
echo "  ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝"
echo ""
echo "  Neural EXploration & Understanding System"
echo "  Team: ByteForge | ABB Accelerator 2026"
echo ""

cd "$(dirname "$0")"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.11+"
    exit 1
fi

echo "📦 Installing dependencies..."
pip install -r backend/requirements.txt -q

echo "🚀 Starting NEXUS server..."
echo "🌐 Dashboard → http://localhost:8000"
echo "📡 WebSocket  → ws://localhost:8000/ws"
echo "📋 API Docs   → http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop."
echo ""

cd backend
PYTHONPATH=".." python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
