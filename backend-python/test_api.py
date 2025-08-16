"""
Test script for FastAPI AI Service
"""
import asyncio
import httpx
import json
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "dev-secret-key-123"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# Sample FAQ data for testing
sample_faqs = [
    {
        "question": "Siparişimi nasıl iptal edebilirim?",
        "answer": "Siparişinizi iptal etmek için hesabınıza giriş yapın ve 'Siparişlerim' bölümünden iptal butonuna tıklayın."
    },
    {
        "question": "Kargo ücreti ne kadar?",
        "answer": "150 TL üzeri siparişlerde kargo ücretsizdir. Altında ise 15 TL kargo ücreti alınır."
    },
    {
        "question": "İade koşulları nelerdir?",
        "answer": "Ürünleri teslim aldığınız tarihten itibaren 14 gün içinde iade edebilirsiniz."
    }
]

async def test_health_endpoint():
    """Test health check endpoint"""
    print("🏥 Testing health endpoint...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/health")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.status_code == 200
        except Exception as e:
            print(f"Error: {e}")
            return False

async def test_root_endpoint():
    """Test root endpoint"""
    print("🏠 Testing root endpoint...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.status_code == 200
        except Exception as e:
            print(f"Error: {e}")
            return False

async def test_ingest_endpoint():
    """Test FAQ ingestion endpoint"""
    print("📥 Testing ingest endpoint...")
    
    payload = {
        "user_id": "test-user-123",
        "faqs": sample_faqs
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{BASE_URL}/v1/ingest",
                headers=headers,
                json=payload
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.status_code == 200
        except Exception as e:
            print(f"Error: {e}")
            return False

async def test_query_endpoint():
    """Test query endpoint"""
    print("❓ Testing query endpoint...")
    
    # Test different languages
    test_queries = [
        {"message": "Siparişimi nasıl iptal ederim?", "language": "Turkish"},
        {"message": "How can I cancel my order?", "language": "English"},
        {"message": "Cuánto cuesta el envío?", "language": "Spanish"}
    ]
    
    results = []
    
    for query_data in test_queries:
        payload = {
            "user_id": "test-user-123",
            "message": query_data["message"]
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{BASE_URL}/v1/query",
                    headers=headers,
                    json=payload
                )
                print(f"\n🌍 {query_data['language']} Query:")
                print(f"Question: {query_data['message']}")
                print(f"Status: {response.status_code}")
                if response.status_code == 200:
                    result = response.json()
                    print(f"Answer: {result.get('answer', 'No answer')}")
                    results.append(True)
                else:
                    print(f"Error Response: {response.text}")
                    results.append(False)
            except Exception as e:
                print(f"Error: {e}")
                results.append(False)
    
    return all(results)

async def test_auth_endpoint():
    """Test API key authentication"""
    print("🔐 Testing authentication...")
    
    # Test without API key
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}/v1/query",
                json={"user_id": "test", "message": "test"}
            )
            print(f"Without API key - Status: {response.status_code}")
            no_auth_failed = response.status_code == 422  # Should fail
        except Exception as e:
            print(f"Error: {e}")
            no_auth_failed = True
    
    # Test with wrong API key
    wrong_headers = {"X-API-Key": "wrong-key", "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}/v1/query",
                headers=wrong_headers,
                json={"user_id": "test", "message": "test"}
            )
            print(f"Wrong API key - Status: {response.status_code}")
            wrong_auth_failed = response.status_code == 401  # Should fail
        except Exception as e:
            print(f"Error: {e}")
            wrong_auth_failed = True
    
    return no_auth_failed and wrong_auth_failed

async def run_all_tests():
    """Run all tests"""
    print("🚀 Starting FastAPI AI Service Tests\n")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_endpoint),
        ("Root Endpoint", test_root_endpoint),
        ("Authentication", test_auth_endpoint),
        ("FAQ Ingestion", test_ingest_endpoint),
        ("Query Processing", test_query_endpoint)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'=' * 20} {test_name} {'=' * 20}")
        try:
            result = await test_func()
            results.append((test_name, result))
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{status}")
        except Exception as e:
            print(f"❌ FAILED: {e}")
            results.append((test_name, False))
    
    print(f"\n{'=' * 50}")
    print("📊 TEST RESULTS")
    print(f"{'=' * 50}")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Total: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! The AI service is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the logs above for details.")

if __name__ == "__main__":
    print("Starting tests in 5 seconds... Make sure the FastAPI server is running!")
    print("Run: uvicorn main:app --reload")
    import time
    time.sleep(5)
    asyncio.run(run_all_tests())
