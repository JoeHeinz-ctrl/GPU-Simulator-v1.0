"""
Server startup script for GPU Parallel Floating-Point Simulator
"""

import uvicorn
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 Starting GPU Parallel Floating-Point Simulator...")
    print("📚 Educational web application for parallel programming concepts")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📖 API documentation at: http://localhost:8000/docs")
    print("⏹️  Press Ctrl+C to stop the server\n")
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )