from django.conf import settings
from django.shortcuts import redirect


class FirstMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        list_urls = ["/login/", "/register/"]

        if not request.user.is_authenticated and request.path not in list_urls:
            return redirect(settings.LOGIN_URL)

        response = self.get_response(request)
        return response