"""
main.py

FastAPI backend for Social Scope - handles post analysis requests
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analyze

# Create the FastAPI app instance
app = FastAPI(
    title="Social Scope API",
    description="AI-powered social media post analysis and engagement assistant",
    version="1.0.0"
)

# Allow requests from iOS app (update with your production domain later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the analyze router
app.include_router(analyze.router)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "message": "Social Scope API is up and running!",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "api": "operational",
            "ai": "operational"
        }
    }
