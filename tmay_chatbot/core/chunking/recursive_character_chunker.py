import logging

from langchain_text_splitters import RecursiveCharacterTextSplitter

from tmay_chatbot.core.chunking.chunker import Chunker
from tmay_chatbot.core.models import Document

logger = logging.getLogger(__name__)


class RecursiveCharacterChunker(Chunker):
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def get_chunks(self, documents: list[Document]) -> list[Document]:
        logger.info(f"Chunking documents: {len(documents)}")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        lc_chunks = text_splitter.split_documents(
            [document.to_langchain_document() for document in documents]
        )
        chunks = [
            Document(
                content=lc_chunk.page_content,
                metadata={**lc_chunk.metadata, "chunk_index": index},
            )
            for index, lc_chunk in enumerate(lc_chunks)
        ]
        logger.info(f"{len(chunks)} documents split into chunks")
        return chunks
