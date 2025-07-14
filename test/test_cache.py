#!/usr/bin/env python3
"""
Test script to verify caching functionality and demonstrate performance improvements.
"""

import requests
import time
import json

BASE_URL = "http://localhost:8000"

def test_cache_functionality():
    """Test basic caching functionality"""
    print("🧪 Testing Cache Functionality")
    print("=" * 50)

    # Test 1: First request (should hit database)
    print("\n1. First request (should hit database):")
    start_time = time.time()
    response1 = requests.get(f"{BASE_URL}/products")
    time1 = time.time() - start_time

    if response1.status_code == 200:
        data1 = response1.json()
        print(f"   ✅ Response time: {time1:.3f}s")
        print(f"   📊 Source: {data1.get('source', 'unknown')}")
        print(f"   📦 Products returned: {len(data1.get('products', []))}")
    else:
        print(f"   ❌ Error: {response1.status_code}")
        return

    # Test 2: Second request (should hit cache)
    print("\n2. Second request (should hit cache):")
    start_time = time.time()
    response2 = requests.get(f"{BASE_URL}/products")
    time2 = time.time() - start_time

    if response2.status_code == 200:
        data2 = response2.json()
        print(f"   ✅ Response time: {time2:.3f}s")
        print(f"   📊 Source: {data2.get('source', 'unknown')}")
        print(f"   📦 Products returned: {len(data2.get('products', []))}")
    else:
        print(f"   ❌ Error: {response2.status_code}")
        return

    # Calculate improvement
    if time1 > 0:
        improvement = ((time1 - time2) / time1) * 100
        print(f"\n🚀 Performance improvement: {improvement:.1f}%")

    # Test 3: Cache statistics
    print("\n3. Cache statistics:")
    stats_response = requests.get(f"{BASE_URL}/cache/stats")
    if stats_response.status_code == 200:
        stats = stats_response.json()
        print(f"   📈 Hits: {stats.get('hits', 0)}")
        print(f"   📉 Misses: {stats.get('misses', 0)}")
        print(f"   🎯 Hit rate: {stats.get('hit_rate', 0)}%")
    else:
        print(f"   ❌ Error getting stats: {stats_response.status_code}")

def test_cache_invalidation():
    """Test cache invalidation when adding new products"""
    print("\n\n🔄 Testing Cache Invalidation")
    print("=" * 50)

    # Add a new product
    new_product = {
        "name": "Test Product",
        "description": "A test product for cache invalidation",
        "price": 99.99,
        "category": "Electronics",
        "stock_quantity": 10
    }

    print("\n1. Adding new product:")
    response = requests.post(f"{BASE_URL}/products", json=new_product)
    if response.status_code == 200:
        print("   ✅ Product added successfully")
    else:
        print(f"   ❌ Error adding product: {response.status_code}")
        return

    # Test that cache was invalidated
    print("\n2. Testing cache invalidation:")
    response = requests.get(f"{BASE_URL}/products")
    if response.status_code == 200:
        data = response.json()
        print(f"   📊 Source: {data.get('source', 'unknown')}")
        if data.get('source') == 'database':
            print("   ✅ Cache was properly invalidated")
        else:
            print("   ⚠️  Cache may not have been invalidated")
    else:
        print(f"   ❌ Error: {response.status_code}")

def test_individual_product_caching():
    """Test caching for individual products"""
    print("\n\n🎯 Testing Individual Product Caching")
    print("=" * 50)

    # Get first product ID
    response = requests.get(f"{BASE_URL}/products")
    if response.status_code != 200:
        print("   ❌ Error getting products")
        return

    products = response.json().get('products', [])
    if not products:
        print("   ❌ No products found")
        return

    product_id = products[0]['id']

    # Test individual product caching
    print(f"\n1. First request for product {product_id}:")
    start_time = time.time()
    response1 = requests.get(f"{BASE_URL}/products/{product_id}")
    time1 = time.time() - start_time

    if response1.status_code == 200:
        data1 = response1.json()
        print(f"   ✅ Response time: {time1:.3f}s")
        print(f"   📊 Source: {data1.get('source', 'unknown')}")
    else:
        print(f"   ❌ Error: {response1.status_code}")
        return

    # Second request
    print(f"\n2. Second request for product {product_id}:")
    start_time = time.time()
    response2 = requests.get(f"{BASE_URL}/products/{product_id}")
    time2 = time.time() - start_time

    if response2.status_code == 200:
        data2 = response2.json()
        print(f"   ✅ Response time: {time2:.3f}s")
        print(f"   📊 Source: {data2.get('source', 'unknown')}")

        if time1 > 0:
            improvement = ((time1 - time2) / time1) * 100
            print(f"   🚀 Performance improvement: {improvement:.1f}%")
    else:
        print(f"   ❌ Error: {response2.status_code}")

def test_performance_comparison():
    """Test the performance comparison endpoint"""
    print("\n\n⚡ Testing Performance Comparison")
    print("=" * 50)

    response = requests.get(f"{BASE_URL}/cache/performance")
    if response.status_code == 200:
        data = response.json()
        print(f"   📊 Cached response time: {data.get('cached_response_time', 0):.3f}s")
        print(f"   📊 Database response time: {data.get('database_response_time', 0):.3f}s")
        print(f"   🚀 Performance improvement: {data.get('performance_improvement', '0%')}")
    else:
        print(f"   ❌ Error: {response.status_code}")

def main():
    """Run all tests"""
    print("🚀 Cache Example Application - Test Suite")
    print("=" * 60)

    try:
        # Test if application is running
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print("❌ Application is not running. Please start the application first.")
            print("   Run: docker-compose up --build")
            return

        print("✅ Application is running")

        # Run tests
        test_cache_functionality()
        test_cache_invalidation()
        test_individual_product_caching()
        test_performance_comparison()

        print("\n\n🎉 All tests completed!")
        print("\n💡 Tips:")
        print("   - Open http://localhost:8000 in your browser to see the web interface")
        print("   - Try the 'Performance Test' button on the web interface")
        print("   - Monitor cache statistics in real-time")

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to application. Please ensure it's running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    main()
