@echo off
REM Windows start script - uses waitress instead of gunicorn
echo Starting Chemical Equipment Visualizer Backend (Windows)...

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Run migrations
echo Running migrations...
python manage.py migrate

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

REM Start server with waitress (Windows-compatible)
echo Starting server on port 8000...
echo.
echo Backend API available at: http://127.0.0.1:8000/api/
echo Admin panel at: http://127.0.0.1:8000/admin/
echo.
echo Press Ctrl+C to stop the server
echo.

python -m waitress --host=0.0.0.0 --port=8000 chemviz.wsgi:application
