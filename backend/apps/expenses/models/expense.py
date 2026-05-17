from django.db import models
from django.conf import settings
from apps.categories.models import Category


class Expense(models.Model):
    class Type(models.TextChoices):
        EXPENSE = "EXPENSE", "Expense"
        INCOME = "INCOME", "Income"

    type = models.CharField(max_length=10, choices=Type.choices, default=Type.EXPENSE)
    

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="expenses")
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="expenses", null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "expenses"
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.amount} - {self.date}"
