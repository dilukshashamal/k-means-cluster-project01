"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Customer Segmentation API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # API
    API_PREFIX: str = "/api/v1"
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    MODEL_DIR: Path = BASE_DIR / "models_artifacts"
    DATA_DIR: Path = BASE_DIR / "data"
    
    # Model files
    KMEANS_MODEL_PATH: str = str(MODEL_DIR / "kmeans_model.pkl")
    SCALER_MODEL_PATH: str = str(MODEL_DIR / "scaler.pkl")
    PROCESSED_DATA_PATH: str = str(DATA_DIR / "processed" / "mall_customers_processed.csv")
    
    # CORS
    ALLOWED_ORIGINS: list = ["*"]
    
    # Cluster Names
    CLUSTER_NAMES: dict = {
        0: 'Average Customer',
        1: 'VIP / Whale',
        2: 'Young Trendsetter',
        3: 'High Earner Saver',
        4: 'Budget Conscious'
    }
    
    class Config:
        case_sensitive = True


settings = Settings()
