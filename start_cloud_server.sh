#!/bin/bash
# DeepRead Cloud Sync Server Startup Script

echo "===================================="
echo "DeepRead Cloud Sync Server"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Install dependencies if needed
echo "Checking dependencies..."
if ! pip3 show fastapi &> /dev/null; then
    echo "Installing FastAPI and dependencies..."
    pip3 install fastapi uvicorn[standard] requests pydantic
fi

# Start the server
echo ""
echo "Starting Cloud Sync Server..."
echo "Server will run at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 cloud_sync_server.py
