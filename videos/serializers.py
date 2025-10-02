from rest_framework import serializers
from .models import RhombergVideo, VideoFetchLog

class RhombergVideoSerializer(serializers.ModelSerializer):
    """Serializer for Rhomberg Video model"""

    class Meta:
        model = RhombergVideo
        fields = [
            'id',
            'video_id',
            'title',
            'thumbnail_url',
            'video_url',
            'duration',
            'published_at',
            'view_count',
            'like_count',
            'channel_title',
            'fetched_at',
            'is_active'
        ]
        read_only_fields = ['id', 'fetched_at']

class VideoFetchLogSerializer(serializers.ModelSerializer):
    """Serializer for Video Fetch Log model"""

    class Meta:
        model = VideoFetchLog
        fields = [
            'id',
            'fetch_date',
            'videos_fetched',
            'success',
            'error_message'
        ]
        read_only_fields = ['id', 'fetch_date']