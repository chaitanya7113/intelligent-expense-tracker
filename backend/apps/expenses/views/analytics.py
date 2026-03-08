from rest_framework.views import APIView
from rest_framework.response import Response

from ..services import AnalyticsService


class MonthlySummaryView(APIView):
    def get(self, request):
        year = request.query_params.get("year")
        month = request.query_params.get("month")
        year = int(year) if year else None
        month = int(month) if month else None
        data = AnalyticsService.monthly_summary(request.user, year=year, month=month)
        return Response(data)


class CategoryBreakdownView(APIView):
    def get(self, request):
        year = request.query_params.get("year")
        month = request.query_params.get("month")
        year = int(year) if year else None
        month = int(month) if month else None
        data = AnalyticsService.category_breakdown(request.user, year=year, month=month)
        return Response(data)


class MonthlyComparisonView(APIView):
    def get(self, request):
        year = request.query_params.get("year")
        months = request.query_params.get("months", 6)
        year = int(year) if year else None
        months = int(months) if months else 6
        data = AnalyticsService.monthly_comparison(request.user, year=year, months=months)
        return Response(data)
