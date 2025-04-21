from django.http import HttpResponseForbidden

class BlockAllauthViewsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        blocked_paths = [
            '/accounts/login/',
            '/accounts/signup/',
            '/accounts/inactive',
            '/accounts/logout',
        ]

        if request.path in blocked_paths:
            return HttpResponseForbidden("Access denied to this page.")

        return self.get_response(request)
