import logging

from litellm import completion
from pydantic import BaseModel, Field
from tenacity import retry, wait_exponential

from tmay_chatbot.chatbot.base import TmayChatbot
from tmay_chatbot.core.context_repository.repository import ContextRepository
from tmay_chatbot.core.models import RetrievedDocument

logger = logging.getLogger(__name__)

_wait = wait_exponential(multiplier=1, min=10, max=240)


class RankOrder(BaseModel):
    order: list[int] = Field(
        description="The order of relevance of chunks, from most relevant to least relevant, by chunk id number"
    )


class TmayChatBotV2(TmayChatbot):
    RETRIEVAL_K = 20
    FINAL_K = 10

    RERANK_SYSTEM_PROMPT = """
You are a document re-ranker.
You are provided with a question and a list of relevant chunks of text from a query of a knowledge base.
The chunks are provided in the order they were retrieved; this should be approximately ordered by relevance, but you may be able to improve on that.
You must rank order the provided chunks by relevance to the question, with the most relevant chunk first.
Reply only with the list of ranked chunk ids, nothing else. Include all the chunk ids you are provided with, reranked.
"""

    REWRITE_QUERY_PROMPT_TEMPLATE = """
You are in a conversation with a user.
You are about to look up information in a Knowledge Base to answer the user's question.

This is the history of your conversation so far with the user:
{history}

And this is the user's current question:
{question}

Since the conversation is contextual, understand the meaning of the user question and add details based on the history.
Condense everything in a single contextually-rich VERY short and specific question, most likely to surface content.

EXAMPLE:
user: Who is the founder? -> Query: who is the founder?
assistant: The founder is FooBar
user: What role covers? -> Query: What role FooBar covers?
...

IMPORTANT: Respond ONLY with the precise knowledgebase query, nothing else.
"""

    def __init__(self, chat_model: str, context_repository: ContextRepository):
        super().__init__(context_repository)
        self.chat_model = chat_model

    def fetch_context(
        self, question: str, history: list[dict] | None = None
    ) -> list[RetrievedDocument]:
        """
        Retrieve relevant context for a question via query rewriting, dual retrieval
        (original + rewritten query) and LLM-based reranking.
        """
        history = history or []
        rewritten_question = self._rewrite_query(question, history)
        logger.info(f"Rewritten query: {rewritten_question}")
        original_chunks = self.context_repository.fetch(question, k=self.RETRIEVAL_K)
        rewritten_chunks = self.context_repository.fetch(rewritten_question, k=self.RETRIEVAL_K)
        merged = self._merge_chunks(original_chunks, rewritten_chunks)
        reranked = self._rerank(question, merged)
        return reranked[: self.FINAL_K]

    def _merge_chunks(
        self, chunks: list[RetrievedDocument], extra: list[RetrievedDocument]
    ) -> list[RetrievedDocument]:
        merged = chunks[:]
        existing = [chunk.content for chunk in chunks]
        for chunk in extra:
            if chunk.content not in existing:
                merged.append(chunk)
        return merged

    @retry(wait=_wait)
    def _rewrite_query(self, question: str, history: list[dict]) -> str:
        """Rewrite the user's question into a specific, standalone query for the Knowledge Base."""
        prompt = self.REWRITE_QUERY_PROMPT_TEMPLATE.format(history=history, question=question)
        response = completion(
            model=self.chat_model, messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content

    @retry(wait=_wait)
    def _rerank(self, question: str, chunks: list[RetrievedDocument]) -> list[RetrievedDocument]:
        if not chunks:
            return chunks
        messages = [
            {"role": "system", "content": self.RERANK_SYSTEM_PROMPT},
            {"role": "user", "content": self._make_rerank_user_prompt(question, chunks)},
        ]
        response = completion(model=self.chat_model, messages=messages, response_format=RankOrder)
        order = RankOrder.model_validate_json(response.choices[0].message.content).order
        return [chunks[i - 1] for i in order]

    def _make_rerank_user_prompt(self, question: str, chunks: list[RetrievedDocument]) -> str:
        prompt = (
            f"The user has asked the following question:\n\n{question}\n\n"
            "Order all the chunks of text by relevance to the question, from most relevant to "
            "least relevant. Include all the chunk ids you are provided with, reranked.\n\n"
            "Here are the chunks:\n\n"
        )
        for index, chunk in enumerate(chunks):
            prompt += f"# CHUNK ID: {index + 1}:\n\n{chunk.content}\n\n"
        prompt += "Reply only with the list of ranked chunk ids, nothing else."
        return prompt

    @retry(wait=_wait)
    def answer_question(
        self, question: str, history: list[dict] | None = None
    ) -> tuple[str, list[RetrievedDocument]]:
        """
        Answer the given question with RAG; return the answer and the context documents.
        """
        history = history or []
        chunks = self.fetch_context(question, history)
        context = "\n\n".join(
            f"Extract from {chunk.metadata.get('source', 'unknown')}:\n{chunk.content}"
            for chunk in chunks
        )
        system_prompt = self.SYSTEM_PROMPT.format(context=context)
        messages = [
            {"role": "system", "content": system_prompt},
            *history,
            {"role": "user", "content": question},
        ]
        response = completion(model=self.chat_model, messages=messages)
        return response.choices[0].message.content, chunks
