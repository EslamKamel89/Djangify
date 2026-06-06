from django.http import HttpRequest


def pr[T](val: T, title="") -> T:
    print(title, val)
    print("type = ", type(val))
    return val


def redirect_url(request: HttpRequest):
    return request.META.get(
        "HTTP_REFERER",
        "/",
    )
