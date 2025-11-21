"""
Test script to debug registration endpoint
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chemviz.settings')
django.setup()

from analytics.serializers import RegisterSerializer
from django.contrib.auth.models import User

# Test 1: Check if serializer validates correctly
print("=" * 60)
print("Test 1: Testing RegisterSerializer validation")
print("=" * 60)

test_data = {
    'username': 'testuser',
    'email': 'test@example.com',
    'password': 'testpass123',
    'password_confirm': 'testpass123'
}

serializer = RegisterSerializer(data=test_data)
if serializer.is_valid():
    print("✓ Serializer validation passed")
    print(f"  Validated data: {serializer.validated_data}")
else:
    print("✗ Serializer validation failed")
    print(f"  Errors: {serializer.errors}")

# Test 2: Try to create a user
print("\n" + "=" * 60)
print("Test 2: Testing user creation")
print("=" * 60)

# Clean up if user exists
if User.objects.filter(username='testuser').exists():
    User.objects.filter(username='testuser').delete()
    print("  Cleaned up existing test user")

serializer = RegisterSerializer(data=test_data)
if serializer.is_valid():
    try:
        user = serializer.save()
        print("✓ User created successfully")
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  ID: {user.id}")
        
        # Verify password was set
        if user.check_password('testpass123'):
            print("✓ Password was set correctly")
        else:
            print("✗ Password was NOT set correctly")
            
    except Exception as e:
        print(f"✗ Error creating user: {e}")
else:
    print("✗ Validation failed")
    print(f"  Errors: {serializer.errors}")

# Test 3: Check for duplicate username
print("\n" + "=" * 60)
print("Test 3: Testing duplicate username handling")
print("=" * 60)

serializer = RegisterSerializer(data=test_data)
if serializer.is_valid():
    try:
        user = serializer.save()
        print("✗ Should have failed with duplicate username")
    except Exception as e:
        print(f"✓ Correctly caught duplicate: {e}")
else:
    print("✓ Validation correctly failed for duplicate")
    print(f"  Errors: {serializer.errors}")

# Test 4: Test password mismatch
print("\n" + "=" * 60)
print("Test 4: Testing password mismatch")
print("=" * 60)

mismatch_data = {
    'username': 'testuser2',
    'email': 'test2@example.com',
    'password': 'testpass123',
    'password_confirm': 'differentpass'
}

serializer = RegisterSerializer(data=mismatch_data)
if serializer.is_valid():
    print("✗ Should have failed with password mismatch")
else:
    print("✓ Correctly rejected mismatched passwords")
    print(f"  Errors: {serializer.errors}")

# Clean up
print("\n" + "=" * 60)
print("Cleaning up test users...")
print("=" * 60)
User.objects.filter(username__in=['testuser', 'testuser2']).delete()
print("✓ Cleanup complete")
