import pandas as pd
import pickle
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "processed" / "mall_customers_processed.csv"
MODEL_DIR = BASE_DIR / "models_artifacts"
MODEL_DIR.mkdir(exist_ok=True)


def train_and_save_model():
    print("=" * 60)
    print("Training Customer Segmentation Model...")
    print("=" * 60)
    
    # Load data
    print("\nLoading processed data...")
    try:
        df = pd.read_csv(DATA_PATH)
        print(f"Data loaded: {df.shape[0]} customers, {df.shape[1]} features")
    except FileNotFoundError:
        print(f"Error: Data file not found at {DATA_PATH}")
        print("   Please run the preprocessing notebook first:")
        print("   notebooks/01_eda_preprocessing.ipynb")
        return False
    
    # Prepare features
    print("\nPreparing features...")
    X = df[['Annual_Income', 'Spending_Score']]
    print(f"Features selected: {list(X.columns)}")
    
    # Scale features
    print("\nScaling features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    print("Features scaled using StandardScaler")
    
    # Train model
    print("\nTraining KMeans model...")
    optimal_k = 5
    kmeans = KMeans(
        n_clusters=optimal_k,
        init='k-means++',
        random_state=42,
        n_init=10
    )
    kmeans.fit(X_scaled)
    print(f"Model trained with {optimal_k} clusters")
    
    # Calculate inertia
    print(f"   Inertia (WCSS): {kmeans.inertia_:.2f}")
    
    # Save models
    print("\nSaving model artifacts...")
    
    # Save KMeans model
    kmeans_path = MODEL_DIR / "kmeans_model.pkl"
    with open(kmeans_path, 'wb') as f:
        pickle.dump(kmeans, f)
    print(f"KMeans model saved: {kmeans_path}")
    
    # Save Scaler
    scaler_path = MODEL_DIR / "scaler.pkl"
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"Scaler saved: {scaler_path}")
    
    # Add cluster predictions to data and save
    df['Cluster'] = kmeans.predict(X_scaled)
    cluster_names = {
        0: 'Average Customer',
        1: 'VIP / Whale',
        2: 'Young Trendsetter',
        3: 'High Earner Saver',
        4: 'Budget Conscious'
    }
    df['Cluster_Label'] = df['Cluster'].map(cluster_names)
    
    output_path = BASE_DIR / "notebooks" / "Marketing_Target_List.csv"
    df.to_csv(output_path, index=False)
    print(f"Clustered data saved: {output_path}")
    
    # Display cluster summary
    print("\n" + "=" * 60)
    print("Cluster Summary:")
    print("=" * 60)
    summary = df.groupby('Cluster_Label')[['Annual_Income', 'Spending_Score']].mean()
    summary['Count'] = df.groupby('Cluster_Label').size()
    print(summary.round(2))
    
    print("\n" + "=" * 60)
    print("Training completed successfully!")
    print("=" * 60)
    print("\nYou can now run the FastAPI application:")
    print("   python main.py")
    print("\n   Or using uvicorn:")
    print("   uvicorn main:app --reload")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    train_and_save_model()
