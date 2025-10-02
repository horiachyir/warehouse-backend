from rest_framework import serializers
from .models import CheckInRecord

class CheckInRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckInRecord
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class CheckInSerializer(serializers.Serializer):
    employee_id = serializers.CharField(max_length=20)
    name = serializers.CharField(max_length=100, required=False)

class CheckOutSerializer(serializers.Serializer):
    employee_id = serializers.CharField(max_length=20)

class DepotCheckInSerializer(serializers.Serializer):
    company = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    reason = serializers.CharField(max_length=100)