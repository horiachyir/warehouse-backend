from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    formatted_file_size = serializers.CharField(read_only=True)
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ['id', 'uploaded_by', 'created_at', 'updated_at', 'download_count']