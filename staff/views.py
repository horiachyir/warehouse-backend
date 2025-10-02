from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from .models import CheckInRecord
from .serializers import CheckInRecordSerializer, CheckInSerializer, CheckOutSerializer, DepotCheckInSerializer

@api_view(['GET'])
def checkin_records(request):
    """Get today's check-in records"""
    today = timezone.now().date()
    records = CheckInRecord.objects.filter(created_at__date=today)
    serializer = CheckInRecordSerializer(records, many=True)
    return Response(serializer.data)

@api_view(['POST'])
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

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def depot_checkin(request):
    """
    GET: Get all check-in records (both checked-in and checked-out)
    POST: Check in a visitor to the depot
    """
    if request.method == 'GET':
        # Get all check-in records
        all_records = CheckInRecord.objects.all().order_by('-created_at')
        serializer = CheckInRecordSerializer(all_records, many=True)
        return Response({
            'success': True,
            'count': all_records.count(),
            'records': serializer.data
        })

    elif request.method == 'POST':
        serializer = DepotCheckInSerializer(data=request.data)
        if serializer.is_valid():
            company = serializer.validated_data['company']
            name = serializer.validated_data['name']
            reason = serializer.validated_data['reason']

            # Check if a record with the same name, company, and reason already exists (regardless of status)
            existing_record = CheckInRecord.objects.filter(
                company=company,
                name=name,
                reason=reason
            ).first()

            if existing_record:
                return Response({
                    'success': False,
                    'error': 'You are aleady registered!'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Create new check-in record
            record = CheckInRecord.objects.create(
                company=company,
                name=name,
                reason=reason,
                check_in_time=timezone.now(),
                status='checked-in'
            )

            return Response({
                'success': True,
                'message': f'Check-in successful for {name}',
                'record': CheckInRecordSerializer(record).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def depot_checkout(request, record_id):
    """Check out a visitor from the depot"""
    try:
        record = CheckInRecord.objects.get(id=record_id)
    except CheckInRecord.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Check-in record not found'
        }, status=status.HTTP_404_NOT_FOUND)

    # Check if already checked out
    if record.status == 'checked-out':
        return Response({
            'success': False,
            'error': 'This visitor is already checked out'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Update record with check-out time
    record.check_out_time = timezone.now()
    record.status = 'checked-out'
    record.save()

    return Response({
        'success': True,
        'message': f'Check-out successful for {record.name}',
        'record': CheckInRecordSerializer(record).data
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def depot_recheckin(request, record_id):
    """Re-check in a visitor who was previously checked out"""
    try:
        record = CheckInRecord.objects.get(id=record_id)
    except CheckInRecord.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Check-in record not found'
        }, status=status.HTTP_404_NOT_FOUND)

    # Check if already checked in
    if record.status == 'checked-in':
        return Response({
            'success': False,
            'error': 'This visitor is already checked in'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Update record to checked-in status
    record.check_in_time = timezone.now()
    record.status = 'checked-in'
    record.save()

    return Response({
        'success': True,
        'message': f'Re-check-in successful for {record.name}',
        'record': CheckInRecordSerializer(record).data
    })
