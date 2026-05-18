from django.http import HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import render

from store.models import Product
import pydash


class Home(View):
    def get(self, request: HttpRequest):
        products = (
            Product.objects.filter(is_available=True).prefetch_related("images").all()
        )
        products = [
            {
                "name": p.name,
                "price": p.display_price,
                "slug": p.slug,
                "image_url": next(
                    (img.image.url for img in p.images.all() if img.is_main),
                    "https://placehold.co/600x400",
                ),
            }
            for p in products
        ]

        return render(request, "home.html", {"products": products})
