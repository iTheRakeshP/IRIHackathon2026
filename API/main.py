"""
In-Force Annuity Review Platform - FastAPI Backend
Hackathon PoC - February 2026
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import policies, clients, products, ai, replacement_transactions
from app.config import settings

app = FastAPI(
    title="Annuity Review API",
    description="In-Force Annuity Review Platform with AI Copilot - Hackathon PoC",
    version="1.0.0"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(policies.router, prefix="/api", tags=["policies"])
app.include_router(clients.router, prefix="/api", tags=["clients"])
app.include_router(products.router, prefix="/api", tags=["products"])
app.include_router(ai.router)
app.include_router(replacement_transactions.router, prefix="/api", tags=["replacement-transactions"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Annuity Review API",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "api": "operational",
        "data_source": "json_files"
    }
