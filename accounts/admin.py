from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from accounts.models import User
from unfold.admin import ModelAdmin


@admin.register(User)
class CustomUserAdmin(UserAdmin, ModelAdmin):
    model = User
    list_display = (
        "id",
        "email",
        "username",
        "phone_number",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    list_display_links = ("id", "email", "username")
    ordering = ("id",)
    fieldsets = tuple(UserAdmin.fieldsets) + (
        (
            "Additional Info",
            {"fields": ("phone_number",)},
        ),
    )  # type: ignore
