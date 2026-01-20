from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        HANDYMAN = "handyman", "Handyman"
        ADMIN = "admin", "Admin"

    username = models.CharField(max_length=150, unique=False, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to="profile", default="profile/default.png")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.email} ({self.role})"


class HandymanProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="handyman_profile"
    )
    bio = models.TextField(blank=True, null=True)
    skills = models.JSONField(default=list, blank=True)
    city = models.CharField(max_length=120)
    hourly_rate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    availability = models.CharField(max_length=255, blank=True, null=True)
    years_experience = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"HandymanProfile({self.user.email})"
