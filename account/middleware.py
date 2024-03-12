from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    # It checks if the current request path matches either the
    #  login or register URL using the reverse function to generate the URLs based on their names.
    # If the request path matches one of these URLs, it redirects the user to the LOGIN_REDIRECT_URL specified in the Django settings.
    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            if request.path in [reverse('login'), reverse('register')]:
                return redirect(settings.LOGIN_REDIRECT_URL)
        return response
