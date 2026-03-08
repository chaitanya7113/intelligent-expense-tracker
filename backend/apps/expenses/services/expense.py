import logging
from decimal import Decimal
from django.db.models import QuerySet
from django.utils import timezone

from apps.expenses.models import Expense
from apps.users.models import User

logger = logging.getLogger(__name__)


class ExpenseService:
    @staticmethod
    def list_for_user(
        user: User,
        date_from=None,
        date_to=None,
        category_id=None,
    ) -> QuerySet:
        qs = Expense.objects.filter(user=user).select_related("category")
        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)
        if category_id is not None:
            qs = qs.filter(category_id=category_id)
        return qs.order_by("-date", "-created_at")

    @staticmethod
    def create(user: User, amount: Decimal, date, category_id=None, description: str = "") -> Expense:
        expense = Expense.objects.create(
            user=user,
            amount=amount,
            date=date,
            category_id=category_id,
            description=description or "",
        )
        logger.info("Expense created: id=%s user=%s amount=%s", expense.id, user.id, amount)
        return expense

    @staticmethod
    def update(expense: Expense, **kwargs) -> Expense:
        for key, value in kwargs.items():
            if hasattr(expense, key):
                setattr(expense, key, value)
        expense.save(update_fields=list(kwargs.keys()))
        logger.info("Expense updated: id=%s", expense.id)
        return expense

    @staticmethod
    def delete(expense: Expense) -> None:
        expense_id = expense.id
        expense.delete()
        logger.info("Expense deleted: id=%s", expense_id)
