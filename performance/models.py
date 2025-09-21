from django.db import models

class PerformanceMetric(models.Model):
    METRIC_TYPE_CHOICES = [
        ('spotlights', 'Spotlight Reports'),
        ('safety_tours', 'Safety Tours'),
        ('possession_utilization', 'Possession Utilization'),
        ('in_process_status', 'In Process Status'),
        ('preparation_status', 'Preparation Status'),
    ]
    
    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    metric_type = models.CharField(max_length=30, choices=METRIC_TYPE_CHOICES)
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    target_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=20, blank=True)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='monthly')
    date = models.DateField()
    created_by = models.CharField(max_length=100, blank=True, help_text='Name of creator')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['metric_type', 'name', 'date']

    def __str__(self):
        return f"{self.name} - {self.value} ({self.date})"

    def performance_percentage(self):
        """Calculate performance as percentage of target if target exists"""
        if self.target_value:
            return round((float(self.value) / float(self.target_value)) * 100, 2)
        return None

class DashboardData(models.Model):
    """Model to store daily dashboard data"""
    date = models.DateField(unique=True)
    spotlights_ytd = models.IntegerField(default=0)
    spotlights_mtd = models.IntegerField(default=0)
    safety_tour_ytd = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    safety_tour_mtd = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    possession_average = models.IntegerField(default=0)
    average_work_per_hour = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    in_process_critical = models.IntegerField(default=0)
    in_process_warning = models.IntegerField(default=0)
    possession_active = models.IntegerField(default=0)
    possession_inactive = models.IntegerField(default=0)
    preparation_status = models.IntegerField(default=0)
    breakdown_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Dashboard Data - {self.date}"

class StaffLocation(models.Model):
    """Model to track staff current location in depot"""
    user_name = models.CharField(max_length=100, help_text='Staff member name')
    location = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)
    is_in_depot = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user_name} - {self.location}"
