import logging

from tmay_chatbot.core.chunking.factory import get_llm_chunker
from tmay_chatbot.core.context_repository.factory import get_context_repository
from tmay_chatbot.core.knowledge_base import get_repository
from tmay_chatbot.ingestor.base import Ingestor

logger = logging.getLogger(__name__)


class AdvancedIngestor(Ingestor):
    def run(self):
        documents = get_repository().fetch_documents()
        chunks = get_llm_chunker().get_chunks(documents)
        get_context_repository().store(chunks)
        logger.info("Done!")
