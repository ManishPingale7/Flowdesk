from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse, FileResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import Dataset
from .serializers import DatasetSerializer, CSVUploadSerializer
from .utils import parse_csv, compute_summary
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import io
import json


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    serializer = CSVUploadSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    file = serializer.validated_data['file']
    
    try:
        df = parse_csv(file)
        summary = compute_summary(df)
        
        file.seek(0)
        file_name = default_storage.save(f'csv_files/{file.name}', ContentFile(file.read()))
        
        dataset = Dataset.objects.create(
            file_path=file_name,
            summary=summary
        )
        
        datasets = Dataset.objects.order_by('-uploaded_at')
        if datasets.count() > 5:
            for old_dataset in datasets[5:]:
                if old_dataset.file_path:
                    default_storage.delete(old_dataset.file_path.name)
                old_dataset.delete()
        
        return Response({
            'message': 'CSV uploaded and processed successfully',
            'dataset_id': dataset.id,
            'summary': summary
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_summary(request):
    try:
        latest_dataset = Dataset.objects.latest('uploaded_at')
        return Response({
            'summary': latest_dataset.summary,
            'uploaded_at': latest_dataset.uploaded_at
        })
    except Dataset.DoesNotExist:
        return Response(
            {'error': 'No datasets found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_history(request):
    datasets = Dataset.objects.all()[:5]
    serializer = DatasetSerializer(datasets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_pdf_report(request):
    try:
        latest_dataset = Dataset.objects.latest('uploaded_at')
        summary = latest_dataset.summary
    except Dataset.DoesNotExist:
        return Response(
            {'error': 'No datasets found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    title = Paragraph("Chemical Equipment Parameter Report", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    summary_data = [
        ['Metric', 'Value'],
        ['Total Equipment Count', str(summary['total_count'])],
        ['Average Flowrate', f"{summary['avg_flowrate']:.2f}"],
        ['Average Pressure', f"{summary['avg_pressure']:.2f}"],
        ['Average Temperature', f"{summary['avg_temperature']:.2f}"],
    ]
    
    summary_table = Table(summary_data)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    type_title = Paragraph("Equipment Type Distribution", styles['Heading2'])
    elements.append(type_title)
    elements.append(Spacer(1, 0.1*inch))
    
    type_data = [['Type', 'Count']]
    for eq_type, count in summary['type_distribution'].items():
        type_data.append([str(eq_type), str(count)])
    
    type_table = Table(type_data)
    type_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(type_table)
    
    doc.build(elements)
    buffer.seek(0)
    
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="equipment_report.pdf"'
    return response
