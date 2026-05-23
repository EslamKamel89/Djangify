from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from cart.models import Cart, CartItem


class CartItemAdmin(TabularInline):
    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = (
        "user",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id", "user")
    inlines = [CartItemAdmin]
    readonly_fields = ("created_at", "updated_at")
