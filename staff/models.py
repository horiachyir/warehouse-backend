from django.db import models

class CheckInRecord(models.Model):
    STATUS_CHOICES = [
        ('checked-in', 'Checked In'),
        ('checked-out', 'Checked Out'),
    ]

    company = models.CharField(max_length=100, default='Unknown')
    name = models.CharField(max_length=100, default='Unknown')
    reason = models.CharField(max_length=100, default='Unknown')
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='checked-out')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'staff_checkinrecord'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.company}) - {self.reason}"
