from django.db import models

class RhombergVideo(models.Model):
    """Model to store videos from Rhomberg Sersa Rail Group YouTube channel"""

    video_id = models.CharField(max_length=50, unique=True, help_text='YouTube video ID')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    thumbnail_url = models.URLField(help_text='YouTube thumbnail URL')
    video_url = models.URLField(help_text='YouTube video URL')
    duration = models.CharField(max_length=20, blank=True, help_text='Video duration in ISO 8601 format')
    published_at = models.DateTimeField(help_text='YouTube video publish date')
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    channel_title = models.CharField(max_length=100, default='Rhomberg Sersa Rail Group')

    # Metadata fields
    fetched_at = models.DateTimeField(auto_now_add=True, help_text='When this record was fetched from YouTube')
    updated_at = models.DateTimeField(auto_now=True, help_text='When this record was last updated')
    is_active = models.BooleanField(default=True, help_text='Whether this video should be displayed')

    class Meta:
        db_table = 'rhomberg_videos'
        ordering = ['-published_at']
        verbose_name = 'Rhomberg Video'
        verbose_name_plural = 'Rhomberg Videos'

    def __str__(self):
        return self.title

class VideoFetchLog(models.Model):
    """Model to track YouTube API fetch operations for rate limiting"""

    fetch_date = models.DateTimeField(auto_now_add=True)
    videos_fetched = models.PositiveIntegerField(default=0)
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ['-fetch_date']
        verbose_name = 'Video Fetch Log'
        verbose_name_plural = 'Video Fetch Logs'

    def __str__(self):
        return f"Fetch on {self.fetch_date.strftime('%Y-%m-%d %H:%M')} - {self.videos_fetched} videos"
