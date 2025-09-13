from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'employee_id', 'phone', 'department', 'role', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 
                 'employee_id', 'phone', 'department', 'role', 
                 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
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