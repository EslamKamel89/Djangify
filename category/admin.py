from django.contrib import admin

from category.models import Category
from unfold.admin import ModelAdmin
from django.utils.html import format_html

# Register your models here.


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = (
        "name",
        "slug",
        "description",
        "created_at",
        "updated_at",
        "image_preview",
    )
    list_filter = ("created_at",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at", "image_preview")

    @admin.display(description="Image Preview")
    def image_preview(self, obj: Category):
        if obj.image:
            return format_html('<img src={} width="60" height="60" />', obj.image.url)
        return "-"
