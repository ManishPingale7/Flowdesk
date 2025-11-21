"""
Test the registration API endpoint via HTTP
This script tests the actual REST API endpoint
"""
import requests
import json

API_BASE_URL = 'http://localhost:8000/api'

def test_registration():
    print("=" * 60)
    print("Testing Registration API Endpoint")
    print("=" * 60)
    
    # Test 1: Valid registration
    print("\n1. Testing valid registration...")
    test_data = {
        'username': 'testuser_api',
        'email': 'testapi@example.com',
        'password': 'testpass123',
        'password_confirm': 'testpass123'
    }
    
    try:
        response = requests.post(
            f'{API_BASE_URL}/register/',
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 201:
            print("   ✓ Registration successful!")
        else:
            print("   ✗ Registration failed")
            
    except requests.exceptions.ConnectionError:
        print("   ✗ Could not connect to backend. Make sure Django is running:")
        print("      cd backend && python manage.py runserver")
        return
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return
    
    # Test 2: Duplicate username
    print("\n2. Testing duplicate username...")
    try:
        response = requests.post(
            f'{API_BASE_URL}/register/',
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 400:
            print("   ✓ Correctly rejected duplicate username")
        else:
            print("   ✗ Should have rejected duplicate")
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 3: Password mismatch
    print("\n3. Testing password mismatch...")
    mismatch_data = {
        'username': 'testuser_api2',
        'email': 'testapi2@example.com',
        'password': 'testpass123',
        'password_confirm': 'differentpass'
    }
    
    try:
        response = requests.post(
            f'{API_BASE_URL}/register/',
            json=mismatch_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 400:
            print("   ✓ Correctly rejected mismatched passwords")
        else:
            print("   ✗ Should have rejected mismatch")
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 4: Login with registered user
    print("\n4. Testing login with registered user...")
    try:
        import base64
        credentials = f"{test_data['username']}:{test_data['password']}"
        auth_header = 'Basic ' + base64.b64encode(credentials.encode()).decode()
        
        response = requests.get(
            f'{API_BASE_URL}/history/',
            headers={'Authorization': auth_header}
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✓ Successfully authenticated with new user!")
        else:
            print(f"   ✗ Authentication failed: {response.text}")
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("Test complete!")
    print("=" * 60)

if __name__ == '__main__':
    test_registration()
