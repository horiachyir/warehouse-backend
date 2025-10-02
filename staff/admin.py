from django.contrib import admin
from .models import CheckInRecord

@admin.register(CheckInRecord)
class CheckInRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'status', 'check_in_time', 'check_out_time', 'reason')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'company', 'reason')
    readonly_fields = ('created_at', 'updated_at')
