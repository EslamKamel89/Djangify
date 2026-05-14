from typing import TYPE_CHECKING, Iterable

from django.db import models
from django.utils.text import slugify
from django.db.models.query import QuerySet

if TYPE_CHECKING:
    from store.models import Product


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="images/categories/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    products: QuerySet["Product"]

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            base_slug = slugify(self.name)
            counter = 1
            slug = base_slug
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{slug}-{counter}"
                counter += 1
            self.slug = slug
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name = "Category"
        verbose_name_plural = "Categories"
