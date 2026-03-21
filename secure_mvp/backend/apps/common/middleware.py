from django.conf import settings


class RequestContextAuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.request_id = request.META.get("HTTP_X_REQUEST_ID", "")
        return self.get_response(request)


class ContentSecurityPolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        policy = "; ".join(
            f"{directive} {' '.join(values)}"
            for directive, values in settings.CSP_POLICY.items()
        )
        response["Content-Security-Policy"] = policy
        response["X-Content-Type-Options"] = "nosniff"
        response["Referrer-Policy"] = settings.SECURE_REFERRER_POLICY
        response["X-Frame-Options"] = settings.X_FRAME_OPTIONS
        response["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        return response
