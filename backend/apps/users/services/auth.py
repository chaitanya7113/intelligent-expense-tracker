import logging
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()
logger = logging.getLogger(__name__)


class AuthService:
    @staticmethod
    def register(username: str, email: str, password: str) -> User:
        if User.objects.filter(username=username).exists():
            raise ValueError("A user with that username already exists.")
        if User.objects.filter(email=email).exists():
            raise ValueError("A user with that email already exists.")
        user = User.objects.create_user(username=username, email=email, password=password)
        logger.info("User registered: %s", user.username)
        return user

    @staticmethod
    def get_tokens_for_user(user: User) -> dict:
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": user,
        }
