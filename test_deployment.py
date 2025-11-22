"""
Quick Deployment Diagnostics
Run this to test if your deployed backend is accessible
"""

import requests
import sys

# REPLACE THESE WITH YOUR ACTUAL DEPLOYED URLS
BACKEND_URL = "https://your-backend.railway.app"  # ← Change this!
FRONTEND_URL = "https://your-app.vercel.app"      # ← Change this!

print("=" * 60)
print("DEPLOYMENT DIAGNOSTICS")
print("=" * 60)
print(f"\nBackend URL: {BACKEND_URL}")
print(f"Frontend URL: {FRONTEND_URL}")
print()

# Test 1: Check if backend is reachable
print("1. Testing backend connectivity...")
try:
    response = requests.get(f"{BACKEND_URL}/api/register/", timeout=10)
    if response.status_code == 405:
        print("   ✓ Backend is UP and reachable")
    else:
        print(f"   ⚠️  Backend responded with unexpected status: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("   ✗ Backend is DOWN or URL is wrong")
    print("   Check: Is your backend deployed? Is the URL correct?")
    sys.exit(1)
except Exception as e:
    print(f"   ✗ Error connecting to backend: {e}")
    sys.exit(1)

# Test 2: Check CORS
print("\n2. Testing CORS configuration...")
try:
    response = requests.options(
        f"{BACKEND_URL}/api/register/",
        headers={
            'Origin': FRONTEND_URL,
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'content-type'
        },
        timeout=10
    )
    
    if 'Access-Control-Allow-Origin' in response.headers:
        allowed_origin = response.headers.get('Access-Control-Allow-Origin')
        if allowed_origin == FRONTEND_URL or allowed_origin == '*':
            print(f"   ✓ CORS is configured correctly")
            print(f"     Allowed Origin: {allowed_origin}")
        else:
            print(f"   ⚠️  CORS allows: {allowed_origin}")
            print(f"     But frontend is: {FRONTEND_URL}")
            print("   Fix: Set FRONTEND_URL environment variable on backend")
    else:
        print("   ✗ CORS headers not found")
        print("   Fix: Set FRONTEND_URL environment variable on backend")
except Exception as e:
    print(f"   ⚠️  Could not test CORS: {e}")

# Test 3: Try registration
print("\n3. Testing registration endpoint...")
test_user = {
    'username': f'testuser_{int(requests.utils.time.time())}',
    'email': 'test@example.com',
    'password': 'testpass123',
    'password_confirm': 'testpass123'
}

try:
    response = requests.post(
        f"{BACKEND_URL}/api/register/",
        json=test_user,
        headers={'Content-Type': 'application/json'},
        timeout=10
    )
    
    if response.status_code == 201:
        print("   ✓ Registration endpoint works!")
        print(f"     Response: {response.json()}")
    elif response.status_code == 400:
        print("   ⚠️  Registration endpoint works but validation failed")
        print(f"     Error: {response.json()}")
    elif response.status_code == 500:
        print("   ✗ Backend error (500)")
        print("   Fix: Check backend logs for Python errors")
        print("   Common causes:")
        print("     - Database migrations not run")
        print("     - Missing environment variables")
        print("     - Code errors")
    else:
        print(f"   ⚠️  Unexpected status: {response.status_code}")
        print(f"     Response: {response.text[:200]}")
        
except Exception as e:
    print(f"   ✗ Error testing registration: {e}")

# Test 4: Check if migrations were run
print("\n4. Testing if database is set up...")
try:
    response = requests.get(f"{BACKEND_URL}/api/history/", timeout=10)
    if response.status_code == 401:
        print("   ✓ Database appears to be working (auth required)")
    elif response.status_code == 404:
        print("   ✗ History endpoint not found")
    elif response.status_code == 500:
        print("   ✗ Database error - migrations might not be run")
        print("   Fix: Run 'python manage.py migrate' in backend console")
    else:
        print(f"   ⚠️  Unexpected response: {response.status_code}")
except Exception as e:
    print(f"   ⚠️  Could not test database: {e}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print("\nIf tests failed, check:")
print("1. Backend environment variables:")
print("   - FRONTEND_URL=https://your-app.vercel.app")
print("   - ALLOWED_HOSTS=your-backend.railway.app")
print("   - DEBUG=False")
print("   - SECRET_KEY=<secure-key>")
print()
print("2. Frontend environment variables:")
print("   - VITE_API_URL=https://your-backend.railway.app/api")
print()
print("3. Run migrations on backend:")
print("   python manage.py migrate")
print()
print("4. Check backend logs for errors")
print()
print("See DEPLOYMENT_GUIDE.md for detailed instructions")
print("=" * 60)
