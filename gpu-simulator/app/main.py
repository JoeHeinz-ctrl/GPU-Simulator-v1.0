"""
Main FastAPI application for GPU Parallel Floating-Point Simulator
Educational web application demonstrating parallel programming concepts
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import sys
from pathlib import Path

# Add the app directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .routes import router

# Create FastAPI application
app = FastAPI(
    title="GPU Parallel Floating-Point Simulator",
    description="Educational web application demonstrating parallel programming concepts using GPU-style simulation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

# Get the directory containing this file
current_dir = Path(__file__).parent.parent

# Mount static files (frontend)
frontend_dir = current_dir / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    """
    Serve the main dashboard HTML file.
    
    Returns:
        HTML response with the simulator dashboard
    """
    html_file = frontend_dir / "index.html"
    if html_file.exists():
        return FileResponse(str(html_file))
    else:
        raise HTTPException(status_code=404, detail="Dashboard not found")

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        Status information about the application
    """
    return {
        "status": "healthy",
        "application": "GPU Parallel Floating-Point Simulator",
        "version": "1.0.0",
        "description": "Educational parallel programming demonstration"
    }

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Custom 404 handler for better user experience."""
    return {
        "success": False,
        "message": "Endpoint not found",
        "available_endpoints": [
            "/",
            "/api/generate-data",
            "/api/run-cpu-simulation", 
            "/api/run-gpu-simulation",
            "/api/performance-history",
            "/api/thread-block-info",
            "/health"
        ]
    }

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    """Custom 500 handler for better error reporting."""
    return {
        "success": False,
        "message": "Internal server error",
        "error": str(exc) if app.debug else "An unexpected error occurred"
    }

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )