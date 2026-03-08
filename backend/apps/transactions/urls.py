from django.urls import path
from apps.transactions.views import StatementUploadView

urlpatterns = [
    path("statements/upload/", StatementUploadView.as_view(), name="statement-upload"),
]
