import pydash
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from category.models import Category
from djangify.utils import pr
from store.models import Product


class StoreView(View):
    def get(self, request: HttpRequest):
        products = (
            Product.objects.prefetch_related("images").filter(is_available=True).all()
        )
        selected_category_slug = request.GET.get("category", None)
        selected_category = None
        if selected_category_slug:
            selected_category = get_object_or_404(Category, slug=selected_category_slug)
            products = products.filter(category__slug=selected_category_slug)
        products_count = products.count()
        products = [
            {
                "id": p.pk,
                "name": p.name,
                "price": p.display_price,
                "original_price": p.original_price,
                "image_url": next(
                    (
                        img.image.url
                        for img in p.images.all()
                        if img.is_main and img.image
                    ),
                    "https://placehold.co/600x400",
                ),
                "slug": p.slug,
            }
            for p in products
        ]
        return render(
            request,
            "store/index.html",
            {
                "products": products,
                "products_count": products_count,
                "selected_category": selected_category,
            },
        )


class ProductDetailsView(View):
    def get(self, request: HttpRequest, product_slug: str):
        product = get_object_or_404(
            Product.objects.prefetch_related("images"),
            slug=product_slug,
            is_available=True,
        )
        images = product.images.order_by("-is_main")
        return render(
            request,
            "store/product_detail.html",
            {
                "product": product,
                "images": images,
                "main_image": pydash.get(images.first(), ".image.url"),
            },
        )
