from django.urls import path
from . import views

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news_list'),
    path('<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('videos/', views.VideoListView.as_view(), name='video_list'),
    path('videos/<int:pk>/', views.VideoDetailView.as_view(), name='video_detail'),
    path('videos/<int:pk>/view/', views.increment_video_views, name='increment_video_views'),
    path('videos/featured/', views.featured_videos, name='featured_videos'),
]