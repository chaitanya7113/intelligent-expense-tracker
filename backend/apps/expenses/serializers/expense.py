from rest_framework import serializers
from apps.expenses.models import Expense
from apps.categories.models import Category


class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Expense
        fields = ("id", "amount", "date", "category", "category_name", "description", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_category(self, value):
        if value is not None and not Category.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError("Invalid category.")
        return value


class ExpenseListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Expense
        fields = ("id", "amount", "date", "category", "category_name", "description", "created_at", "updated_at")
