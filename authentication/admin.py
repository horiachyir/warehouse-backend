from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'employee_id', 'department', 'role', 'is_active')
    list_filter = ('department', 'role', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'employee_id')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('employee_id', 'phone', 'department', 'role')
        }),
    )
