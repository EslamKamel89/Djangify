from typing import Any

from django.core.management.base import BaseCommand

from category.models import Category


class Command(BaseCommand):
    help = "Seed Categories Data"

    def handle(self, *args: Any, **options: Any) -> str | None:
        categories = [
            {
                "name": "Jackets",
                "description": (
                    "Premium outerwear including winter jackets, "
                    "lightweight bombers, and casual everyday layers."
                ),
                "image": "images/categories/jackets.png",
            },
            {
                "name": "Jeans",
                "description": (
                    "Modern denim collection featuring slim fit, "
                    "relaxed fit, and stretch jeans for everyday wear."
                ),
                "image": "images/categories/jeans.png",
            },
            {
                "name": "Shirts",
                "description": (
                    "Formal and casual shirts crafted for comfort, "
                    "office wear, and smart styling."
                ),
                "image": "images/categories/shirts.png",
            },
            {
                "name": "Shoes",
                "description": (
                    "Lifestyle and performance footwear including "
                    "sneakers, boots, and casual shoes."
                ),
                "image": "images/categories/shoes.png",
            },
            {
                "name": "T-Shirts",
                "description": (
                    "Essential cotton t-shirts with modern cuts, "
                    "graphic prints, and minimal everyday styles."
                ),
                "image": "images/categories/tshirts.png",
            },
        ]
        for category_data in categories:
            category, created = Category.objects.update_or_create(
                name=category_data["name"],
                defaults={
                    "description": category_data["description"],
                    "image": category_data["image"],
                },
            )
            action = "created" if created else "updated"
            self.stdout.write(self.style.SUCCESS(f"{action} category: {category.name}"))
