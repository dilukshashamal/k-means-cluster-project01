# Customer Segmentation ML Application

A production-ready **FastAPI** web application for customer segmentation using **Machine Learning (KMeans Clustering)**. Built with **MVC architecture** following industry best practices.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Architecture](#-architecture)
- [Customer Segments](#-customer-segments)
- [Technologies](#-technologies)

## Features

- **Machine Learning**: KMeans clustering for customer segmentation
- **FastAPI Backend**: High-performance async API
- **Modern UI**: Beautiful, responsive HTML interface
- **Real-time Predictions**: Instant customer segment classification
- **MVC Architecture**: Clean separation of concerns
- **Business Intelligence**: Marketing strategy recommendations
- **Input Validation**: Pydantic schemas for data validation
- **Auto Documentation**: Swagger UI and ReDoc
- **Best Practices**: Following industry standards

## 📁 Project Structure

```
practice/
├── app/                          # Main application package
│   ├── __init__.py              # Package initialization
│   ├── core/                    # Core configuration
│   │   ├── __init__.py
│   │   └── config.py           # Application settings
│   ├── models/                  # ML Models (Model layer)
│   │   ├── __init__.py
│   │   └── ml_model.py         # KMeans model handler
│   ├── schemas/                 # Data validation schemas
│   │   ├── __init__.py
│   │   └── customer.py         # Pydantic models
│   ├── services/                # Business logic (Service layer)
│   │   ├── __init__.py
│   │   └── prediction_service.py
│   ├── controllers/             # Request handlers (Controller layer)
│   │   ├── __init__.py
│   │   ├── api_controller.py   # REST API endpoints
│   │   └── view_controller.py  # HTML views
│   ├── templates/               # Jinja2 templates (View layer)
│   │   ├── index.html          # Home page
│   │   └── about.html          # About page
│   ├── static/                  # Static assets
│   │   ├── css/
│   │   │   └── style.css       # Styles
│   │   └── js/
│   │       └── app.js          # Frontend JavaScript
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       └── helpers.py
├── data/                        # Data directory
│   ├── raw/                    # Raw data
│   │   └── mall_customers.csv
│   └── processed/              # Processed data
│       └── mall_customers_processed.csv
├── models_artifacts/           # Saved ML models
│   ├── kmeans_model.pkl       # Trained KMeans model
│   └── scaler.pkl             # Feature scaler
├── notebooks/                  # Jupyter notebooks
│   ├── 01_eda_preprocessing.ipynb
│   └── 02_modeling_evaluation.ipynb
├── main.py                     # Application entry point
├── train_model.py             # Model training script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Step 1: Clone or Navigate to Project

```bash
cd d:\AIML\practice
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Train the Model

First, you need to train the KMeans model and save the artifacts:

**Option A: Using Jupyter Notebooks (Recommended for first-time users)**

```bash
# Launch Jupyter
jupyter notebook

# Open and run these notebooks in order:
# 1. notebooks/01_eda_preprocessing.ipynb
# 2. notebooks/02_modeling_evaluation.ipynb
```

**Option B: Using Training Script**

```bash
# This requires processed data from the notebooks
python train_model.py
```

The training script will:

- Load processed customer data
- Train KMeans clustering model
- Save model artifacts to `models_artifacts/`
- Generate customer segment labels

### Step 2: Run the Application

```bash
# Start the FastAPI server
python main.py

# Or using uvicorn directly:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Access the Application

- **Web Interface**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **API Documentation (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

## API Documentation

### REST API Endpoints

#### 1. Predict Customer Segment

```http
POST /api/v1/predict
Content-Type: application/json

{
  "annual_income": 70.0,
  "spending_score": 75
}
```

**Response:**

```json
{
  "cluster_id": 1,
  "cluster_name": "VIP / Whale",
  "annual_income": 70.0,
  "spending_score": 75,
  "description": "High income, high spending customers",
  "marketing_strategy": "Premium products, exclusive offers..."
}
```

#### 2. Get Cluster Statistics

```http
GET /api/v1/clusters
```

#### 3. Get Cluster Information

```http
GET /api/v1/clusters/info
```

#### 4. Get Model Information

```http
GET /api/v1/model/info
```

#### 5. Health Check

```http
GET /api/v1/health
```

### Using Python Requests

```python
import requests

# Predict customer segment
response = requests.post(
    "http://localhost:8000/api/v1/predict",
    json={
        "annual_income": 90.0,
        "spending_score": 85
    }
)
result = response.json()
print(f"Segment: {result['cluster_name']}")
```

### Using cURL

```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
     -H "Content-Type: application/json" \
     -d '{"annual_income": 90.0, "spending_score": 85}'
```

## 🏗️ Architecture

This application follows the **MVC (Model-View-Controller)** architectural pattern:

### Model Layer (`app/models/`)

- Handles ML model loading, predictions, and persistence
- Manages KMeans clustering model and StandardScaler
- Provides model metadata and cluster centroids

### View Layer (`app/templates/`, `app/static/`)

- Jinja2 templates for HTML rendering
- CSS for styling
- JavaScript for interactivity and API calls

### Controller Layer (`app/controllers/`)

- **API Controller**: REST API endpoints
- **View Controller**: HTML page rendering
- Request/response handling
- Input validation

### Service Layer (`app/services/`)

- Business logic and rules
- Prediction processing
- Cluster descriptions and marketing strategies
- Statistics calculation

### Core Configuration (`app/core/`)

- Application settings
- Environment variables
- Path configurations

### Schemas (`app/schemas/`)

- Pydantic models for validation
- Request/response schemas
- Type safety

## Customer Segments

The model identifies **5 distinct customer segments**:

| Segment               | Income       | Spending | Description           | Marketing Strategy                         |
| --------------------- | ------------ | -------- | --------------------- | ------------------------------------------ |
| **Average Customer**  | Moderate     | Moderate | Balanced shoppers     | Standard promotions, loyalty programs      |
| **VIP / Whale**       | High         | High     | Premium customers     | Exclusive offers, VIP experiences          |
| **Young Trendsetter** | Low-Moderate | High     | Fashion-conscious     | Trendy products, social media marketing    |
| **High Earner Saver** | High         | Low      | Conservative spenders | Quality products, investment opportunities |
| **Budget Conscious**  | Low          | Low      | Price-sensitive       | Discounts, clearance sales                 |

## Technologies

### Backend

- **FastAPI** - Modern, fast web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **scikit-learn** - Machine Learning
- **pandas** - Data manipulation
- **NumPy** - Numerical computing

### Frontend

- **HTML5** - Semantic markup
- **CSS3** - Modern styling with gradients and animations
- **JavaScript** - Async API calls and DOM manipulation
- **Jinja2** - Template engine

### ML/Data Science

- **KMeans Clustering** - Customer segmentation algorithm
- **StandardScaler** - Feature normalization
- **matplotlib** - Visualization (notebooks)
- **seaborn** - Statistical visualization (notebooks)

## Configuration

Application settings can be configured in [app/core/config.py](app/core/config.py):

```python
class Settings(BaseSettings):
    APP_NAME: str = "Customer Segmentation API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"
    # ... more settings
```

## Model Performance

- **Algorithm**: KMeans with k-means++ initialization
- **Number of Clusters**: 5 (optimized using Elbow Method)
- **Features**: Annual Income, Spending Score
- **Preprocessing**: StandardScaler normalization
- **Validation**: Silhouette Score

## 🚦 Testing

### Manual Testing

1. **Test via Web Interface**: Navigate to http://localhost:8000
2. **Test via API Docs**: Go to http://localhost:8000/docs
3. **Test via Command Line**:

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Prediction
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"annual_income": 90, "spending_score": 85}'
```

## 🤝 Contributing

This is a learning project. Feel free to:

- Add more features
- Improve the UI/UX
- Add more ML models
- Implement authentication
- Add database integration

## 📝 License

This project is created for educational purposes.

## 👨‍💻 Author

**AI ML Team**

## 🙏 Acknowledgments

- FastAPI documentation
- scikit-learn documentation
- Mall Customers dataset

## 📞 Support

For issues or questions:

1. Check the API documentation at `/docs`
2. Review the code comments
3. Check application logs

## 🔮 Future Enhancements

- [ ] Add database integration (PostgreSQL/MongoDB)
- [ ] Implement user authentication (JWT)
- [ ] Add more ML models (DBSCAN, Hierarchical)
- [ ] Create batch prediction endpoint
- [ ] Add model retraining endpoint
- [ ] Implement A/B testing framework
- [ ] Add monitoring and logging (Prometheus/Grafana)
- [ ] Dockerize the application
- [ ] Add CI/CD pipeline
- [ ] Deploy to cloud (AWS/Azure/GCP)

---

**⭐ If you found this helpful, please star the repository!**
"# k-means-cluster-project01" 
