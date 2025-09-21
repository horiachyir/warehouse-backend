from django.db import models

class CheckInRecord(models.Model):
    STATUS_CHOICES = [
        ('checked-in', 'Checked In'),
        ('checked-out', 'Checked Out'),
    ]
    
    # Removed user field - check-ins are now tracked by employee_id only
    employee_id = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='checked-out')
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.employee_id}) - {self.status}"
