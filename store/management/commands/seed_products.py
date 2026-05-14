from typing import Any

from django.core.management.base import BaseCommand

from category.models import Category
from store.models import Product, ProductImage


class Command(BaseCommand):
    help = "Seed Products Data"

    def handle(self, *args: Any, **options: Any) -> str | None:
        products = [
            {
                "category": "Jackets",
                "name": "US Polo Assn Jacket",
                "description": (
                    "Premium casual jacket designed for lightweight comfort "
                    "and modern streetwear styling."
                ),
                "price": 22000,
                "stock": 15,
                "is_available": True,
                "images": [
                    {
                        "image": "images/products/US-Polo-Assn_Jacket.jpg",
                        "is_main": True,
                    },
                ],
            },
            {
                "category": "Jeans",
                "name": "ATX Jeans",
                "description": (
                    "Slim-fit denim jeans crafted for everyday comfort "
                    "with a clean modern finish."
                ),
                "price": 14000,
                "stock": 30,
                "is_available": True,
                "images": [
                    {
                        "image": "images/products/ATX-Jeans.jpg",
                        "is_main": True,
                    },
                    {
                        "image": "images/products/jeans_1.jpg",
                        "is_main": False,
                    },
                    {
                        "image": "images/products/jeans_2.jpg",
                        "is_main": False,
                    },
                    {
                        "image": "images/products/jeans_3.jpg",
                        "is_main": False,
                    },
                ],
            },
            {
                "category": "Jeans",
                "name": "Mavi Jeans",
                "description": (
                    "Stretch denim jeans with a relaxed fit " "for casual daily wear."
                ),
                "price": 16500,
                "stock": 18,
                "is_available": True,
                "images": [
                    {
                        "image": "images/products/Mavi_jeans.jpg",
                        "is_main": True,
                    },
                ],
            },
            {
                "category": "Shirts",
                "name": "Blue Shirt",
                "description": (
                    "Classic blue shirt tailored for smart casual "
                    "and office-ready outfits."
                ),
                "price": 12000,
                "stock": 22,
                "is_available": True,
                "images": [
                    {
                        "image": "images/products/Blue-Shirt.jpg",
                        "is_main": True,
                    },
                ],
            },
            {
                "category": "Shirts",
                "name": "Wrangler Shirt",
                "description": (
                    "Comfortable cotton shirt with a timeless design "
                    "for versatile everyday styling."
                ),
                "price": 13500,
                "stock": 20,
                "is_available": True,
                "images": [
                    {
                        "image": "images/products/Wrangler-Shirt.jpg",
                        "is_main": True,
                    },
                ],
            },
            {
                "category": "Shoes",
                "name": "Jordan True Flight Basketball Shoes",
                "description": (
                    "Performance basketball shoes offering ankle support, "
                    "comfort, and modern athletic styling."
                ),
                "price": 32000,
                "stock": 12,
                "is_available": True,
                "images": [
                    {
                        "image": (
                            "images/products/" "jordan-true-flight-basketball-shoes.jpg"
                        ),
                        "is_main": True,
                    },
                ],
            },
            {
                "category": "Shoes",
                "name": "Puma Ferrari Shoes",
                "description": (
                    "Motorsport-inspired sneakers combining sporty aesthetics "
                    "with lightweight comfort."
                ),
                "price": 28000,
                "stock": 10,
                "is_available": True,
                "images": [
                    {
                        "image": "images/products/Puma-Ferrari-Shoes.jpg",
                        "is_main": True,
                    },
                ],
            },
            {
                "category": "T-Shirts",
                "name": "Great Tshirt",
                "description": (
                    "Minimal everyday t-shirt made from soft cotton "
                    "with a modern relaxed fit."
                ),
                "price": 8000,
                "stock": 40,
                "is_available": True,
                "images": [
                    {
                        "image": "images/products/Great-Tshirt.jpg",
                        "is_main": True,
                    },
                ],
            },
        ]
        for product_data in products:
            category = Category.objects.get(name=product_data["category"])
            product, created = Product.objects.update_or_create(
                name=product_data["name"],
                defaults={
                    "category": category,
                    "description": product_data["description"],
                    "price": product_data["price"],
                    "stock": product_data["stock"],
                    "is_available": product_data["is_available"],
                },
            )
            ProductImage.objects.filter(product=product).delete()
            for image_data in product_data["images"]:
                ProductImage.objects.create(
                    product=product,
                    image=image_data["image"],
                    is_main=image_data["is_main"],
                )
            action = "created" if created else "updated"
            self.stdout.write(self.style.SUCCESS(f"{action} product: {product.name}"))
