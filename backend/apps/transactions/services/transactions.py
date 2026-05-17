# import logging
# from decimal import Decimal
# from django.db.models import QuerySet
# from apps.transactions.models import Transaction
# from apps.users.models import User

# logger=logging.getLogger(__name__)

# class TransactionService:

#     @staticmethod
#     def list_of_user(
#         user:User,
#         date_from=None,
#         date_to=None,
#         category_id=None,
#         source_id=None,
#         transaction_type=None
#     )->QuerySet:
#         qs=(Transaction.object.filter(user=user).select_related("category"))
