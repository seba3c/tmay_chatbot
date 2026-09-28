import logging

from litellm import completion
from pydantic import BaseModel, Field
from tenacity import retry, wait_exponential

from tmay_chatbot.core.chunking.chunker import Chunker
from tmay_chatbot.core.models import Document

logger = logging.getLogger(__name__)

_wait = wait_exponential(multiplier=1, min=10, max=240)


class LLMChunk(BaseModel):
    headline: str = Field(
        description="A brief heading for this chunk, typically a few words, that is most likely to be surfaced in a query",
    )
    summary: str = Field(
        description="A few sentences summarizing the content of this chunk to answer common questions"
    )
    original_text: str = Field(
        description="The original text of this chunk from the provided document, exactly as is, not changed in any way"
    )

    def to_document(self, metadata: dict) -> Document:
        return Document(
            content=self.headline + "\n\n" + self.summary + "\n\n" + self.original_text,
            metadata=metadata,
        )


class LLMChunks(BaseModel):
    chunks: list[LLMChunk]


class LLMChunker(Chunker):
    PROMPT_TEMPLATE = """
You take a document and you split the document into overlapping chunks for a KnowledgeBase.

The document is from the personal knowledge base of Tmay, used to answer questions about them, drawing on material such as their resume, academic work, GitHub projects, LinkedIn profile, personal stories, and website content.
The document is of type: {doc_type}
The document has been retrieved from: {source}

A chatbot will use these chunks to answer questions about Tmay.
You should divide up the document as you see fit, being sure that the entire document is returned across the chunks - don't leave anything out.
This document should probably be split into at least {how_many} chunks, but you can have more or less as appropriate, ensuring that there are individual chunks to answer specific questions.
There should be overlap between the chunks as appropriate; typically about 25% overlap or about 50 words, so you have the same text in multiple chunks for best retrieval results.

For each chunk, you should provide a headline, a summary, and the original text of the chunk.
Together your chunks should represent the entire document with overlap.

Here is the document:

{content}

Respond with the chunks.
"""

    def __init__(self, model: str, average_chunk_size: int = 100):
        self.model = model
        self.average_chunk_size = average_chunk_size

    def get_chunks(self, documents: list[Document]) -> list[Document]:
        logger.info(f"Chunking documents: {len(documents)}")
        flat_chunks = [
            chunk for document in documents for chunk in self._process_document(document)
        ]
        chunks = [
            Document(content=chunk.content, metadata={**chunk.metadata, "chunk_index": index})
            for index, chunk in enumerate(flat_chunks)
        ]
        logger.info(f"{len(chunks)} documents split into chunks")
        return chunks

    @retry(wait=_wait)
    def _process_document(self, document: Document) -> list[Document]:
        response = completion(
            model=self.model,
            messages=self._make_messages(document),
            response_format=LLMChunks,
        )
        reply = response.choices[0].message.content
        llm_chunks = LLMChunks.model_validate_json(reply).chunks
        return [chunk.to_document(metadata={**document.metadata}) for chunk in llm_chunks]

    def _make_messages(self, document: Document) -> list[dict]:
        return [{"role": "user", "content": self._make_prompt(document)}]

    def _make_prompt(self, document: Document) -> str:
        how_many = (len(document.content) // self.average_chunk_size) + 1
        return self.PROMPT_TEMPLATE.format(
            doc_type=document.metadata.get("doc_type", "unknown"),
            source=document.metadata.get("source", "unknown"),
            how_many=how_many,
            content=document.content,
        )
