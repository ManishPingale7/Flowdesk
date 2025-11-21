from django.contrib import admin
from .models import Dataset


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
	list_display = ('id', 'uploaded_at')
	readonly_fields = ('uploaded_at',)
	search_fields = ('file_path',)
	list_filter = ('uploaded_at',)

