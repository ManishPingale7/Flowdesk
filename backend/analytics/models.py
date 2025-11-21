from django.db import models


class Dataset(models.Model):
    file_path = models.FileField(upload_to='csv_files/')
    summary = models.JSONField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"Dataset {self.id} - {self.uploaded_at}"
