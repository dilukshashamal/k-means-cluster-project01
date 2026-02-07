"""
Pydantic schemas for customer data validation
"""
from pydantic import BaseModel, Field, validator
from typing import Optional


class CustomerInput(BaseModel):
    """Schema for customer input data"""
    annual_income: float = Field(
        ..., 
        ge=0, 
        le=200,
        description="Annual Income in thousands ($k)",
        example=70.0
    )
    spending_score: int = Field(
        ..., 
        ge=1, 
        le=100,
        description="Spending Score (1-100)",
        example=75
    )
    
    @validator('annual_income')
    def validate_income(cls, v):
        if v < 0:
            raise ValueError('Annual income must be positive')
        return v
    
    @validator('spending_score')
    def validate_score(cls, v):
        if v < 1 or v > 100:
            raise ValueError('Spending score must be between 1 and 100')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "annual_income": 70.0,
                "spending_score": 75
            }
        }


class PredictionResponse(BaseModel):
    """Schema for prediction response"""
    cluster_id: int = Field(..., description="Numerical cluster ID")
    cluster_name: str = Field(..., description="Human-readable cluster name")
    annual_income: float = Field(..., description="Input annual income")
    spending_score: int = Field(..., description="Input spending score")
    description: str = Field(..., description="Cluster description")
    marketing_strategy: str = Field(..., description="Recommended marketing strategy")
    
    class Config:
        json_schema_extra = {
            "example": {
                "cluster_id": 1,
                "cluster_name": "VIP / Whale",
                "annual_income": 90.0,
                "spending_score": 85,
                "description": "High income, high spending customers",
                "marketing_strategy": "Premium products, exclusive offers, loyalty programs"
            }
        }


class ClusterStats(BaseModel):
    """Schema for cluster statistics"""
    cluster_id: int
    cluster_name: str
    count: int
    avg_income: float
    avg_spending_score: float
    avg_age: Optional[float] = None


class ModelInfo(BaseModel):
    """Schema for model information"""
    model_type: str = "KMeans Clustering"
    n_clusters: int = 5
    features_used: list = ["Annual_Income", "Spending_Score"]
    model_loaded: bool
    scaler_loaded: bool
