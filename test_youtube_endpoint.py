#!/usr/bin/env python3
"""
Test script to verify the YouTube endpoint functionality with mock data
"""

import os
import sys
import django
from datetime import datetime, timezone as dt_timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'depot_hub.settings')
sys.path.append('/home/administrator/Documents/warehouse-backend')
django.setup()

from videos.models import RhombergVideo
from videos.services import RhombergVideoManager

def create_test_data():
    """Create some test video data"""
    print("Creating test video data...")

    # Create a test video from "today"
    test_video = RhombergVideo.objects.create(
        video_id="test123",
        title="Test Rhomberg Video",
        description="This is a test video from Rhomberg Sersa Rail Group",
        thumbnail_url="https://i.ytimg.com/vi/test123/maxresdefault.jpg",
        video_url="https://www.youtube.com/watch?v=test123",
        duration="PT5M30S",
        published_at=datetime.now(dt_timezone.utc),
        view_count=1000,
        like_count=50,
        channel_title="Rhomberg Sersa Rail Group"
    )

    print(f"Created test video: {test_video.title}")
    return test_video

def test_endpoint_logic():
    """Test the endpoint logic"""
    manager = RhombergVideoManager()

    print("\n--- Testing today's data check ---")
    has_today = manager.has_todays_data()
    print(f"Has today's data: {has_today}")

    print("\n--- Testing get_videos_for_list_endpoint ---")
    result = manager.get_videos_for_list_endpoint()

    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    print(f"From cache: {result.get('from_cache', False)}")
    print(f"Fetched today: {result.get('fetched_today', False)}")
    print(f"Number of videos: {len(result.get('videos', []))}")

    if result.get('videos'):
        video = result['videos'][0]
        print(f"First video title: {video['title']}")

if __name__ == "__main__":
    print("Testing YouTube endpoint functionality...")

    # Clean up any existing test data
    RhombergVideo.objects.filter(video_id="test123").delete()

    # Create test data
    test_video = create_test_data()

    # Test the logic
    test_endpoint_logic()

    print("\n✅ Test completed successfully!")
    print("\nThe /api/youtube/list/ endpoint will:")
    print("1. Check if rhomberg_videos table has data from today")
    print("2. If YES: Return cached data")
    print("3. If NO: Fetch fresh data from YouTube API")