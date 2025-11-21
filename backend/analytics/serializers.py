from rest_framework import serializers
from .models import Dataset


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id', 'file_path', 'summary', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

