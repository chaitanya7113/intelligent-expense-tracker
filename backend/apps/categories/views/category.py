from rest_framework.views import APIView
from rest_framework.response import Response
from apps.categories.models import Category


class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all().order_by("name")
        return Response([{"id": c.id, "name": c.name} for c in categories])
