from tmay_chatbot.chatbot.v1 import TmayChatBotV1
from tmay_chatbot.chatbot.v2 import TmayChatBotV2
from tmay_chatbot.core.context_repository.factory import get_context_repository
from tmay_chatbot.settings import settings


def get_chatbot():
    if settings.version == "v1":
        return TmayChatBotV1(
            chat_model=settings.chat_model,
            context_repository=get_context_repository(),
        )
    elif settings.version == "v2":
        return TmayChatBotV2(
            chat_model=settings.chat_model,
            context_repository=get_context_repository(),
        )
    raise RuntimeError(f"Unknown version: {settings.version}")
