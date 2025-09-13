from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from .models import CheckInRecord
from .serializers import CheckInRecordSerializer, CheckInSerializer, CheckOutSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def checkin_records(request):
    """Get today's check-in records"""
    today = timezone.now().date()
    records = CheckInRecord.objects.filter(created_at__date=today)
    serializer = CheckInRecordSerializer(records, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_in(request):
    """Check in an employee"""
    serializer = CheckInSerializer(data=request.data)
    if serializer.is_valid():
        employee_id = serializer.validated_data['employee_id']
        name = serializer.validated_data.get('name', f'Employee {employee_id}')
        
        # Check if user is already checked in today
        today = timezone.now().date()
        existing_record = CheckInRecord.objects.filter(
            employee_id=employee_id, 
            status='checked-in',
            created_at__date=today
        ).first()
        
        if existing_record:
            return Response({
                'error': f'Employee {employee_id} is already checked in'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create new check-in record
        record = CheckInRecord.objects.create(
            user=request.user,
            employee_id=employee_id,
            name=name,
            check_in_time=timezone.now(),
            status='checked-in'
        )
        
        return Response({
            'message': f'Check-in successful for {name}',
            'record': CheckInRecordSerializer(record).data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_out(request):
    """Check out an employee"""
    serializer = CheckOutSerializer(data=request.data)
    if serializer.is_valid():
        employee_id = serializer.validated_data['employee_id']
        
        # Find the checked-in record for today
        today = timezone.now().date()
        record = CheckInRecord.objects.filter(
            employee_id=employee_id, 
            status='checked-in',
            created_at__date=today
        ).first()
        
        if not record:
            return Response({
                'error': f'Employee {employee_id} is not currently checked in'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Update record with check-out time
        record.check_out_time = timezone.now()
        record.status = 'checked-out'
        record.save()
        
        return Response({
            'message': f'Check-out successful for {record.name}',
            'record': CheckInRecordSerializer(record).data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def staff_status(request):
    """Get current staff status (who's checked in/out today)"""
    today = timezone.now().date()
    records = CheckInRecord.objects.filter(created_at__date=today).order_by('-created_at')
    
    # Get latest record for each employee
    employee_status = {}
    for record in records:
        if record.employee_id not in employee_status:
            employee_status[record.employee_id] = record
    
    serializer = CheckInRecordSerializer(list(employee_status.values()), many=True)
    return Response(serializer.data)
