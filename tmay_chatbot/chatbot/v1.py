from langchain_core.messages import HumanMessage, SystemMessage, convert_to_messages
from langchain_openai import ChatOpenAI

from tmay_chatbot.chatbot.base import TmayChatbot
from tmay_chatbot.core.context_repository.repository import ContextRepository
from tmay_chatbot.core.knowledge_base import RetrievedDocument


class TmayChatBotV1(TmayChatbot):
    RETRIEVAL_K = 10

    def __init__(self, chat_model: str, context_repository: ContextRepository):
        super().__init__(context_repository)
        self.llm = ChatOpenAI(temperature=0, model=chat_model)

    def fetch_context(self, question: str) -> list[RetrievedDocument]:
        """
        Retrieve relevant context documents for a question.
        """
        return self.context_repository.fetch(question, k=self.RETRIEVAL_K)

    def combined_question(self, question: str, history: list[dict] | None = None) -> str:
        """
        Combine all the user's messages into a single string.
        """
        if history is None:
            history = []
        prior = "\n".join(m["content"] for m in history if m["role"] == "user")
        return prior + "\n" + question

    def answer_question(
        self, question: str, history: list[dict] | None = None
    ) -> tuple[str, list[RetrievedDocument]]:
        """
        Answer the given question with RAG; return the answer and the context documents.
        """
        history = history or []
        combined = self.combined_question(question, history)
        docs = self.fetch_context(combined)
        context = "\n\n".join(doc.content for doc in docs)
        system_prompt = self.SYSTEM_PROMPT.format(context=context)
        messages = [SystemMessage(content=system_prompt)]
        messages.extend(convert_to_messages(history))
        messages.append(HumanMessage(content=question))
        response = self.llm.invoke(messages)
        return response.content, docs
