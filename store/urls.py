from django.urls import path

from . import views

urlpatterns = [
    path("", views.StoreView.as_view(), name="store"),
    path(
        "products/<slug:product_slug>/",
        views.ProductDetailsView.as_view(),
        name="product_details",
    ),
]
