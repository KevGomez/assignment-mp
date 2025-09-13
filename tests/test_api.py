#!/usr/bin/env python3
"""
Test script to demonstrate JWT-secured Product API usage
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_api():
    print("=== Product Management API Test ===\n")
    
    # Step 1: Register a user (or use existing admin)
    print("1. Using admin credentials...")
    username = "admin"
    password = "admin123"
    
    # Step 2: Get JWT token
    print("2. Getting JWT token...")
    token_data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/token", data=token_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print(f"✓ Token obtained: {token[:20]}...")
        else:
            print(f"✗ Failed to get token: {response.text}")
            return
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
        return
    
    # Headers for authenticated requests
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Step 3: Test getting all products
    print("\n3. Getting all products...")
    try:
        response = requests.get(f"{BASE_URL}/products/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Found {data['total']} products")
            if data['products']:
                print(f"   First product: {data['products'][0]['name']}")
        else:
            print(f"✗ Failed: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    
    # Step 4: Test creating a new product
    print("\n4. Creating a new product...")
    new_product = {
        "brand": "Test Brand",
        "slug": "test-product-jwt",
        "name": "JWT Test Product",
        "stock": 50
    }
    
    try:
        response = requests.post(f"{BASE_URL}/products/", 
                               headers=headers, 
                               json=new_product)
        if response.status_code == 201:
            created_product = response.json()["product"]
            print(f"✓ Created product with ID: {created_product['id']}")
            product_id = created_product['id']
        else:
            print(f"✗ Failed: {response.text}")
            return
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
        return
    
    # Step 5: Test getting product by ID
    print(f"\n5. Getting product by ID {product_id}...")
    try:
        response = requests.get(f"{BASE_URL}/products/{product_id}", headers=headers)
        if response.status_code == 200:
            product = response.json()["product"]
            print(f"✓ Retrieved: {product['name']}")
        else:
            print(f"✗ Failed: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    
    # Step 6: Test search functionality
    print("\n6. Searching for 'shirt' products...")
    try:
        response = requests.get(f"{BASE_URL}/products/?search=shirt", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Found {len(data['products'])} products matching 'shirt'")
        else:
            print(f"✗ Failed: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    
    # Step 7: Test without authentication (should fail)
    print("\n7. Testing without authentication (should fail)...")
    try:
        response = requests.get(f"{BASE_URL}/products/")
        if response.status_code == 401:
            print("✓ Correctly rejected unauthenticated request")
        else:
            print(f"✗ Unexpected response: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_api()
