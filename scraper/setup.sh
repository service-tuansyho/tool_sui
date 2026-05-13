#!/bin/bash

# Setup script for SUI NFT Scraper

echo "================================"
echo "SUI NFT Scraper Setup"
echo "================================"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

echo ""

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found"
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ .env created. Please edit it with your API credentials:"
    echo ""
    echo "   nano .env"
    echo ""
else
    echo "✅ .env file already exists"
fi

echo ""
echo "================================"
echo "Setup Complete! 🎉"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API credentials"
echo "2. Run: python main.py --once (test run)"
echo "3. Or: python main.py (scheduled mode)"
echo ""
