# Registration Issue - Debugging Guide

## Changes Made to Fix Registration

### 1. Updated CORS Settings (backend/chemviz/settings.py)
Added additional allowed origins and headers for better CORS support:
- Added Vite dev server ports (5173) to CORS_ALLOWED_ORIGINS
- Added explicit CORS_ALLOW_HEADERS to include all necessary headers for API requests

### 2. Verified Registration Endpoint
The registration endpoint is correctly configured:
- URL: POST /api/register/
- Permission: AllowAny (no authentication required)
- Accepts JSON with: username, email, password, password_confirm

## Common Issues and Solutions

### Issue 1: CORS Errors
**Symptom:** Browser console shows CORS policy errors
**Solution:** 
- Backend CORS settings have been updated
- Ensure frontend is running on localhost:3000 or localhost:5173
- Check browser console for specific CORS error messages

### Issue 2: CSRF Token Errors
**Symptom:** 403 Forbidden or CSRF verification failed
**Solution:**
- DRF's @api_view decorator handles CSRF automatically
- For API-only endpoints with @permission_classes([AllowAny]), CSRF is not required
- SessionAuthentication requires CSRF, but BasicAuthentication does not

### Issue 3: Password Validation Errors
**Symptom:** Registration returns 400 with password errors
**Solution:**
- Password must be at least 8 characters
- password and password_confirm must match
- Check serializer validation in backend/analytics/serializers.py

### Issue 4: Duplicate Username
**Symptom:** Registration returns 400 with username errors
**Solution:**
- Username must be unique
- Django automatically validates this in User model
- Clear the database or use a different username

## Testing the Registration

### Option 1: Using the Test Script
```cmd
cd g:\Flowdesk\backend
python test_api_registration.py
```

This will test:
1. Valid registration
2. Duplicate username handling
3. Password mismatch handling
4. Login with registered credentials

### Option 2: Using curl (Windows cmd)
```cmd
curl -X POST http://localhost:8000/api/register/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"testuser\",\"email\":\"test@example.com\",\"password\":\"testpass123\",\"password_confirm\":\"testpass123\"}"
```

### Option 3: Using the Web Frontend
1. Start backend: `cd backend && python manage.py runserver`
2. Start frontend: `cd web-frontend && npm run dev`
3. Navigate to http://localhost:5173
4. Click "Sign Up" and fill in the form

### Option 4: Using the Desktop Frontend
1. Start backend: `cd backend && python manage.py runserver`
2. Run desktop app: `cd desktop-frontend && python main.py`
3. Click "Register" and fill in the form

## Verification Steps

### 1. Check if Backend is Running
```cmd
curl http://localhost:8000/api/register/
```
Should return: `{"detail":"Method \"GET\" not allowed."}`
This confirms the endpoint exists and is accessible.

### 2. Check Database for User
```cmd
cd backend
python manage.py shell
```
```python
from django.contrib.auth.models import User
User.objects.filter(username='testuser').exists()
User.objects.get(username='testuser')
```

### 3. Test Authentication
```cmd
curl -X GET http://localhost:8000/api/history/ ^
  -H "Authorization: Basic dGVzdHVzZXI6dGVzdHBhc3MxMjM="
```
(The Base64 string is username:password encoded)

## API Endpoint Details

### POST /api/register/
**Request:**
```json
{
  "username": "string (required)",
  "email": "string (required, valid email)",
  "password": "string (required, min 8 chars)",
  "password_confirm": "string (required, must match password)"
}
```

**Success Response (201):**
```json
{
  "message": "User registered successfully",
  "username": "testuser"
}
```

**Error Response (400):**
```json
{
  "username": ["A user with that username already exists."],
  "password": ["This password is too short. It must contain at least 8 characters."],
  "non_field_errors": ["Passwords don't match"]
}
```

## Files Modified

1. **backend/chemviz/settings.py**
   - Added localhost:5173 to CORS_ALLOWED_ORIGINS (Vite dev server)
   - Added explicit CORS_ALLOW_HEADERS

2. **backend/analytics/views.py**
   - No changes needed (already correct)

3. **backend/analytics/serializers.py**
   - No changes needed (already correct)

## Next Steps if Still Not Working

1. **Check Django logs:**
   - Look for errors in the terminal where `python manage.py runserver` is running
   - Check for validation errors or exceptions

2. **Check browser console:**
   - Open browser DevTools (F12)
   - Look in Console and Network tabs
   - Check request/response details

3. **Verify request format:**
   - Ensure Content-Type header is 'application/json'
   - Ensure JSON is properly formatted
   - Check field names match exactly (password_confirm not passwordConfirm)

4. **Database issues:**
   - Run migrations: `python manage.py migrate`
   - Check if database is writable
   - Try creating user via Django admin to verify DB works

5. **Test with minimal request:**
   ```python
   import requests
   resp = requests.post('http://localhost:8000/api/register/', 
                       json={'username': 'test', 'email': 'a@b.com', 
                             'password': '12345678', 'password_confirm': '12345678'})
   print(resp.status_code, resp.text)
   ```
