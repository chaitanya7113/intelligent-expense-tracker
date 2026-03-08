import logging
from datetime import date
from django.db.models import Sum, Q
from django.utils import timezone

from apps.expenses.models import Expense
from apps.users.models import User

logger = logging.getLogger(__name__)


class AnalyticsService:
    @staticmethod
    def monthly_summary(user: User, year: int = None, month: int = None) -> dict:
        qs = Expense.objects.filter(user=user)
        if year is not None:
            qs = qs.filter(date__year=year)
        if month is not None:
            qs = qs.filter(date__month=month)
        total = qs.aggregate(total=Sum("amount"))["total"] or 0
        return {
            "year": year or timezone.now().year,
            "month": month or timezone.now().month,
            "total_spending": float(total),
            "count": qs.count(),
        }

    @staticmethod
    def category_breakdown(user: User, year: int = None, month: int = None) -> list:
        from django.db.models import Count
        qs = Expense.objects.filter(user=user)
        if year is not None:
            qs = qs.filter(date__year=year)
        if month is not None:
            qs = qs.filter(date__month=month)
        breakdown = list(
            qs.values("category__id", "category__name")
            .annotate(total=Sum("amount"), count=Count("id"))
            .order_by("-total")
        )
        return [
            {
                "category_id": b["category__id"],
                "category_name": b["category__name"] or "Uncategorized",
                "total": float(b["total"] or 0),
                "count": b["count"],
            }
            for b in breakdown
        ]

    @staticmethod
    def monthly_comparison(user: User, year: int = None, months: int = 6) -> list:
        from dateutil.relativedelta import relativedelta
        now = timezone.now().date()
        result = []
        for i in range(months):
            d = now - relativedelta(months=i)
            d = d.replace(day=1)
            total = (
                Expense.objects.filter(user=user, date__year=d.year, date__month=d.month).aggregate(
                    total=Sum("amount")
                )["total"]
                or 0
            )
            result.append({
                "year": d.year,
                "month": d.month,
                "month_label": d.strftime("%Y-%m"),
                "total_spending": float(total),
            })
        return result
