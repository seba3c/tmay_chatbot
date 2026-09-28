from tmay_chatbot.core.chunking.chunker import Chunker
from tmay_chatbot.core.chunking.llm_chunker import LLMChunker
from tmay_chatbot.core.chunking.recursive_character_chunker import RecursiveCharacterChunker
from tmay_chatbot.settings import settings


def get_recursive_char_chunker() -> Chunker:
    return RecursiveCharacterChunker()


def get_llm_chunker() -> Chunker:
    return LLMChunker(model=settings.chunking_model)
