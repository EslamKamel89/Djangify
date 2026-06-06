from django.db.models import Sum
from django.http import HttpRequest

from cart.models import Cart, CartItem


def cart_item_count(request: HttpRequest):
    session_key = request.session.session_key
    if not session_key:
        return {"count": 0}

    count = (
        CartItem.objects.filter(
            cart__session_id=session_key,
        )
        .aggregate(total=Sum("quantity"))
        .get("total")
        or 0
    )
    return {"count": count}
