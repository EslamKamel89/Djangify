from django.http import HttpRequest

from category.models import Category


def all_categories(request: HttpRequest):
    return {
        "all_categories": Category.objects.all(),
    }
