import requests
import json


BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1"


def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("Testing Health Endpoint...")
    print("="*60)
    
    response = requests.get(f"{API_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_model_info():
    """Test model info endpoint"""
    print("\n" + "="*60)
    print("Testing Model Info Endpoint...")
    print("="*60)
    
    response = requests.get(f"{API_URL}/model/info")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_prediction():
    """Test prediction endpoint"""
    print("\n" + "="*60)
    print("Testing Prediction Endpoint...")
    print("="*60)
    
    test_cases = [
        {"annual_income": 90.0, "spending_score": 85, "expected": "VIP / Whale"},
        {"annual_income": 30.0, "spending_score": 80, "expected": "Young Trendsetter"},
        {"annual_income": 100.0, "spending_score": 20, "expected": "High Earner Saver"},
        {"annual_income": 25.0, "spending_score": 25, "expected": "Budget Conscious"},
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"   Input: Income=${test_case['annual_income']}k, Score={test_case['spending_score']}")
        
        response = requests.post(
            f"{API_URL}/predict",
            json={
                "annual_income": test_case["annual_income"],
                "spending_score": test_case["spending_score"]
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Predicted Segment: {result['cluster_name']}")
            print(f"   Description: {result['description'][:60]}...")
            
            if result['cluster_name'] != test_case['expected']:
                print(f"   Expected: {test_case['expected']}")
        else:
            print(f"   Error: {response.status_code}")
            print(f"   {response.text}")
            all_passed = False
    
    return all_passed


def test_cluster_stats():
    """Test cluster statistics endpoint"""
    print("\n" + "="*60)
    print("Testing Cluster Statistics Endpoint...")
    print("="*60)
    
    response = requests.get(f"{API_URL}/clusters")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        stats = response.json()
        print(f"Number of Clusters: {len(stats)}")
        for stat in stats:
            print(f"  - {stat['cluster_name']}: {stat['count']} customers")
    else:
        print(f"Response: {response.text}")
    
    return response.status_code == 200


def test_cluster_info():
    """Test cluster info endpoint"""
    print("\n" + "="*60)
    print("Testing Cluster Info Endpoint...")
    print("="*60)
    
    response = requests.get(f"{API_URL}/clusters/info")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        info = response.json()
        print(f"Number of Clusters: {len(info)}")
        for cluster_id, details in info.items():
            print(f"  Cluster {cluster_id}: {details['name']}")
    
    return response.status_code == 200


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("Customer Segmentation API - Test Suite")
    print("="*60)
    print(f"Testing API at: {API_URL}")
    
    results = {
        "Health Check": False,
        "Model Info": False,
        "Prediction": False,
        "Cluster Stats": False,
        "Cluster Info": False
    }
    
    try:
        results["Health Check"] = test_health()
        results["Model Info"] = test_model_info()
        results["Prediction"] = test_prediction()
        results["Cluster Stats"] = test_cluster_stats()
        results["Cluster Info"] = test_cluster_info()
        
    except requests.exceptions.ConnectionError:
        print("\n" + "="*60)
        print("ERROR: Cannot connect to API")
        print("="*60)
        print("Please make sure the FastAPI server is running:")
        print("  python main.py")
        return False
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("All tests passed!")
    else:
        print("Some tests failed. Please check the output above.")
    print("="*60)
    
    return all_passed


if __name__ == "__main__":
    run_all_tests()
