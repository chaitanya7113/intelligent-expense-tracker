import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        return response
    logger.exception("Unhandled exception: %s", exc, exc_info=True)
    return Response(
        {"detail": "An unexpected error occurred.", "error": str(exc)},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
