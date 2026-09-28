from tmay_chatbot.core.context_repository.repository import (
    ChromaContextRepository,
    ContextRepository,
)
from tmay_chatbot.settings import settings


def get_context_repository() -> ContextRepository:
    return ChromaContextRepository(
        db_path=settings.vector_db_path,
        embedding_model=settings.embedding_model,
        collection_name=settings.collection_name,
    )
