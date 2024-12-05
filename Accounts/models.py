from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .manager import AccountManager

from django.utils.timezone import now
from datetime import timedelta


class UserAccount(AbstractBaseUser, PermissionsMixin):
    regno = models.CharField(max_length=20, unique=True)  
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    section = models.CharField(max_length=10)
    password = models.CharField(max_length=128)  

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Required for admin interface access
    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'regno' 
    REQUIRED_FIELDS = ['name', 'email', 'section']

    def __str__(self):
        return self.regno
    

class Verification(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return now() < self.created_at + timedelta(minutes=5)
