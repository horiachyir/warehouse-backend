from django.db import models

class NewsItem(models.Model):
    CATEGORY_CHOICES = [
        ('urgent', 'Urgent'),
        ('info', 'Information'),
        ('maintenance', 'Maintenance'),
        ('success', 'Success'),
        ('safety', 'Safety'),
    ]
    
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    
    title = models.CharField(max_length=200)
    summary = models.TextField()
    content = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    author = models.CharField(max_length=100, blank=True, help_text='Author name')
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'News Item'
        verbose_name_plural = 'News Items'

    def __str__(self):
        return self.title

class Video(models.Model):
    VIDEO_TYPE_CHOICES = [
        ('training', 'Training'),
        ('safety', 'Safety'),
        ('induction', 'Induction'),
        ('rsrg', 'RSRG'),
        ('red', 'RED Safety'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_type = models.CharField(max_length=20, choices=VIDEO_TYPE_CHOICES)
    thumbnail = models.ImageField(upload_to='video_thumbnails/', null=True, blank=True)
    video_url = models.URLField(blank=True, help_text='External video URL (YouTube, Vimeo, etc.)')
    video_file = models.FileField(upload_to='videos/', null=True, blank=True, help_text='Local video file')
    duration = models.DurationField(null=True, blank=True)
    uploaded_by = models.CharField(max_length=100, blank=True, help_text='Uploader name')
    is_featured = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
