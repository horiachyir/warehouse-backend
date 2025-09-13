from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username
