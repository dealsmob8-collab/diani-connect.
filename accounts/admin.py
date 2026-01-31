from django.contrib import admin

from .models import Profile, ProviderProfile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "phone", "area")
    list_filter = ("role", "area")
    search_fields = ("user__username", "phone")


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ("business_name", "user", "verified", "plan_type", "services_count")
    list_filter = ("verified", "plan_type")
    search_fields = ("business_name", "user__username")
