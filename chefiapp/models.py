from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

from .helpers import MONTHS_DICT

ROLE_CHOICES = [
        ('admin', _('Admin')),
        ('management', _('Management')),
        ('staff', _('Staff')),
    ]

DEPARTMENT_CHOICES = [
        ('pizzaiolo', _('Pizzaiolo')),
        ('estafeta', _('Estafeta')),
        ('caixa', _('Caixa')),
        ('gerente', _('Gerente')),
    ]

class Department(models.Model):
    name = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, unique=True)
    workers = models.ManyToManyField('User', related_name='department_users', blank=True)

    def __str__(self):
        return f"${self.name}"

class User(AbstractUser):
    
    role = models.CharField(_('role'), max_length=20, choices=ROLE_CHOICES, blank=True)
    name = models.CharField(_('name'), max_length=120, blank=True)
    address = models.CharField(_('address'), max_length=255, blank=True)
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    department = models.CharField(_('department'), max_length=20, choices=DEPARTMENT_CHOICES, blank=True)
    
    departments = models.ManyToManyField(Department, related_name='users', blank=True)  

    is_staff = models.BooleanField(_('staff status'), default=True)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateField(_('date joined'), blank=True, null=True)

class PreCreateUser(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    department = models.CharField(_('department'), max_length=20, choices=DEPARTMENT_CHOICES, blank=True)

    activation_token = models.UUIDField(default=uuid.uuid4, editable=False)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.email
    
class MonthlySchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to link with the User model
    month = models.CharField(_('month'), max_length=15, choices=MONTHS_DICT)
    year = models.PositiveIntegerField(_('Year'), null=True, blank=True)

    class Meta:
        unique_together = ['user', 'month', 'year']

    def __str__(self):
        return f"{self.user.username}'s schedule for {self.month}"

class DailySchedule(models.Model):
    monthly_schedule = models.ForeignKey(MonthlySchedule, on_delete=models.CASCADE)
    date = models.DateField(_('date'))  # Day of the month
    start_hour = models.TimeField(blank=True, null=True)  # Start hour
    end_hour = models.TimeField(blank=True, null=True)  # End hour
    is_dayoff = models.BooleanField(default=False)

    class Meta:
        unique_together = ['date', 'monthly_schedule']

    def __str__(self):
        return f"{self.monthly_schedule.user.username}'s schedule on {self.date}"