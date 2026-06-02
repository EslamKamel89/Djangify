from typing import Iterable, Optional, cast

from django.db import models
from django.db.models.fields.related_descriptors import ReverseManyToOneDescriptor
from django.db.models.query import QuerySet
from django.utils.text import slugify

from category.models import Category


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255, unique=True, null=False)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=False)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    @property
    def display_price(self):
        return f"{self.price / 100:.2f}"

    @property
    def original_price(self):
        return f"{(self.price * 1.2) / 100:.2f}"

    @property
    def main_image(self) -> str:
        main_image = cast(ProductImage | None, self.images.filter(is_main=True).first())  # type: ignore
        if main_image:
            return main_image.image.url
        return "https://placehold.co/600x400"

    class Meta:
        ordering = ("name",)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to="images/products/")
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.product.name} Image"
