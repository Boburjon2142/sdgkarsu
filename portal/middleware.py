class PortalLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language_code = request.session.get("portal_language", "en")
        if language_code not in {"uz", "en"}:
            language_code = "en"
        request.LANGUAGE_CODE = language_code
        response = self.get_response(request)
        response.set_cookie("portal_language", language_code)
        return response
