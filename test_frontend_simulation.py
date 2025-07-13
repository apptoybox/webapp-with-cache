#!/usr/bin/env python3
"""
Test script to simulate frontend form submission and identify 422 errors.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def simulate_frontend_submission():
    """Simulate what the frontend might be sending"""
    print("🖥️  Simulating frontend form submission...")

    # Test cases that might cause issues
    test_cases = [
        {
            "name": "Normal submission",
            "data": {
                "name": "Test Product",
                "description": "A test product",
                "price": 29.99,
                "category": "Electronics",
                "stock_quantity": 10
            }
        },
        {
            "name": "Empty description",
            "data": {
                "name": "Test Product",
                "description": "",
                "price": 29.99,
                "category": "Electronics",
                "stock_quantity": 10
            }
        },
        {
            "name": "Null description",
            "data": {
                "name": "Test Product",
                "description": None,
                "price": 29.99,
                "category": "Electronics",
                "stock_quantity": 10
            }
        },
        {
            "name": "Missing description",
            "data": {
                "name": "Test Product",
                "price": 29.99,
                "category": "Electronics",
                "stock_quantity": 10
            }
        },
        {
            "name": "String numbers",
            "data": {
                "name": "Test Product",
                "description": "A test product",
                "price": "29.99",
                "category": "Electronics",
                "stock_quantity": "10"
            }
        },
        {
            "name": "Whitespace values",
            "data": {
                "name": "   Test Product   ",
                "description": "   A test product   ",
                "price": 29.99,
                "category": "Electronics",
                "stock_quantity": 10
            }
        }
    ]

    for test_case in test_cases:
        print(f"\n📝 Testing: {test_case['name']}")
        print(f"   Data: {json.dumps(test_case['data'], indent=2)}")

        try:
            response = requests.post(f"{BASE_URL}/products", json=test_case["data"])
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success! Product ID: {data['product']['id']}")
            elif response.status_code == 422:
                data = response.json()
                print(f"   ❌ Validation error:")
                for error in data.get('detail', []):
                    print(f"      - {error['loc']}: {error['msg']}")
            else:
                print(f"   ❌ Unexpected response: {response.text}")

        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_browser_specific_issues():
    """Test issues that might occur in browser environments"""
    print("\n🌐 Testing browser-specific issues...")

    # Test with different content types
    headers_variations = [
        {"Content-Type": "application/json"},
        {"Content-Type": "application/json; charset=utf-8"},
        {"Content-Type": "application/json", "Accept": "application/json"},
        {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    ]

    test_data = {
        "name": "Browser Test Product",
        "description": "A test product",
        "price": 29.99,
        "category": "Electronics",
        "stock_quantity": 10
    }

    for i, headers in enumerate(headers_variations):
        print(f"\n   Testing headers variation {i+1}: {headers}")
        try:
            response = requests.post(f"{BASE_URL}/products", json=test_data, headers=headers)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print(f"   ✅ Success!")
            else:
                print(f"   ❌ Failed: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def main():
    """Run frontend simulation tests"""
    print("🖥️  Frontend Simulation Test Suite")
    print("=" * 50)

    simulate_frontend_submission()
    test_browser_specific_issues()

    print("\n🎉 Frontend simulation tests completed!")

if __name__ == "__main__":
    main()
