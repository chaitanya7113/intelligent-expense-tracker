import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.ai_agent.services import AgentService

logger = logging.getLogger(__name__)


class AgentChatView(APIView):
    def post(self, request):
        message = request.data.get("message", "").strip()
        history = request.data.get("history", [])

        if not message:
            return Response(
                {"error": "message is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not isinstance(history, list):
            history = []

        reply = AgentService.chat(user=request.user, message=message, history=history)
        return Response({"reply": reply})
