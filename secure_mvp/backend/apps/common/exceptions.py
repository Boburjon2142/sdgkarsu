import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


security_logger = logging.getLogger("django.security")


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        return response

    request = context.get("request")
    view = context.get("view")
    security_logger.exception(
        "unhandled_api_error path=%s view=%s",
        getattr(request, "path", "unknown"),
        view.__class__.__name__ if view else "unknown",
    )
    return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
