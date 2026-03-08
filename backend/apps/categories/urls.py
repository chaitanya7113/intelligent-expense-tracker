from django.urls import path
from apps.categories.views import CategoryListView

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
]
