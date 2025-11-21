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

1. Navigate to backend directory:
```bash
cd backend
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

## License

This project is for educational purposes.
