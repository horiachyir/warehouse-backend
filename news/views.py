from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import NewsItem, Video
from .serializers import NewsItemSerializer, VideoSerializer

class NewsListView(generics.ListCreateAPIView):
    serializer_class = NewsItemSerializer
    
    def get_queryset(self):
        queryset = NewsItem.objects.filter(is_published=True)
        category = self.request.query_params.get('category', None)
        priority = self.request.query_params.get('priority', None)
        
        if category:
            queryset = queryset.filter(category=category)
        if priority:
            queryset = queryset.filter(priority=priority)
            
        return queryset
    
    def perform_create(self, serializer):
        serializer.save()

class NewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NewsItem.objects.filter(is_published=True)
    serializer_class = NewsItemSerializer

class VideoListView(generics.ListCreateAPIView):
    serializer_class = VideoSerializer
    
    def get_queryset(self):
        queryset = Video.objects.filter(is_active=True)
        video_type = self.request.query_params.get('type', None)
        
        if video_type:
            queryset = queryset.filter(video_type=video_type)
            
        return queryset
    
    def perform_create(self, serializer):
        serializer.save()

class VideoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.filter(is_active=True)
    serializer_class = VideoSerializer

@api_view(['POST'])
def increment_video_views(request, pk):
    """Increment video view count"""
    video = get_object_or_404(Video, pk=pk, is_active=True)
    video.view_count += 1
    video.save(update_fields=['view_count'])
    return Response({'message': 'View count updated'})

@api_view(['GET'])
def featured_videos(request):
    """Get featured videos"""
    videos = Video.objects.filter(is_featured=True, is_active=True)
    serializer = VideoSerializer(videos, many=True)
    return Response(serializer.data)
