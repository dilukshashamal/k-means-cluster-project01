"""
Business logic layer for predictions
Handles the business rules and data processing
"""
from typing import Dict, List
import pandas as pd

from app.models.ml_model import ml_model
from app.schemas.customer import CustomerInput, PredictionResponse, ClusterStats
from app.core.config import settings


class PredictionService:
    """
    Service layer for customer segmentation predictions
    Contains business logic separate from controllers
    """
    
    @staticmethod
    def get_cluster_description(cluster_id: int) -> str:
        """
        Get detailed description for each cluster
        
        Args:
            cluster_id: The cluster ID
            
        Returns:
            Description string
        """
        descriptions = {
            0: "Average customers with moderate income and spending habits. Balanced segment.",
            1: "VIP customers with high income and high spending. Premium segment.",
            2: "Young trendsetters with moderate to low income but high spending scores.",
            3: "High earners who are conservative spenders. Save more than they spend.",
            4: "Budget-conscious customers with lower income and spending scores."
        }
        return descriptions.get(cluster_id, "Unknown segment")
    
    @staticmethod
    def get_marketing_strategy(cluster_id: int) -> str:
        """
        Get recommended marketing strategy for each cluster
        
        Args:
            cluster_id: The cluster ID
            
        Returns:
            Marketing strategy string
        """
        strategies = {
            0: "Standard promotions, seasonal offers, and loyalty programs. Focus on value for money.",
            1: "Premium products, exclusive offers, VIP experiences, and personalized service. No discount needed.",
            2: "Trendy products, social media marketing, influencer partnerships, and flexible payment options.",
            3: "Investment opportunities, quality products, long-term value propositions, and savings programs.",
            4: "Discounts, budget-friendly options, clearance sales, and basic product lines."
        }
        return strategies.get(cluster_id, "General marketing approach")
    
    @staticmethod
    async def predict_segment(customer_data: CustomerInput) -> PredictionResponse:
        """
        Predict customer segment based on income and spending score
        
        Args:
            customer_data: Customer input data
            
        Returns:
            PredictionResponse with cluster information
        """
        # Get prediction from ML model
        cluster_id, cluster_name = ml_model.predict(
            customer_data.annual_income,
            customer_data.spending_score
        )
        
        # Get business insights
        description = PredictionService.get_cluster_description(cluster_id)
        marketing_strategy = PredictionService.get_marketing_strategy(cluster_id)
        
        # Build response
        response = PredictionResponse(
            cluster_id=cluster_id,
            cluster_name=cluster_name,
            annual_income=customer_data.annual_income,
            spending_score=customer_data.spending_score,
            description=description,
            marketing_strategy=marketing_strategy
        )
        
        return response
    
    @staticmethod
    async def get_cluster_statistics() -> List[ClusterStats]:
        """
        Get statistics for all clusters from processed data
        
        Returns:
            List of cluster statistics
        """
        try:
            # Load processed data
            df = pd.read_csv(settings.PROCESSED_DATA_PATH)
            
            # If clusters are not in the data, we need to predict them
            if 'Cluster' not in df.columns:
                # Predict clusters for all customers
                X = df[['Annual_Income', 'Spending_Score']]
                X_scaled = ml_model.scaler.transform(X)
                df['Cluster'] = ml_model.kmeans.predict(X_scaled)
            
            # Calculate statistics
            stats = []
            for cluster_id in sorted(df['Cluster'].unique()):
                cluster_data = df[df['Cluster'] == cluster_id]
                
                stat = ClusterStats(
                    cluster_id=int(cluster_id),
                    cluster_name=settings.CLUSTER_NAMES.get(cluster_id, "Unknown"),
                    count=len(cluster_data),
                    avg_income=round(cluster_data['Annual_Income'].mean(), 2),
                    avg_spending_score=round(cluster_data['Spending_Score'].mean(), 2),
                    avg_age=round(cluster_data['Age'].mean(), 2) if 'Age' in df.columns else None
                )
                stats.append(stat)
            
            return stats
            
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Error calculating statistics: {e}")
            return []
    
    @staticmethod
    def get_all_cluster_info() -> Dict:
        """
        Get comprehensive information about all clusters
        
        Returns:
            Dictionary with cluster information
        """
        cluster_info = {}
        
        for cluster_id, cluster_name in settings.CLUSTER_NAMES.items():
            cluster_info[cluster_id] = {
                "name": cluster_name,
                "description": PredictionService.get_cluster_description(cluster_id),
                "marketing_strategy": PredictionService.get_marketing_strategy(cluster_id)
            }
        
        return cluster_info


# Service instance
prediction_service = PredictionService()
