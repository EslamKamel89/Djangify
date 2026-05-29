import pydash
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from store.models import Product


class Home(View):
    def get(self, request: HttpRequest):
        products = (
            Product.objects.filter(is_available=True).prefetch_related("images").all()
        )
        products = [
            {
                "id": p.pk,
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
