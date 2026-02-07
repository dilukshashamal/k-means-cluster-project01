"""
Main FastAPI Application
Customer Segmentation ML Application with MVC Architecture
"""
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.controllers.api_controller import router as api_router
from app.controllers.view_controller import router as view_router
from app.models.ml_model import ml_model


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup: Load ML models
    print("=" * 50)
    print("Starting Customer Segmentation API...")
    print("=" * 50)
    
    success = ml_model.load_models()
    if success:
        print("ML models loaded successfully")
    else:
        print("Warning: ML models not loaded")
        print("   Please train the model using the Jupyter notebooks")
        print("   Then run the training script to save models")
    
    print("=" * 50)
    print(f"Application started: {settings.APP_NAME} v{settings.APP_VERSION}")
    print("=" * 50)
    
    yield
    
    # Shutdown
    print("\n" + "=" * 50)
    print("🛑 Shutting down Customer Segmentation API...")
    print("=" * 50)


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered customer segmentation using KMeans clustering",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount(
    "/static", 
    StaticFiles(directory=str(settings.BASE_DIR / "app" / "static")), 
    name="static"
)

# Include routers
app.include_router(api_router)  # API endpoints
app.include_router(view_router)  # HTML views

# Root endpoint redirect
@app.get("/api")
async def api_root():
    """API root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/api/v1/health"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )
