import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from .models import RhombergVideo, VideoFetchLog
from .serializers import RhombergVideoSerializer, VideoFetchLogSerializer
from .services import RhombergVideoManager

logger = logging.getLogger(__name__)

@extend_schema_view(
    list=extend_schema(
        summary="List Rhomberg videos",
        description="Get a list of videos from Rhomberg Sersa Rail Group YouTube channel",
        tags=["Videos"]
    ),
    retrieve=extend_schema(
        summary="Get specific video",
        description="Get details of a specific Rhomberg video",
        tags=["Videos"]
    ),
)
class RhombergVideoViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Rhomberg videos"""

    queryset = RhombergVideo.objects.filter(is_active=True).order_by('-published_at')
    serializer_class = RhombergVideoSerializer
    permission_classes = [AllowAny]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.video_manager = RhombergVideoManager()

    @extend_schema(
        summary="Refresh video data",
        description="Fetch latest videos from YouTube API and update the database",
        tags=["Videos"],
        parameters=[
            OpenApiParameter(
                name="force",
                description="Force refresh even if rate limit is reached",
                required=False,
                type=bool,
                location=OpenApiParameter.QUERY
            )
        ]
    )
    @action(detail=False, methods=['post'])
    def refresh(self, request):
        """Refresh video data from YouTube API"""
        force_refresh = request.query_params.get('force', 'false').lower() == 'true'

        try:
            if force_refresh:
                result = self.video_manager.fetch_and_store_videos()
            else:
                result = self.video_manager.get_videos()

            if result['success']:
                return Response({
                    'message': result['message'],
                    'videos_updated': result.get('videos_updated', 0),
                    'total_videos': result.get('total_videos', 0),
                    'from_cache': result.get('from_cache', False)
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': result['message']
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error in refresh endpoint: {e}")
            return Response({
                'error': 'Internal server error while refreshing videos'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        summary="Get video statistics",
        description="Get statistics about video fetching and storage",
        tags=["Videos"]
    )
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get video statistics"""
        try:
            total_videos = RhombergVideo.objects.filter(is_active=True).count()
            recent_fetches = VideoFetchLog.objects.order_by('-fetch_date')[:5]

            latest_fetch = recent_fetches.first()
            can_fetch = self.video_manager.should_fetch_videos()

            stats_data = {
                'total_videos': total_videos,
                'latest_fetch': {
                    'date': latest_fetch.fetch_date if latest_fetch else None,
                    'videos_fetched': latest_fetch.videos_fetched if latest_fetch else 0,
                    'success': latest_fetch.success if latest_fetch else False
                } if latest_fetch else None,
                'can_fetch_now': can_fetch,
                'recent_fetches': VideoFetchLogSerializer(recent_fetches, many=True).data
            }

            return Response(stats_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error in stats endpoint: {e}")
            return Response({
                'error': 'Internal server error while getting statistics'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema_view(
    list=extend_schema(
        summary="List video fetch logs",
        description="Get a list of video fetch operations",
        tags=["Video Logs"]
    ),
)
class VideoFetchLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for video fetch logs"""

    queryset = VideoFetchLog.objects.all().order_by('-fetch_date')
    serializer_class = VideoFetchLogSerializer
    permission_classes = [AllowAny]


@extend_schema(
    summary="Get YouTube video list",
    description="Get Rhomberg videos with smart caching - returns today's cache if available, otherwise fetches fresh data from YouTube",
    tags=["YouTube"],
    responses={
        200: {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "message": {"type": "string"},
                "videos": {"type": "array", "items": {"$ref": "#/components/schemas/RhombergVideo"}},
                "from_cache": {"type": "boolean"},
                "fetched_today": {"type": "boolean"},
                "total_videos": {"type": "integer"}
            }
        },
        400: {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "error": {"type": "string"}
            }
        }
    }
)
@api_view(['GET'])
@permission_classes([AllowAny])
def youtube_list(request):
    """
    API endpoint for /api/youtube/list/

    If rhomberg_videos table contains data loaded today, return cached data.
    If not, fetch fresh data from YouTube API.
    """
    try:
        manager = RhombergVideoManager()
        result = manager.get_videos_for_list_endpoint()

        if result['success']:
            return Response({
                'success': True,
                'message': result['message'],
                'videos': result['videos'],
                'from_cache': result.get('from_cache', False),
                'fetched_today': result.get('fetched_today', False),
                'total_videos': len(result['videos']),
                'videos_updated': result.get('videos_updated', 0)
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'error': result['message']
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Error in youtube_list endpoint: {e}")
        return Response({
            'success': False,
            'error': 'Internal server error while getting YouTube videos'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
