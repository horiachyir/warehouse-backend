from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RhombergVideoViewSet, VideoFetchLogViewSet, youtube_list

router = DefaultRouter()
router.register(r'rhomberg-videos', RhombergVideoViewSet, basename='rhomberg-videos')
router.register(r'video-logs', VideoFetchLogViewSet, basename='video-logs')

urlpatterns = [
    path('', include(router.urls)),
]