#!/bin/bash

# Development startup script for FastAPI AI Service
echo "🚀 Starting FastAPI AI Service Development Environment"
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run: python -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️ .env file not found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env file with your API keys before running the service."
    exit 1
fi

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Start the development server
echo "🌟 Starting FastAPI development server..."
echo "📍 Server will be available at: http://localhost:8000"
echo "📖 API docs will be available at: http://localhost:8000/docs"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000
