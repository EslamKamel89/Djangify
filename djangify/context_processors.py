from django.http import HttpRequest


def query_params(request: HttpRequest):
    return {"query_params": request.GET}
