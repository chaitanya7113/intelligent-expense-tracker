from rest_framework import serializers
from apps.transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Transaction
        fields = (
            "id", "source", "date", "description", "amount", "transaction_type",
            "category", "category_name", "created_at",
        )
        read_only_fields = ("id", "created_at")


class UploadStatementSerializer(serializers.Serializer):
    file = serializers.FileField(allow_empty_file=False)
    source_name = serializers.CharField(required=False, default="Uploaded Statement", max_length=100)
