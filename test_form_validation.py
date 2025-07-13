#!/usr/bin/env python3
"""
Test script to verify form validation and identify 422 errors.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_valid_product():
    """Test with valid product data"""
    print("✅ Testing valid product creation...")

    valid_product = {
        "name": "Valid Product",
        "description": "A valid product description",
        "price": 29.99,
        "category": "Electronics",
        "stock_quantity": 10
    }

    try:
        response = requests.post(f"{BASE_URL}/products", json=valid_product)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success! Product ID: {data['product']['id']}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_invalid_products():
    """Test various invalid product data scenarios"""
    print("\n❌ Testing invalid product scenarios...")

    test_cases = [
        {
            "name": "Empty name",
            "data": {"name": "", "description": "Test", "price": 10.0, "category": "Electronics", "stock_quantity": 5},
            "expected_error": "String should have at least 1 character"
        },
        {
            "name": "Zero price",
            "data": {"name": "Test Product", "description": "Test", "price": 0, "category": "Electronics", "stock_quantity": 5},
            "expected_error": "Input should be greater than 0"
        },
        {
            "name": "Negative price",
            "data": {"name": "Test Product", "description": "Test", "price": -10.0, "category": "Electronics", "stock_quantity": 5},
            "expected_error": "Input should be greater than 0"
        },
        {
            "name": "Empty category",
            "data": {"name": "Test Product", "description": "Test", "price": 10.0, "category": "", "stock_quantity": 5},
            "expected_error": "String should have at least 1 character"
        },
        {
            "name": "Negative stock",
            "data": {"name": "Test Product", "description": "Test", "price": 10.0, "category": "Electronics", "stock_quantity": -5},
            "expected_error": "Input should be greater than or equal to 0"
        },
        {
            "name": "Missing required fields",
            "data": {"description": "Test", "price": 10.0, "stock_quantity": 5},
            "expected_error": "Field required"
        }
    ]

    for test_case in test_cases:
        print(f"\n   Testing: {test_case['name']}")
        try:
            response = requests.post(f"{BASE_URL}/products", json=test_case["data"])
            if response.status_code == 422:
                data = response.json()
                print(f"   ✅ Correctly rejected with 422")
                if "detail" in data:
                    print(f"   Error details: {data['detail']}")
            else:
                print(f"   ❌ Unexpected response: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_edge_cases():
    """Test edge cases that might cause issues"""
    print("\n🔍 Testing edge cases...")

    edge_cases = [
        {
            "name": "Very long name",
            "data": {"name": "A" * 300, "description": "Test", "price": 10.0, "category": "Electronics", "stock_quantity": 5}
        },
        {
            "name": "Very long category",
            "data": {"name": "Test Product", "description": "Test", "price": 10.0, "category": "A" * 150, "stock_quantity": 5}
        },
        {
            "name": "Very high price",
            "data": {"name": "Test Product", "description": "Test", "price": 999999.99, "category": "Electronics", "stock_quantity": 5}
        },
        {
            "name": "Very high stock",
            "data": {"name": "Test Product", "description": "Test", "price": 10.0, "category": "Electronics", "stock_quantity": 999999}
        }
    ]

    for test_case in edge_cases:
        print(f"\n   Testing: {test_case['name']}")
        try:
            response = requests.post(f"{BASE_URL}/products", json=test_case["data"])
            if response.status_code == 200:
                print(f"   ✅ Accepted")
            elif response.status_code == 422:
                print(f"   ✅ Correctly rejected")
            else:
                print(f"   ❌ Unexpected response: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def main():
    """Run all validation tests"""
    print("🧪 Form Validation Test Suite")
    print("=" * 50)

    test_valid_product()
    test_invalid_products()
    test_edge_cases()

    print("\n🎉 Validation tests completed!")

if __name__ == "__main__":
    main()
