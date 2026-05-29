from django.urls import path

from . import views

urlpatterns = [
    path("", views.CartView.as_view(), name="cart_view"),
    path("items/update/", views.update_cart_item, name="update_cart_item"),
]
