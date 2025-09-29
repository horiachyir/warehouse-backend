# Generated manually for videos app

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RhombergVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_id', models.CharField(help_text='YouTube video ID', max_length=50, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('thumbnail_url', models.URLField(help_text='YouTube thumbnail URL')),
                ('video_url', models.URLField(help_text='YouTube video URL')),
                ('duration', models.CharField(blank=True, help_text='Video duration in ISO 8601 format', max_length=20)),
                ('published_at', models.DateTimeField(help_text='YouTube video publish date')),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('like_count', models.PositiveIntegerField(default=0)),
                ('channel_title', models.CharField(default='Rhomberg Sersa Rail Group', max_length=100)),
                ('fetched_at', models.DateTimeField(auto_now_add=True, help_text='When this record was fetched from YouTube')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='When this record was last updated')),
                ('is_active', models.BooleanField(default=True, help_text='Whether this video should be displayed')),
            ],
            options={
                'verbose_name': 'Rhomberg Video',
                'verbose_name_plural': 'Rhomberg Videos',
                'db_table': 'rhomberg_videos',
                'ordering': ['-published_at'],
            },
        ),
        migrations.CreateModel(
            name='VideoFetchLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fetch_date', models.DateTimeField(auto_now_add=True)),
                ('videos_fetched', models.PositiveIntegerField(default=0)),
                ('success', models.BooleanField(default=True)),
                ('error_message', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Video Fetch Log',
                'verbose_name_plural': 'Video Fetch Logs',
                'ordering': ['-fetch_date'],
            },
        ),
    ]