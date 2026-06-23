from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('technician', 'Technician'),
        ('staff', 'Staff'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    def is_admin(self):
        return self.role == 'admin'

    def is_technician(self):
        return self.role == 'technician'

    def is_staff_member(self):
        return self.role == 'staff'