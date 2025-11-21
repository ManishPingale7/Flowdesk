from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv'),
    path('summary/', views.get_summary, name='get_summary'),
    path('history/', views.get_history, name='get_history'),
    path('report/pdf/', views.generate_pdf_report, name='generate_pdf_report'),
]

