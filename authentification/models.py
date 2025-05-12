from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    ROLE_CHOICES=[
        ('artisan','ARTISAN'),
        ('client','CLIENT'),
        ('admin','admin')
    ]
    
    phone_number=models.CharField(max_length=30,unique=True,null=True)
    adresse=models.CharField(max_length=30,null=True)
    photo=models.ImageField(upload_to='profile',default='profile/default.png')
    role=models.CharField(max_length=30,choices=ROLE_CHOICES,default='client') 
    lat=models.FloatField(null=True)
    lan=models.FloatField(null=True)