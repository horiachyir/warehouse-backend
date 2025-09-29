from django.contrib import admin
from .models import RhombergVideo, VideoFetchLog

@admin.register(RhombergVideo)
class RhombergVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'view_count', 'like_count', 'is_active', 'fetched_at')
    list_filter = ('is_active', 'published_at', 'fetched_at')
    search_fields = ('title', 'description', 'video_id')
    readonly_fields = ('video_id', 'fetched_at', 'updated_at')
    ordering = ('-published_at',)

@admin.register(VideoFetchLog)
class VideoFetchLogAdmin(admin.ModelAdmin):
    list_display = ('fetch_date', 'videos_fetched', 'success')
    list_filter = ('success', 'fetch_date')
    readonly_fields = ('fetch_date',)
    ordering = ('-fetch_date',)
