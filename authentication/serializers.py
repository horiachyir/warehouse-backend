from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import datetime
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                 'employee_id', 'phone', 'department', 'role', 'visit_reason',
                 'visit_date', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=6)
    confirmPassword = serializers.CharField(write_only=True)
    date = serializers.DateTimeField(required=True)
    visitReason = serializers.CharField(required=True)

    def validate(self, attrs):
        # Check if passwords match
        if attrs['password'] != attrs['confirmPassword']:
            raise serializers.ValidationError("Passwords don't match")

        # Validate visit reason
        valid_reasons = ['employee', 'visitor', 'contractor', 'delivery', 'other']
        if attrs['visitReason'] not in valid_reasons:
            raise serializers.ValidationError(f"Invalid visit reason. Must be one of: {', '.join(valid_reasons)}")

        return attrs

    def create(self, validated_data):
        # Extract email to use as username
        email = validated_data['email']
        username = email.split('@')[0]  # Use email prefix as username

        # Check if username already exists and make it unique if necessary
        base_username = username
        counter = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        # Create the user
        user = CustomUser(
            username=username,
            email=email,
            visit_reason=validated_data['visitReason'],
            visit_date=validated_data['date']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    name_or_email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        name_or_email = attrs.get('name_or_email')
        password = attrs.get('password')

        if name_or_email and password:
            # Try to authenticate with username first, then email
            user = authenticate(username=name_or_email, password=password)
            if not user:
                # Try with email
                try:
                    user_by_email = CustomUser.objects.get(email=name_or_email)
                    user = authenticate(username=user_by_email.username, password=password)
                except CustomUser.DoesNotExist:
                    pass

            if not user:
                raise serializers.ValidationError('Invalid credentials')
            
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must provide username/email and password')