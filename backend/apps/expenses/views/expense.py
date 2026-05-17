import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from apps.expenses.models import Expense
from apps.expenses.serializers import ExpenseSerializer, ExpenseListSerializer
from apps.expenses.services import ExpenseService

logger = logging.getLogger(__name__)


class ExpenseListCreateView(APIView):
    def get(self, request):
        user = request.user
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")
        category = request.query_params.get("category")
        category_id = int(category) if category and category.isdigit() else None
        tx_type = request.query_params.get("type")  # INCOME / EXPENSE

        qs = ExpenseService.list_for_user(
            user,
            date_from=date_from,
            date_to=date_to,
            category_id=category_id,
            type=tx_type,
        )

        from rest_framework.pagination import PageNumberPagination
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = ExpenseListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        tx_type = data.get("type", Expense.Type.EXPENSE)

        expense = ExpenseService.create(
            user=request.user,
            type=tx_type,
            amount=data["amount"],
            date=data["date"],
            category_id=data.get("category").id if data.get("category") else None,
            description=data.get("description", ""),
        )
        return Response(ExpenseSerializer(expense).data, status=status.HTTP_201_CREATED)


class ExpenseDetailView(APIView):
    def get_object(self, request, pk):
        expense = Expense.objects.filter(user=request.user, pk=pk).first()
        if not expense:
            from rest_framework.exceptions import NotFound
            raise NotFound("Expense not found.")
        return expense

    def get(self, request, pk):
        expense = self.get_object(request, pk)
        return Response(ExpenseSerializer(expense).data)

    def put(self, request, pk):
        expense = self.get_object(request, pk)
        serializer = ExpenseSerializer(expense, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        ExpenseService.update(
            expense,
            amount=data.get("amount", expense.amount),
            date=data.get("date", expense.date),
            category=data.get("category") if "category" in data else expense.category,
            description=data.get("description", expense.description),
        )
        expense.refresh_from_db()
        return Response(ExpenseSerializer(expense).data)

    def delete(self, request, pk):
        expense = self.get_object(request, pk)
        ExpenseService.delete(expense)
        return Response(status=status.HTTP_204_NO_CONTENT)


