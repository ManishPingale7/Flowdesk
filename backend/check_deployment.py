"""
Production Deployment Checker
This script helps diagnose issues with production deployment
"""
import os
import sys

print("=" * 60)
print("DEPLOYMENT CONFIGURATION CHECK")
print("=" * 60)

# Check Django settings
print("\n1. Checking Django Settings...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chemviz.settings')

try:
    import django
    django.setup()
    from django.conf import settings
    
    print(f"   ✓ Django version: {django.get_version()}")
    print(f"   ✓ DEBUG mode: {settings.DEBUG}")
    print(f"   ✓ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    
    if settings.DEBUG:
        print("   ⚠️  WARNING: DEBUG is True - should be False in production!")
    
    if '*' in settings.ALLOWED_HOSTS and not settings.DEBUG:
        print("   ⚠️  WARNING: ALLOWED_HOSTS contains '*' - not recommended for production!")
        
except Exception as e:
    print(f"   ✗ Error loading Django: {e}")
    sys.exit(1)

# Check CORS settings
print("\n2. Checking CORS Settings...")
try:
    print(f"   ✓ CORS enabled: {'corsheaders' in settings.INSTALLED_APPS}")
    
    if hasattr(settings, 'CORS_ALLOWED_ORIGINS'):
        print(f"   ✓ CORS_ALLOWED_ORIGINS count: {len(settings.CORS_ALLOWED_ORIGINS)}")
        for origin in settings.CORS_ALLOWED_ORIGINS:
            print(f"     - {origin}")
    
    if hasattr(settings, 'CORS_ALLOW_ALL_ORIGINS') and settings.CORS_ALLOW_ALL_ORIGINS:
        print("   ⚠️  WARNING: CORS_ALLOW_ALL_ORIGINS is True - security risk!")
    
    print(f"   ✓ CORS_ALLOW_CREDENTIALS: {settings.CORS_ALLOW_CREDENTIALS}")
    
except Exception as e:
    print(f"   ✗ Error checking CORS: {e}")

# Check environment variables
print("\n3. Checking Environment Variables...")
env_vars = {
    'SECRET_KEY': '***' if os.environ.get('SECRET_KEY') else None,
    'DEBUG': os.environ.get('DEBUG'),
    'ALLOWED_HOSTS': os.environ.get('ALLOWED_HOSTS'),
    'FRONTEND_URL': os.environ.get('FRONTEND_URL'),
    'DATABASE_URL': '***' if os.environ.get('DATABASE_URL') else None,
    'CORS_ALLOW_ALL': os.environ.get('CORS_ALLOW_ALL'),
}

for key, value in env_vars.items():
    if value:
        print(f"   ✓ {key}: {value}")
    else:
        print(f"   ✗ {key}: Not set (using default)")

# Check database
print("\n4. Checking Database...")
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    print(f"   ✓ Database connection: OK")
    print(f"   ✓ Database engine: {settings.DATABASES['default']['ENGINE']}")
    
    if 'sqlite3' in settings.DATABASES['default']['ENGINE'] and not settings.DEBUG:
        print("   ⚠️  WARNING: Using SQLite in production - consider PostgreSQL")
        
except Exception as e:
    print(f"   ✗ Database connection failed: {e}")

# Check migrations
print("\n5. Checking Migrations...")
try:
    from django.db.migrations.executor import MigrationExecutor
    from django.db import connections
    
    executor = MigrationExecutor(connections['default'])
    plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
    
    if plan:
        print(f"   ⚠️  WARNING: {len(plan)} unapplied migrations found!")
        print("   Run: python manage.py migrate")
    else:
        print("   ✓ All migrations applied")
        
except Exception as e:
    print(f"   ✗ Error checking migrations: {e}")

# Check static files
print("\n6. Checking Static Files...")
try:
    static_root = settings.STATIC_ROOT
    if static_root and os.path.exists(static_root):
        print(f"   ✓ STATIC_ROOT exists: {static_root}")
        file_count = sum(len(files) for _, _, files in os.walk(static_root))
        print(f"   ✓ Static files count: {file_count}")
    else:
        print("   ⚠️  WARNING: STATIC_ROOT not found or doesn't exist")
        print("   Run: python manage.py collectstatic")
except Exception as e:
    print(f"   ✗ Error checking static files: {e}")

# Check installed packages
print("\n7. Checking Required Packages...")
required_packages = [
    'django',
    'djangorestframework',
    'django-cors-headers',
    'pandas',
    'reportlab',
    'matplotlib',
    'gunicorn',
    'whitenoise'
]

for package in required_packages:
    try:
        __import__(package.replace('-', '_'))
        print(f"   ✓ {package}")
    except ImportError:
        print(f"   ✗ {package} - NOT INSTALLED")

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

issues = []

if settings.DEBUG:
    issues.append("DEBUG mode is enabled")

if '*' in settings.ALLOWED_HOSTS and not settings.DEBUG:
    issues.append("ALLOWED_HOSTS contains wildcard")

if hasattr(settings, 'CORS_ALLOW_ALL_ORIGINS') and settings.CORS_ALLOW_ALL_ORIGINS:
    issues.append("CORS allows all origins")

if not os.environ.get('FRONTEND_URL'):
    issues.append("FRONTEND_URL environment variable not set")

if 'sqlite3' in settings.DATABASES['default']['ENGINE'] and not settings.DEBUG:
    issues.append("Using SQLite in production")

if issues:
    print(f"\n⚠️  Found {len(issues)} potential issue(s):")
    for i, issue in enumerate(issues, 1):
        print(f"   {i}. {issue}")
    print("\nReview DEPLOYMENT_GUIDE.md for fixes.")
else:
    print("\n✓ All checks passed! Configuration looks good.")

print("\n" + "=" * 60)
