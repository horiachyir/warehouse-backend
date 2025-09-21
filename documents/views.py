from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from .models import Document
from .serializers import DocumentSerializer

class DocumentListView(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    
    def get_queryset(self):
        queryset = Document.objects.filter(is_active=True)
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset
    
    def perform_create(self, serializer):
        # Calculate file size
        file_obj = self.request.FILES.get('file')
        if file_obj:
            serializer.save(
                file_size=file_obj.size
            )

class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.filter(is_active=True)
    serializer_class = DocumentSerializer

@api_view(['POST'])
def download_document(request, pk):
    """Download a document and increment download count"""
    document = get_object_or_404(Document, pk=pk, is_active=True)
    
    # Increment download count
    document.download_count += 1
    document.save(update_fields=['download_count'])
    
    # Return file response
    try:
        response = HttpResponse(
            document.file.read(),
            content_type='application/octet-stream'
        )
        response['Content-Disposition'] = f'attachment; filename="{document.file.name.split("/")[-1]}"'
        return response
    except Exception as e:
        return Response(
            {'error': 'File not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
def document_categories(request):
    """Get list of available document categories"""
    from .models import Document
    categories = [
        {'value': choice[0], 'label': choice[1]}
        for choice in Document.CATEGORY_CHOICES
    ]
    return Response(categories)
