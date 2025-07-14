#!/usr/bin/env python3
"""
Test script to verify that the 500 error has been resolved.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test the health endpoint"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health endpoint working: {data}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")

def test_create_product():
    """Test creating a product (the endpoint that was failing)"""
    print("\n🧪 Testing product creation...")

    test_product = {
        "name": "Test Product",
        "description": "A test product to verify the fix",
        "price": 29.99,
        "category": "Electronics",
        "stock_quantity": 10
    }

    try:
        response = requests.post(f"{BASE_URL}/products", json=test_product)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Product creation successful!")
            print(f"   Product ID: {data['product']['id']}")
            print(f"   Source: {data['source']}")
            print(f"   Response Time: {data['response_time']:.3f}s")
        else:
            print(f"❌ Product creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Product creation error: {e}")

def test_get_products():
    """Test getting products"""
    print("\n📦 Testing get products...")

    try:
        response = requests.get(f"{BASE_URL}/products")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Get products successful!")
            print(f"   Products count: {len(data['products'])}")
            print(f"   Source: {data['source']}")
            print(f"   Response Time: {data['response_time']:.3f}s")
        else:
            print(f"❌ Get products failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Get products error: {e}")

def test_cache_stats():
    """Test cache statistics"""
    print("\n📊 Testing cache statistics...")

    try:
        response = requests.get(f"{BASE_URL}/cache/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Cache stats successful!")
            print(f"   Hits: {data['hits']}")
            print(f"   Misses: {data['misses']}")
            print(f"   Hit Rate: {data['hit_rate']}%")
        else:
            print(f"❌ Cache stats failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Cache stats error: {e}")

def main():
    """Run all tests"""
    print("🔧 Testing Cache Example Application Fix")
    print("=" * 50)

    # Wait a moment for application to be ready
    print("⏳ Waiting for application to be ready...")
    time.sleep(3)

    test_health_endpoint()
    test_create_product()
    test_get_products()
    test_cache_stats()

    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    main()
