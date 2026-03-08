import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from apps.transactions.serializers import TransactionSerializer, UploadStatementSerializer
from apps.transactions.services import StatementParserService

logger = logging.getLogger(__name__)


class StatementUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = UploadStatementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data["file"]
        source_name = serializer.validated_data.get("source_name") or "Uploaded Statement"
        if not file.name.lower().endswith(".csv"):
            return Response(
                {"detail": "Only CSV files are allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            content = file.read()
            transactions = StatementParserService.parse_csv(
                content, user=request.user, source_name=source_name
            )
        except Exception as e:
            logger.exception("Statement upload failed: %s", e)
            return Response(
                {"detail": "Failed to parse CSV.", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "message": f"Imported {len(transactions)} transactions.",
                "count": len(transactions),
                "transactions": TransactionSerializer(transactions[:50], many=True).data,
            },
            status=status.HTTP_201_CREATED,
        )
