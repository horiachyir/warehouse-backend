from rest_framework import serializers
from .models import PerformanceMetric, DashboardData, StaffLocation

class PerformanceMetricSerializer(serializers.ModelSerializer):
    performance_percentage = serializers.ReadOnlyField()
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = PerformanceMetric
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

class DashboardDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardData
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class StaffLocationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = StaffLocation
        fields = '__all__'
        read_only_fields = ['id', 'updated_at']