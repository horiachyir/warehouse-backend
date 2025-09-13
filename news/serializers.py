from rest_framework import serializers
from .models import NewsItem, Video

class NewsItemSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = NewsItem
        fields = '__all__'
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

class VideoSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    
    class Meta:
        model = Video
        fields = '__all__'
        read_only_fields = ['id', 'uploaded_by', 'created_at', 'updated_at', 'view_count']