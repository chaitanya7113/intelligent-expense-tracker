from django.db import models
from django.conf import settings


class TransactionSource(models.Model):
    class SourceType(models.TextChoices):
        BANK = "bank", "Bank"
        CREDIT_CARD = "credit_card", "Credit Card"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transaction_sources")
    name = models.CharField(max_length=100)
    source_type = models.CharField(max_length=20, choices=SourceType.choices, default=SourceType.BANK)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transaction_sources"

    def __str__(self):
        return f"{self.name} ({self.get_source_type_display()})"
