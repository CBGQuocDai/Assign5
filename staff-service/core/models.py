from django.db import models


class Staff(models.Model):
    ROLE_CHOICES = [('staff', 'Staff'), ('senior_staff', 'Senior Staff'), ('supervisor', 'Supervisor')]
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='staff')
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

    class Meta:
        db_table = 'staff'
