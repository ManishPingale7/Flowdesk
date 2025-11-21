from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.http import HttpResponse, FileResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from .models import Dataset
from .serializers import DatasetSerializer, CSVUploadSerializer, RegisterSerializer
from .utils import parse_csv, compute_summary
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'User registered successfully',
            'username': user.username
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    doc = SimpleDocTemplate(buffer, pagesize=letter, 
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    title = Paragraph("Chemical Equipment Parameter Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    summary_heading = Paragraph("Summary Statistics", heading_style)
    elements.append(summary_heading)
    elements.append(Spacer(1, 0.15*inch))
    
    summary_data = [
        ['Metric', 'Value'],
        ['Total Equipment Count', str(summary['total_count'])],
        ['Average Flowrate', f"{summary['avg_flowrate']:.2f}"],
        ['Average Pressure', f"{summary['avg_pressure']:.2f}"],
        ['Average Temperature', f"{summary['avg_temperature']:.2f}"],
    ]
    
    summary_table = Table(summary_data, colWidths=[4*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1e293b')),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.4*inch))
    
    type_heading = Paragraph("Equipment Type Distribution", heading_style)
    elements.append(type_heading)
    elements.append(Spacer(1, 0.15*inch))
    
    type_data = [['Equipment Type', 'Count']]
    for eq_type, count in summary['type_distribution'].items():
        type_data.append([str(eq_type), str(count)])
    
    type_table = Table(type_data, colWidths=[4*inch, 2*inch])
    type_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7c3aed')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1e293b')),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
    ]))
    elements.append(type_table)
    elements.append(Spacer(1, 0.4*inch))
    
    charts_heading = Paragraph("Visualizations", heading_style)
    elements.append(charts_heading)
    elements.append(Spacer(1, 0.15*inch))
    
    chart_buffer1 = io.BytesIO()
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    types = list(summary['type_distribution'].keys())
    counts = list(summary['type_distribution'].values())
    colors_list = ['#2563eb', '#7c3aed', '#10b981', '#f59e0b', '#ef4444']
    ax1.pie(counts, labels=types, autopct='%1.1f%%', colors=colors_list[:len(types)], 
            startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
    ax1.set_title('Equipment Type Distribution', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(chart_buffer1, format='png', dpi=150, bbox_inches='tight')
    plt.close()
    chart_buffer1.seek(0)
    
    chart_img1 = Image(chart_buffer1, width=5*inch, height=3.3*inch)
    elements.append(chart_img1)
    elements.append(Spacer(1, 0.3*inch))
    
    chart_buffer2 = io.BytesIO()
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    stats = ['Flowrate', 'Pressure', 'Temperature']
    values = [
        summary['avg_flowrate'],
        summary['avg_pressure'],
        summary['avg_temperature']
    ]
    bars = ax2.bar(stats, values, color=['#2563eb', '#10b981', '#f59e0b'], 
                    edgecolor='white', linewidth=1.5)
    ax2.set_title('Average Statistics', fontsize=14, fontweight='bold', pad=20)
    ax2.set_ylabel('Value', fontweight='bold', fontsize=11)
    ax2.grid(True, alpha=0.3, axis='y', linestyle='--')
    ax2.set_axisbelow(True)
    
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}', ha='center', va='bottom', 
                fontweight='bold', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(chart_buffer2, format='png', dpi=150, bbox_inches='tight')
    plt.close()
    chart_buffer2.seek(0)
    
    chart_img2 = Image(chart_buffer2, width=5*inch, height=3.3*inch)
    elements.append(chart_img2)
    
    doc.build(elements)
    buffer.seek(0)
    
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="equipment_report.pdf"'
    return response
