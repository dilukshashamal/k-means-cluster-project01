"""
View Controllers - Handle HTML template rendering
Serves the web interface
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.models.ml_model import ml_model


# Create router for views
router = APIRouter(tags=["Web Interface"])

# Setup templates
templates = Jinja2Templates(directory=str(settings.BASE_DIR / "app" / "templates"))


@router.get("/", response_class=HTMLResponse, summary="Home page")
async def home(request: Request):
    """
    Render the main application page
    """
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": settings.APP_NAME,
            "app_version": settings.APP_VERSION,
            "model_loaded": ml_model.is_loaded
        }
    )


@router.get("/about", response_class=HTMLResponse, summary="About page")
async def about(request: Request):
    """
    Render the about page with model information
    """
    model_info = ml_model.get_model_info()
    cluster_names = settings.CLUSTER_NAMES
    
    return templates.TemplateResponse(
        "about.html",
        {
            "request": request,
            "app_name": settings.APP_NAME,
            "model_info": model_info,
            "cluster_names": cluster_names
        }
    )
