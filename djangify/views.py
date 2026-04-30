from django.http import HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import render


class Home(View):
    def get(self, request: HttpRequest):
        return render(request, "home.html")
