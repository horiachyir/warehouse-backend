import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from django.conf import settings
from django.utils import timezone
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .models import RhombergVideo, VideoFetchLog

logger = logging.getLogger(__name__)

class YouTubeService:
    """Service class for interacting with YouTube Data API v3"""

    CHANNEL_HANDLE = "@RhombergSersaRailGroup"
    CHANNEL_URL = "https://www.youtube.com/@RhombergSersaRailGroup"

    def __init__(self):
        self.api_key = settings.YOUTUBE_API_KEY
        self.channel_id = settings.YOUTUBE_CHANNEL_ID
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def get_channel_id(self) -> Optional[str]:
        """Get the channel ID - now directly from settings"""
        if self.channel_id:
            logger.info(f"Using channel ID from settings: {self.channel_id}")
            return self.channel_id

        logger.error("No channel ID found in settings")
        return None

    def get_channel_videos(self, max_results: int = 50) -> List[Dict]:
        """Fetch videos from the Rhomberg Sersa Rail Group channel"""
        try:
            # First get the channel ID
            channel_id = self.get_channel_id()
            if not channel_id:
                logger.error("Could not find channel ID")
                return []

            # Get the uploads playlist ID
            request = self.youtube.channels().list(
                part='contentDetails',
                id=channel_id
            )
            response = request.execute()

            if not response['items']:
                logger.error("Channel not found")
                return []

            uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

            # Get videos from the uploads playlist
            videos = []
            next_page_token = None

            while len(videos) < max_results:
                request = self.youtube.playlistItems().list(
                    part='snippet',
                    playlistId=uploads_playlist_id,
                    maxResults=min(50, max_results - len(videos)),
                    pageToken=next_page_token
                )
                response = request.execute()

                video_ids = [item['snippet']['resourceId']['videoId'] for item in response['items']]

                # Get detailed video information
                video_details_request = self.youtube.videos().list(
                    part='snippet,contentDetails,statistics',
                    id=','.join(video_ids)
                )
                video_details_response = video_details_request.execute()

                for video in video_details_response['items']:
                    video_data = self._parse_video_data(video)
                    if video_data:
                        videos.append(video_data)

                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break

            logger.info(f"Fetched {len(videos)} videos from YouTube")
            return videos

        except HttpError as e:
            logger.error(f"Error fetching videos from YouTube: {e}")
            return []

    def _parse_video_data(self, video: Dict) -> Optional[Dict]:
        """Parse video data from YouTube API response"""
        try:
            snippet = video['snippet']
            content_details = video['contentDetails']
            statistics = video['statistics']

            return {
                'video_id': video['id'],
                'title': snippet['title'],
                'thumbnail_url': snippet['thumbnails'].get('high', {}).get('url', ''),
                'video_url': f"https://www.youtube.com/watch?v={video['id']}",
                'duration': content_details.get('duration', ''),
                'published_at': datetime.fromisoformat(snippet['publishedAt'].replace('Z', '+00:00')),
                'view_count': int(statistics.get('viewCount', 0)),
                'like_count': int(statistics.get('likeCount', 0)),
                'channel_title': snippet['channelTitle']
            }
        except (KeyError, ValueError) as e:
            logger.error(f"Error parsing video data: {e}")
            return None

class RhombergVideoManager:
    """Manager class for Rhomberg video operations"""

    def __init__(self):
        self.youtube_service = YouTubeService()

    def should_fetch_videos(self) -> bool:
        """Check if we should fetch videos based on rate limiting"""
        # Check if we've fetched videos in the last 12 hours
        twelve_hours_ago = timezone.now() - timedelta(hours=12)
        recent_fetches = VideoFetchLog.objects.filter(
            fetch_date__gte=twelve_hours_ago,
            success=True
        ).count()

        # Allow maximum 2 successful fetches per 12 hours
        return recent_fetches < 2

    def fetch_and_store_videos(self) -> Dict[str, any]:
        """Fetch videos from YouTube and store them in the database"""
        if not self.should_fetch_videos():
            logger.info("Rate limit reached. Skipping video fetch.")
            return {
                'success': False,
                'message': 'Rate limit reached. Maximum 2 fetches per 12 hours.',
                'videos_updated': 0
            }

        try:
            # Fetch videos from YouTube
            videos = self.youtube_service.get_channel_videos()

            if not videos:
                # Log the attempt even if no videos were fetched
                VideoFetchLog.objects.create(
                    videos_fetched=0,
                    success=False,
                    error_message="No videos returned from YouTube API"
                )
                return {
                    'success': False,
                    'message': 'No videos fetched from YouTube',
                    'videos_updated': 0
                }

            # Store videos in database
            videos_updated = 0
            for video_data in videos:
                video, created = RhombergVideo.objects.update_or_create(
                    video_id=video_data['video_id'],
                    defaults=video_data
                )
                if created or video.updated_at < timezone.now() - timedelta(hours=1):
                    videos_updated += 1

            # Log successful fetch
            VideoFetchLog.objects.create(
                videos_fetched=len(videos),
                success=True
            )

            logger.info(f"Successfully stored/updated {videos_updated} videos")
            return {
                'success': True,
                'message': f'Successfully fetched and stored {len(videos)} videos',
                'videos_updated': videos_updated,
                'total_videos': len(videos)
            }

        except Exception as e:
            logger.error(f"Error in fetch_and_store_videos: {e}")
            # Log failed fetch
            VideoFetchLog.objects.create(
                videos_fetched=0,
                success=False,
                error_message=str(e)
            )
            return {
                'success': False,
                'message': f'Error fetching videos: {str(e)}',
                'videos_updated': 0
            }

    def get_cached_videos(self) -> List[RhombergVideo]:
        """Get videos from database cache"""
        return RhombergVideo.objects.filter(is_active=True).order_by('-published_at')

    def has_todays_data(self) -> bool:
        """Check if we have videos fetched today"""
        today = timezone.now().date()
        today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))
        today_end = timezone.make_aware(datetime.combine(today, datetime.max.time()))

        return RhombergVideo.objects.filter(
            fetched_at__gte=today_start,
            fetched_at__lte=today_end,
            is_active=True
        ).exists()

    def get_videos_for_list_endpoint(self) -> Dict[str, any]:
        """Get videos for /api/youtube/list/ endpoint - returns cached data if available, otherwise fetches from YouTube"""
        # Check if table has any data
        if RhombergVideo.objects.exists():
            # Return cached data without fetching from YouTube
            videos = self.get_cached_videos()
            return {
                'success': True,
                'message': f'Retrieved {videos.count()} videos from cache',
                'videos': list(videos.values()),
                'from_cache': True
            }
        else:
            # Fetch fresh data from YouTube only if table is empty
            result = self.fetch_and_store_videos()
            if result['success']:
                # Return the fresh data
                videos = self.get_cached_videos()
                result['videos'] = list(videos.values())
                result['from_cache'] = False
            return result

    def get_videos(self, force_refresh: bool = False) -> Dict[str, any]:
        """Get videos with smart caching logic"""
        if force_refresh or not RhombergVideo.objects.exists():
            # Fetch fresh data if forced or no cached data exists
            return self.fetch_and_store_videos()
        else:
            # Return cached data
            videos = self.get_cached_videos()
            return {
                'success': True,
                'message': f'Retrieved {videos.count()} videos from cache',
                'videos': list(videos.values()),
                'from_cache': True
            }