import pydash
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from cart.models import Cart, CartItem
from category.models import Category
from djangify.utils import pr
from store.models import Product


class StoreView(View):
    def get(self, request: HttpRequest):
        products = Product.objects.prefetch_related("images").filter(is_available=True)
        selected_category_slug = request.GET.get("category", None)
        selected_category = None
        if selected_category_slug:
            selected_category = get_object_or_404(Category, slug=selected_category_slug)
            products = products.filter(category__slug=selected_category_slug)
        q = request.GET.get("q", None)
        if q and q.strip():
            products = products.filter(
                Q(name__icontains=q.strip()) | Q(description__icontains=q.strip())
            )
        products_count = products.count()
        per_page = request.GET.get("per_page", "6")
        per_page = per_page if per_page.isdigit() else "6"
        page = request.GET.get("page", "1")
        page = int(page) if page.isdigit() else 1
        paginator = Paginator(products, per_page)
        page_obj = paginator.get_page(page)
        products = [
            {
                "id": p.pk,
                "name": p.name,
                "price": p.display_price,
                "original_price": p.original_price,
                "image_url": next(
                    (
                        img.image.url
                        for img in p.images.all()  # type: ignore
                        if img.is_main and img.image
                    ),
                    "https://placehold.co/600x400",
                ),
                "slug": p.slug,
            }
            for p in page_obj.object_list
        ]
        return render(
            request,
            "store/index.html",
            {
                "products": products,
                "products_count": products_count,
                "selected_category": selected_category,
                "page_obj": page_obj,
                "pages": range(1, page_obj.paginator.num_pages + 1),
                "curr_page": page,
                "per_page": per_page,
                "per_page_options": ["6", "12", "24", "48"],
            },
        )


class ProductDetailsView(View):
    def get(self, request: HttpRequest, product_slug: str):
        product = get_object_or_404(
            Product.objects.prefetch_related("images"),
            slug=product_slug,
            is_available=True,
        )
        images = product.images.order_by("-is_main")  # type: ignore
        if not request.session.session_key:
            request.session.create()
        cart_item = CartItem.objects.filter(
            cart__session_id=request.session.session_key, product=product
        ).first()
        return render(
            request,
            "store/product_detail.html",
            {
                "product": product,
                "cart_item": cart_item,
                "images": images,
                "main_image": pydash.get(images.first(), ".image.url"),
            },
        )
