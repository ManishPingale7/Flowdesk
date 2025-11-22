@echo off
REM Simple development server for Windows
echo Starting Django Development Server...

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Start Django dev server
echo.
echo Backend API available at: http://127.0.0.1:8000/api/
echo Admin panel at: http://127.0.0.1:8000/admin/
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver 0.0.0.0:8000
