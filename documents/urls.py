from django.urls import path
from . import views

urlpatterns = [
    path('', views.DocumentListView.as_view(), name='document_list'),
    path('<int:pk>/', views.DocumentDetailView.as_view(), name='document_detail'),
    path('<int:pk>/download/', views.download_document, name='download_document'),
    path('categories/', views.document_categories, name='document_categories'),
]