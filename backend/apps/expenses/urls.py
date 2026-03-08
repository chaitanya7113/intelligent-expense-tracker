from django.urls import path, include
from apps.expenses.views import (
    ExpenseListCreateView,
    ExpenseDetailView,
    MonthlySummaryView,
    CategoryBreakdownView,
    MonthlyComparisonView,
)

urlpatterns = [
    path("expenses/", ExpenseListCreateView.as_view(), name="expense-list-create"),
    path("expenses/<int:pk>/", ExpenseDetailView.as_view(), name="expense-detail"),
    path("analytics/summary/", MonthlySummaryView.as_view(), name="analytics-summary"),
    path("analytics/by-category/", CategoryBreakdownView.as_view(), name="analytics-by-category"),
    path("analytics/monthly-comparison/", MonthlyComparisonView.as_view(), name="analytics-monthly-comparison"),
]
