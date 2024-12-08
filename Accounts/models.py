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
    is_staff = models.BooleanField(default=False)  
    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'regno' 
    REQUIRED_FIELDS = ['name', 'email', 'section']

    def __str__(self):
        return self.regno
    

class Verification(models.Model):
    user = models.ForeignKey(UserAccount,on_delete=models.CASCADE,related_name="verifications",null=True,blank=True)
    otp = models.CharField(max_length=6)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(null=True, blank=True) 
    
    def is_valid(self):
        return now() < self.updated_at + timedelta(minutes=5)
    
    def __str__(self):
        if self.user:
            return f"OTP for {self.user.email} is {self.otp}"
        return f"OTP (unlinked) is {self.otp}"



from django.db import models
from django.utils.timezone import now


class UserActivityLog(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True, blank=True)
    request_path = models.CharField(max_length=255)  # Store the path of the request
    request_method = models.CharField(max_length=10)  # GET, POST, etc.
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # User's IP
    user_agent = models.TextField(null=True, blank=True)  # Browser or client information
    timestamp = models.DateTimeField(default=now)  # Log time
    additional_info = models.JSONField(null=True, blank=True)  # For extra context

    def __str__(self):
        return f"Log for {self.user.name if self.user else 'Anonymous'} on {self.timestamp}"
