from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View

from cart.forms import UpdateCartItemForm
from cart.models import Cart, CartItem


def update_cart_item(request: HttpRequest):
    if request.method != "POST":
        raise PermissionDenied()
    form = UpdateCartItemForm(request.POST)
    if not form.is_valid():
        return JsonResponse(
            {"errors": form.errors},
            status=400,
        )
    product = form.product
    quantity = form.cleaned_data["quantity"]
    action = form.cleaned_data["action"]
    if not request.session.session_key:
        request.session.create()
    cart, _ = Cart.objects.get_or_create(
        session_id=request.session.session_key,
    )
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={
            "price_at_purchase": product.price,
        },
    )
    current_quantity = item.quantity
    if created:
        current_quantity = 0
    if action == "inc":
        new_quantity = current_quantity + quantity
    else:
        new_quantity = current_quantity - quantity

    if new_quantity <= 0:
        item.delete()
        return redirect("cart_view")
    if new_quantity > product.stock:
        raise PermissionDenied("Insufficient stock")

    item.quantity = new_quantity

    item.save(
        update_fields=[
            "quantity",
            "updated_at",
        ]
    )

    return redirect("cart_view")


class CartView(View):
    def get(self, request: HttpRequest):
        return render(request, "cart/main.html")
