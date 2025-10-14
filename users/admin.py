from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "email", "registration_source", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password", "is_active", "is_staff",)}),
        ("Important dates", {"fields": ("last_login",)}),
    )
    ordering = ("last_login",)