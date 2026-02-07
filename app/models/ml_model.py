"""
Machine Learning Model Handler
Handles model loading, prediction, and persistence
"""
import pickle
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from app.core.config import settings


class CustomerSegmentationModel:
    """
    Handles the KMeans clustering model for customer segmentation
    """
    
    def __init__(self):
        self.kmeans: Optional[KMeans] = None
        self.scaler: Optional[StandardScaler] = None
        self.cluster_names = settings.CLUSTER_NAMES
        self.is_loaded = False
    
    def load_models(self) -> bool:
        """
        Load the trained KMeans model and scaler from disk
        
        Returns:
            bool: True if models loaded successfully, False otherwise
        """
        try:
            # Load KMeans model
            with open(settings.KMEANS_MODEL_PATH, 'rb') as f:
                self.kmeans = pickle.load(f)
            
            # Load Scaler
            with open(settings.SCALER_MODEL_PATH, 'rb') as f:
                self.scaler = pickle.load(f)
            
            self.is_loaded = True
            print(f"Models loaded successfully from {settings.MODEL_DIR}")
            return True
            
        except FileNotFoundError as e:
            print(f"Model files not found: {e}")
            print("Please train the model first using the notebook")
            self.is_loaded = False
            return False
        except Exception as e:
            print(f"Error loading models: {e}")
            self.is_loaded = False
            return False
    
    def save_models(self, kmeans: KMeans, scaler: StandardScaler) -> bool:
        """
        Save the trained models to disk
        
        Args:
            kmeans: Trained KMeans model
            scaler: Fitted StandardScaler
            
        Returns:
            bool: True if saved successfully
        """
        try:
            # Create model directory if it doesn't exist
            Path(settings.MODEL_DIR).mkdir(parents=True, exist_ok=True)
            
            # Save models
            with open(settings.KMEANS_MODEL_PATH, 'wb') as f:
                pickle.dump(kmeans, f)
            
            with open(settings.SCALER_MODEL_PATH, 'wb') as f:
                pickle.dump(scaler, f)
            
            self.kmeans = kmeans
            self.scaler = scaler
            self.is_loaded = True
            
            print(f"Models saved successfully to {settings.MODEL_DIR}")
            return True
            
        except Exception as e:
            print(f"Error saving models: {e}")
            return False
    
    def predict(self, annual_income: float, spending_score: float) -> Tuple[int, str]:
        """
        Predict the customer segment
        
        Args:
            annual_income: Annual income in thousands
            spending_score: Spending score (1-100)
            
        Returns:
            Tuple of (cluster_id, cluster_name)
        """
        if not self.is_loaded:
            raise RuntimeError("Models not loaded. Please load models first.")
        
        # Create dataframe
        new_data = pd.DataFrame(
            [[annual_income, spending_score]], 
            columns=['Annual_Income', 'Spending_Score']
        )
        
        # Scale the data
        new_scaled = self.scaler.transform(new_data)
        
        # Predict cluster
        cluster_id = int(self.kmeans.predict(new_scaled)[0])
        cluster_name = self.cluster_names.get(cluster_id, "Unknown")
        
        return cluster_id, cluster_name
    
    def get_cluster_centroids(self) -> pd.DataFrame:
        """
        Get the cluster centroids in original scale
        
        Returns:
            DataFrame with centroid coordinates
        """
        if not self.is_loaded:
            raise RuntimeError("Models not loaded.")
        
        # Inverse transform to get original scale
        centroids = self.scaler.inverse_transform(self.kmeans.cluster_centers_)
        
        df = pd.DataFrame(
            centroids,
            columns=['Annual_Income', 'Spending_Score']
        )
        df['Cluster'] = range(len(df))
        df['Cluster_Name'] = df['Cluster'].map(self.cluster_names)
        
        return df
    
    def get_model_info(self) -> dict:
        """
        Get information about the loaded model
        
        Returns:
            Dictionary with model metadata
        """
        return {
            "model_type": "KMeans Clustering",
            "n_clusters": len(self.cluster_names),
            "features_used": ["Annual_Income", "Spending_Score"],
            "model_loaded": self.is_loaded,
            "scaler_loaded": self.scaler is not None,
            "cluster_names": self.cluster_names
        }


# Global model instance (Singleton pattern)
ml_model = CustomerSegmentationModel()
