from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from marketplace.models import Area


class Profile(models.Model):
    ROLE_CUSTOMER = "customer"
    ROLE_PROVIDER = "provider"
    ROLE_ADMIN = "admin"

    ROLE_CHOICES = [
        (ROLE_CUSTOMER, "Customer"),
        (ROLE_PROVIDER, "Provider"),
        (ROLE_ADMIN, "Admin"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CUSTOMER)
    phone = models.CharField(max_length=30, blank=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class ProviderProfile(models.Model):
    PLAN_FREE = "free"
    PLAN_PREMIUM = "premium"
    PLAN_CHOICES = [
        (PLAN_FREE, "Free"),
        (PLAN_PREMIUM, "Premium"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    services_count = models.PositiveIntegerField(default=0)
    rating_avg = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    plan_type = models.CharField(max_length=20, choices=PLAN_CHOICES, default=PLAN_FREE)
    plan_expires = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.business_name


def create_profile_for_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


models.signals.post_save.connect(create_profile_for_user, sender=User)
