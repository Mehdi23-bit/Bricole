from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    ROLE_CHOICES=[
        ('arisan','ARTISAN'),
        ('client','CLIENT'),
        ('admin','admin')
    ]
    
    phone_number=models.CharField(max_length=30,unique=True,null=True)
    adresse=models.CharField(max_length=30,null=True)
    role=models.CharField(max_length=30,choices=ROLE_CHOICES,default='client') 
    lat=models.FloatField(null=True)
    lan=models.FloatField(null=True)