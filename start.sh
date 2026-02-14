#!/bin/bash

# Startup script for SupaCall
# Usage: ./start.sh

echo "🚀 Starting SupaCall..."
echo ""

# Check if the virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found."
    echo "   Run: python3 -m venv venv"
    exit 1
fi

# Activate the virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if the .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found."
    echo "   Copy .env.example to .env and configure your variables."
    exit 1
fi

# Check dependencies
echo "🔍 Checking dependencies..."
pip install -q -r requirements.txt

# Run configuration tests (optional)
read -p "🧪 Run configuration tests? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python test_system.py
    if [ $? -ne 0 ]; then
        echo ""
        read -p "⚠️  Tests failed. Continue anyway? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
fi

# Start the server
echo ""
echo "🎉 Starting the server..."
echo ""
python main.py
