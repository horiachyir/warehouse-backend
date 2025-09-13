from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Document(models.Model):
    CATEGORY_CHOICES = [
        ('maintenance', 'Maintenance'),
        ('operation', 'Operation'),
        ('safety', 'Safety'),
        ('training', 'Training'),
    ]
    
    TYPE_CHOICES = [
        ('PDF', 'PDF'),
        ('DOC', 'Word Document'),
        ('PPT', 'PowerPoint'),
        ('XLS', 'Excel'),
        ('TXT', 'Text'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    document_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    file = models.FileField(upload_to='documents/%Y/%m/')
    file_size = models.PositiveIntegerField(help_text='File size in bytes')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    download_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def formatted_file_size(self):
        """Return human readable file size"""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
