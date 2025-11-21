import pandas as pd
from django.core.exceptions import ValidationError


REQUIRED_COLUMNS = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']


def validate_csv_columns(df):
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValidationError(f"Missing required columns: {', '.join(missing_columns)}")


def parse_csv(file):
    try:
        df = pd.read_csv(file)
        validate_csv_columns(df)
        return df
    except Exception as e:
        raise ValidationError(f"Error parsing CSV: {str(e)}")


def compute_summary(df):
    numeric_cols = ['Flowrate', 'Pressure', 'Temperature']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    summary = {
        'total_count': len(df),
        'avg_flowrate': float(df['Flowrate'].mean()) if not df['Flowrate'].isna().all() else 0.0,
        'avg_pressure': float(df['Pressure'].mean()) if not df['Pressure'].isna().all() else 0.0,
        'avg_temperature': float(df['Temperature'].mean()) if not df['Temperature'].isna().all() else 0.0,
        'type_distribution': df['Type'].value_counts().to_dict(),
        'equipment_data': df.to_dict('records')
    }
    
    return summary

