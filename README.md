# Chemical Equipment Parameter Visualizer

A hybrid application that works as both a Web App (React) and a Desktop App (PyQt5) using a common Django REST backend for data processing and visualization.

## Project Structure

```
Flowdesk/
├── backend/              # Django REST API
├── web-frontend/         # React web application
├── desktop-frontend/     # PyQt5 desktop application
└── README.md
```

## Features

- CSV file upload with validation
- Equipment data visualization with charts
- Summary statistics (count, averages, type distribution)
- History of last 5 uploaded datasets
- PDF report generation
- Basic authentication
- Cross-platform desktop application

## Backend Setup (Django)

### Windows

1. Navigate to backend directory:
```cmd
cd backend
```

2. Create and activate virtual environment:
```cmd
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```cmd
pip install -r requirements.txt
```

4. Run migrations:
```cmd
python manage.py migrate
```

5. Create superuser:
```cmd
python manage.py createsuperuser
```

6. Run development server:
```cmd
python manage.py runserver
```

Or use the batch script:
```cmd
start_dev.bat
```

**Note:** Gunicorn doesn't work on Windows. Use Django dev server (development) or Waitress (production-like testing). See [WINDOWS_VS_UNIX.md](WINDOWS_VS_UNIX.md) for details.

### Unix/Linux/Mac

1. Navigate to backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

### API Endpoints

- `POST /api/upload/` - Upload CSV file
- `GET /api/summary/` - Get latest summary
- `GET /api/history/` - Get upload history (last 5)
- `GET /api/report/pdf/` - Download PDF report

All endpoints require Basic Authentication.

## Web Frontend Setup (React)

1. Navigate to web-frontend directory:
```bash
cd web-frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file (optional, defaults to localhost):
```bash
VITE_API_URL=http://localhost:8000/api
```

4. Run development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Vercel Deployment

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel
```

3. Set environment variable in Vercel dashboard:
   - `VITE_API_URL` = Your backend API URL

The `vercel.json` file is already configured for API proxying.

## Desktop Frontend Setup (PyQt5)

1. Navigate to desktop-frontend directory:
```bash
cd desktop-frontend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
# or
source venv/bin/activate      # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

## CSV File Format

The CSV file must contain the following columns:
- Equipment Name
- Type
- Flowrate
- Pressure
- Temperature

Example:
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-001,Pump,100.5,50.2,25.0
Valve-001,Valve,75.3,30.1,20.5
```

## Usage

1. Start the Django backend server
2. Start either the web frontend or desktop application
3. Login with your Django superuser credentials
4. Upload a CSV file with equipment data
5. View summary statistics, charts, and equipment table
6. Access history of previous uploads
7. Download PDF reports

## Technologies Used

- **Backend**: Django, Django REST Framework, pandas, ReportLab
- **Web Frontend**: React, Chart.js, Axios, Vite
- **Desktop Frontend**: PyQt5, Matplotlib, requests

## Deployment

### Production Deployment

For detailed deployment instructions, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

#### Quick Deploy Checklist

**Backend (Railway/Render):**
1. Set environment variables:
   - `SECRET_KEY` - Generate new secure key
   - `DEBUG=False`
   - `ALLOWED_HOSTS` - Your backend domain
   - `FRONTEND_URL` - Your frontend URL(s)
2. Run migrations after deploy
3. Create superuser

**Frontend (Vercel):**
1. Set environment variable:
   - `VITE_API_URL` - Your backend API URL
2. Deploy from GitHub

**Important:** After deploying, update backend's `FRONTEND_URL` with your deployed frontend URL to fix CORS issues.

### Troubleshooting Deployment

If registration works locally but not in production:
1. Check that `FRONTEND_URL` environment variable is set on backend
2. Verify CORS settings allow your frontend domain
3. Check browser console for CORS errors
4. Review [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed fixes

Run deployment checker:
```bash
cd backend
python check_deployment.py
```

## Documentation

- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Complete deployment instructions
- [REGISTRATION_DEBUG.md](REGISTRATION_DEBUG.md) - Registration troubleshooting
- [REGISTRATION_TEST_RESULTS.md](REGISTRATION_TEST_RESULTS.md) - Test verification

## License

This project is for educational purposes.
