from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from store.models import Product
import pydash


class StoreView(View):
    def get(self, request: HttpRequest):
        products = Product.objects.filter(is_available=True).all()
        products = [
            {
                "name": p.name,
                "price": p.price / 100,
                "image_url": pydash.get(
                    p.images.filter(is_main=True).first(), "image.url"
                )
                or "https://placehold.co/600x400",
            }
            for p in products
        ]
        return render(request, "store/index.html", {"products": products})
