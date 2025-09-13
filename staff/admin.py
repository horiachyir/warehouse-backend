from django.contrib import admin
from .models import CheckInRecord

@admin.register(CheckInRecord)
class CheckInRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee_id', 'status', 'check_in_time', 'check_out_time', 'location')
    list_filter = ('status', 'created_at', 'location')
    search_fields = ('name', 'employee_id')
    readonly_fields = ('created_at', 'updated_at')
