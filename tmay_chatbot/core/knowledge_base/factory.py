from tmay_chatbot.core.knowledge_base.repository import (
    KnowledgeBaseRepository,
    MarkdownKnowledgeBaseRepository,
)
from tmay_chatbot.settings import settings


def get_repository() -> KnowledgeBaseRepository:
    return MarkdownKnowledgeBaseRepository(settings.knowledge_base_path)
