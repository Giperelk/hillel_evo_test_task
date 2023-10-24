from django.utils import timezone


class UserLastRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        user = request.user

        response = self.get_response(request)

        if user.is_authenticated:

            user.last_request = timezone.now()
            user.save()

        return response


class UserLastLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        was_not_auth = not user.is_authenticated
        response = self.get_response(request)

        if user.is_authenticated and was_not_auth:
            user.last_login = timezone.now()
            user.save()

        return response
