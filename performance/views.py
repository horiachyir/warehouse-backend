from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import PerformanceMetric, DashboardData, StaffLocation
from .serializers import PerformanceMetricSerializer, DashboardDataSerializer, StaffLocationSerializer

class PerformanceMetricListView(generics.ListCreateAPIView):
    serializer_class = PerformanceMetricSerializer
    
    def get_queryset(self):
        queryset = PerformanceMetric.objects.filter(is_active=True)
        metric_type = self.request.query_params.get('type', None)
        period = self.request.query_params.get('period', None)
        
        if metric_type:
            queryset = queryset.filter(metric_type=metric_type)
        if period:
            queryset = queryset.filter(period=period)
            
        return queryset
    
    def perform_create(self, serializer):
        serializer.save()

class DashboardDataListView(generics.ListCreateAPIView):
    queryset = DashboardData.objects.all()
    serializer_class = DashboardDataSerializer

@api_view(['GET'])
def current_dashboard_data(request):
    """Get current dashboard data (today's or latest available)"""
    today = timezone.now().date()
    
    # Try to get today's data first
    dashboard_data = DashboardData.objects.filter(date=today).first()
    
    # If no data for today, get the latest available
    if not dashboard_data:
        dashboard_data = DashboardData.objects.first()
    
    if dashboard_data:
        serializer = DashboardDataSerializer(dashboard_data)
        return Response(serializer.data)
    else:
        # Return default data structure if no data exists
        return Response({
            'date': today,
            'spotlights_ytd': 81,
            'spotlights_mtd': 2,
            'safety_tour_ytd': 7.59,
            'safety_tour_mtd': 7.33,
            'possession_average': 63,
            'average_work_per_hour': 218.42,
            'in_process_critical': 65,
            'in_process_warning': 35,
            'possession_active': 75,
            'possession_inactive': 25,
            'preparation_status': 55,
            'breakdown_status': 45,
        })

class StaffLocationListView(generics.ListCreateAPIView):
    queryset = StaffLocation.objects.filter(is_in_depot=True)
    serializer_class = StaffLocationSerializer

@api_view(['POST'])
def update_staff_location(request):
    """Update current user's location"""
    location = request.data.get('location', '')
    is_in_depot = request.data.get('is_in_depot', True)
    
    # Since authentication is removed, we'll use a default approach
    # This endpoint might need rework for non-authenticated usage
    return Response({'message': 'Authentication removed - endpoint needs rework'}, status=status.HTTP_501_NOT_IMPLEMENTED)
    
    if not created:
        staff_location.location = location
        staff_location.is_in_depot = is_in_depot
        staff_location.save()
    
    serializer = StaffLocationSerializer(staff_location)
    return Response(serializer.data)

@api_view(['GET'])
def staff_in_depot(request):
    """Get list of staff currently in depot"""
    staff_locations = StaffLocation.objects.filter(is_in_depot=True)
    
    # Add some sample data if none exists
    if not staff_locations.exists():
        sample_staff = [
            {"user_name": "Darryl Gwilliam", "location": "Office"},
            {"user_name": "Robert Mullen", "location": "Office"},
            {"user_name": "Aidan Langley", "location": "Safety Tour"},
            {"user_name": "Colm Jones", "location": "Maintenance"},
            {"user_name": "Michael Sweetman", "location": "Testing 743"},
            {"user_name": "Declan Kilmurray", "location": "Hiding"},
        ]
        return Response(sample_staff)
    
    serializer = StaffLocationSerializer(staff_locations, many=True)
    return Response(serializer.data)
