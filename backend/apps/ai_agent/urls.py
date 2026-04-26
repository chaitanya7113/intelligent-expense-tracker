from django.urls import path
from apps.ai_agent.views import AgentChatView

urlpatterns = [
    path("ai/chat/", AgentChatView.as_view(), name="ai-chat"),
]
