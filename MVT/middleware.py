
import time
from django.http import JsonResponse

# Keep track of requests per IP
VISIT_LOG = {}

class LoginRateLimitMiddleware:
    """
    Middleware to limit login attempts per IP address.
    Example: max 5 login attempts per minute.
    """

    def __init__(self, get_response):
        # Django passes the next step (next middleware or view) as get_response - this is the next middleware or view to be called
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/api/login/" and request.method == "POST":  # this is the path and method we want to apply rate limiting to - Only apply rate limiting to POST /api/login/

            ip = self.get_client_ip(request)  # get client IP
            now = time.time()
            visits = VISIT_LOG.get(ip, [])

            # Keep only requests in the last 60 seconds
            visits = [t for t in visits if now - t < 60]

            # If more than 5 requests in last 60 seconds → block
            if len(visits) >= 5:
                return JsonResponse(
                    {"error": "Too many login attempts. Try again later."},
                    status=429
                )

            # Otherwise, add this request timestamp
            visits.append(now)
            VISIT_LOG[ip] = visits

        # Let the request continue to the view (or next middleware)
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """
        Get the client IP address.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip