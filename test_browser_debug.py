#!/usr/bin/env python3
"""
Test script to debug browser-specific issues using the debug endpoint.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_debug_endpoint():
    """Test the debug endpoint to see exactly what data is being received"""
    print("🔍 Testing debug endpoint...")

    # Test with various data formats that might cause issues
    test_cases = [
        {
            "name": "Normal data",
            "data": {
                "name": "Debug Test Product",
                "description": "A test product",
                "price": 29.99,
                "category": "Electronics",
                "stock_quantity": 10
            }
        },
        {
            "name": "Empty strings",
            "data": {
                "name": "",
                "description": "",
                "price": 0,
                "category": "",
                "stock_quantity": -1
            }
        },
        {
            "name": "Invalid types",
            "data": {
                "name": None,
                "description": None,
                "price": "invalid",
                "category": None,
                "stock_quantity": "invalid"
            }
        }
    ]

    for test_case in test_cases:
        print(f"\n📝 Testing: {test_case['name']}")
        print(f"   Data: {json.dumps(test_case['data'], indent=2)}")

        try:
            response = requests.post(f"{BASE_URL}/debug/products", json=test_case["data"])
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success! Product ID: {data['product']['id']}")
            elif response.status_code == 422:
                data = response.json()
                print(f"   ❌ Validation error: {data.get('detail', 'Unknown error')}")
            else:
                print(f"   ❌ Unexpected response: {response.text}")

        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_original_endpoint_with_problematic_data():
    """Test the original endpoint with data that might cause 422 errors"""
    print("\n🧪 Testing original endpoint with problematic data...")

    problematic_cases = [
        {
            "name": "All empty values",
            "data": {
                "name": "",
                "description": "",
                "price": 0,
                "category": "",
                "stock_quantity": -1
            }
        },
        {
            "name": "Missing required fields",
            "data": {
                "description": "Only description"
            }
        },
        {
            "name": "Invalid price types",
            "data": {
                "name": "Test",
                "description": "Test",
                "price": "not a number",
                "category": "Electronics",
                "stock_quantity": 10
            }
        }
    ]

    for test_case in problematic_cases:
        print(f"\n📝 Testing: {test_case['name']}")
        try:
            response = requests.post(f"{BASE_URL}/products", json=test_case["data"])
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                print(f"   ✅ Unexpected success!")
            elif response.status_code == 422:
                data = response.json()
                print(f"   ✅ Correctly rejected with validation errors:")
                for error in data.get('detail', []):
                    print(f"      - {error['loc']}: {error['msg']}")
            else:
                print(f"   ❌ Unexpected response: {response.text}")

        except Exception as e:
            print(f"   ❌ Error: {e}")

def main():
    """Run browser debug tests"""
    print("🔍 Browser Debug Test Suite")
    print("=" * 50)

    test_debug_endpoint()
    test_original_endpoint_with_problematic_data()

    print("\n🎉 Browser debug tests completed!")

if __name__ == "__main__":
    main()
