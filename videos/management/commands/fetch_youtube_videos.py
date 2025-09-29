from django.core.management.base import BaseCommand
from videos.services import RhombergVideoManager


class Command(BaseCommand):
    help = 'Fetch videos from Rhomberg Sersa Rail Group YouTube channel'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force fetch even if rate limit is reached',
        )

    def handle(self, *args, **options):
        manager = RhombergVideoManager()

        if options['force']:
            self.stdout.write('Forcing video fetch...')
            result = manager.fetch_and_store_videos()
        else:
            result = manager.get_videos()

        if result['success']:
            self.stdout.write(
                self.style.SUCCESS(f"✓ {result['message']}")
            )
            if 'videos_updated' in result:
                self.stdout.write(f"Videos updated: {result['videos_updated']}")
            if 'total_videos' in result:
                self.stdout.write(f"Total videos: {result['total_videos']}")
        else:
            self.stdout.write(
                self.style.ERROR(f"✗ {result['message']}")
            )