from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from django.utils.html import format_html
from store.models import Product, ProductImage


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ("image_preview",)
    fields = (
        "image",
        "image_preview",
        "is_main",
    )

    @admin.display(description="Preview")
    def image_preview(self, obj: ProductImage):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" />', obj.image.url)
        return "-"


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ("name", "slug", "price")
    list_display_links = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]
    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "category",
                    "name",
                    "slug",
                    "description",
                )
            },
        ),
        (
            "Pricing & Inventory",
            {
                "fields": (
                    "price",
                    "stock",
                )
            },
        ),
        (
            "Availability",
            {"fields": ("is_available",)},
        ),
        (
            "Metadata",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
    search_fields = (
        "name",
        "slug",
    )

    list_filter = (
        "category",
        "is_available",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
