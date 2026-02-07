"""
API Controllers - Handle HTTP requests and responses
RESTful API endpoints for the application
"""
from fastapi import APIRouter, HTTPException, status
from typing import List

from app.schemas.customer import (
    CustomerInput, 
    PredictionResponse, 
    ClusterStats,
    ModelInfo
)
from app.services.prediction_service import prediction_service
from app.models.ml_model import ml_model


# Create API router
router = APIRouter(prefix="/api/v1", tags=["Customer Segmentation API"])


@router.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict customer segment",
    description="Predict which customer segment a person belongs to based on their income and spending score"
)
async def predict_customer_segment(customer: CustomerInput):
    """
    Predict customer segment endpoint
    
    - **annual_income**: Annual income in thousands of dollars (e.g., 70 means $70k)
    - **spending_score**: Spending score from 1 to 100
    
    Returns the predicted cluster with marketing recommendations
    """
    try:
        prediction = await prediction_service.predict_segment(customer)
        return prediction
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Model not available: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction error: {str(e)}"
        )


@router.get(
    "/clusters",
    response_model=List[ClusterStats],
    summary="Get cluster statistics",
    description="Get statistical information about all customer segments"
)
async def get_cluster_statistics():
    """
    Get statistics for all clusters from the training data
    """
    try:
        stats = await prediction_service.get_cluster_statistics()
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching statistics: {str(e)}"
        )


@router.get(
    "/clusters/info",
    summary="Get cluster information",
    description="Get detailed information about all customer segments"
)
async def get_cluster_info():
    """
    Get comprehensive information about all clusters including descriptions and strategies
    """
    try:
        info = prediction_service.get_all_cluster_info()
        return info
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching cluster info: {str(e)}"
        )


@router.get(
    "/model/info",
    response_model=ModelInfo,
    summary="Get model information",
    description="Get information about the loaded ML model"
)
async def get_model_info():
    """
    Get model metadata and status
    """
    try:
        info = ml_model.get_model_info()
        return ModelInfo(**info)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching model info: {str(e)}"
        )


@router.get(
    "/health",
    summary="Health check",
    description="Check if the API is running and models are loaded"
)
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "model_loaded": ml_model.is_loaded,
        "message": "Customer Segmentation API is running"
    }
