from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import View


class CartView(View):
    def get(self, request: HttpRequest):
        return render(request, "cart/main.html")
