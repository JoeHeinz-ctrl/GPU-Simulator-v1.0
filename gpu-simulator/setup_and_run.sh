#!/bin/bash
# GPU Simulator - Automated Setup and Run Script for Linux/Mac
# This script will install dependencies and start the application

echo "========================================"
echo "GPU Simulator - Setup and Run"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    echo "Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "Mac: brew install python3"
    exit 1
fi

echo "[1/3] Python found:"
python3 --version
echo ""

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "[ERROR] pip3 is not available"
    echo "Ubuntu/Debian: sudo apt-get install python3-pip"
    echo "Mac: python3 -m ensurepip"
    exit 1
fi

echo "[2/3] Installing required packages..."
echo "This may take a few minutes on first run..."
echo ""

# Install dependencies
pip3 install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    echo "Please check your internet connection and try again"
    exit 1
fi

echo "[SUCCESS] All packages installed successfully!"
echo ""

echo "[3/3] Starting GPU Simulator..."
echo ""
echo "========================================"
echo "Server will start at: http://localhost:8000"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python3 run_server.py
