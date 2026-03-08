from django.db import models
from django.conf import settings
from apps.categories.models import Category
from .transaction_source import TransactionSource


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        DEBIT = "debit", "Debit"
        CREDIT = "credit", "Credit"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    source = models.ForeignKey(
        TransactionSource, on_delete=models.CASCADE, related_name="transactions", null=True, blank=True
    )
    date = models.DateField()
    description = models.CharField(max_length=500)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions"
    )
    raw_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transactions"
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"{self.date} {self.description} {self.amount}"
