from pathlib import Path

from litellm import completion

from tmay_chatbot.chatbot.base import TmayChatbot
from tmay_chatbot.evaluation.models import AnswerEval, RetrievalEval, TestQuestion
from tmay_chatbot.evaluation.service import EvalMetricCalculatorService
from tmay_chatbot.evaluation.test import TestLoader


class ChatbotEvaluator:
    def __init__(self, chatbot: TmayChatbot, eval_model: str, tests_path: Path) -> None:
        self.eval_metric_evaluator = EvalMetricCalculatorService()
        self.chatbot = chatbot
        self.eval_model = eval_model
        self.tests = TestLoader().load_tests(tests_path)

    def evaluate_retrieval(self, test: TestQuestion, k: int = 10) -> RetrievalEval:
        """
        Evaluate retrieval performance for a test question.

        Args:
            test: TestQuestion object containing question and keywords
            k: Number of top documents to retrieve (default 10)

        Returns:
            RetrievalEval object with MRR, nDCG, and keyword coverage metrics
        """
        # Retrieve documents using shared answer module
        retrieved_docs = self.chatbot.fetch_context(test.question)

        # Calculate MRR (average across all keywords)
        mrr_scores = [
            self.eval_metric_evaluator.calculate_mrr(keyword, retrieved_docs)
            for keyword in test.keywords
        ]
        avg_mrr = sum(mrr_scores) / len(mrr_scores) if mrr_scores else 0.0

        # Calculate nDCG (average across all keywords)
        ndcg_scores = [
            self.eval_metric_evaluator.calculate_ndcg(keyword, retrieved_docs, k)
            for keyword in test.keywords
        ]
        avg_ndcg = sum(ndcg_scores) / len(ndcg_scores) if ndcg_scores else 0.0

        # Calculate keyword coverage
        keywords_found = sum(1 for score in mrr_scores if score > 0)
        total_keywords = len(test.keywords)
        keyword_coverage = (keywords_found / total_keywords * 100) if total_keywords > 0 else 0.0

        return RetrievalEval(
            mrr=avg_mrr,
            ndcg=avg_ndcg,
            keywords_found=keywords_found,
            total_keywords=total_keywords,
            keyword_coverage=keyword_coverage,
        )

    def _get_judge_prompt(self, test: TestQuestion, generated_answer: str):
        return [
            {
                "role": "system",
                "content": "You are an expert evaluator assessing the quality of answers. Evaluate the generated answer by comparing it to the reference answer. Only give 5/5 scores for perfect answers.",
            },
            {
                "role": "user",
                "content": f"""Question:
    {test.question}
    
    Generated Answer:
    {generated_answer}
    
    Reference Answer:
    {test.reference_answer}
    
    Please evaluate the generated answer on three dimensions:
    1. Accuracy: How factually correct is it compared to the reference answer? Only give 5/5 scores for perfect answers.
    2. Completeness: How thoroughly does it address all aspects of the question, covering all the information from the reference answer?
    3. Relevance: How well does it directly answer the specific question asked, giving no additional information?
    
    Provide detailed feedback and scores from 1 (very poor) to 5 (ideal) for each dimension. If the answer is wrong, then the accuracy score must be 1.""",
            },
        ]

    def evaluate_answer(self, test: TestQuestion) -> tuple[AnswerEval, str, list]:
        """
        Evaluate answer quality using LLM-as-a-judge (async).

        Args:
            test: TestQuestion object containing question and reference answer

        Returns:
            Tuple of (AnswerEval object, generated_answer string, retrieved_docs list)
        """
        # Get RAG response using shared answer module
        generated_answer, retrieved_docs = self.chatbot.answer_question(test.question)

        # LLM judge prompt
        judge_messages = self._get_judge_prompt(test, generated_answer)

        # Call LLM judge with structured outputs (async)
        judge_response = completion(
            model=self.eval_model, messages=judge_messages, response_format=AnswerEval
        )

        answer_eval = AnswerEval.model_validate_json(judge_response.choices[0].message.content)

        return answer_eval, generated_answer, retrieved_docs

    def evaluate_all_retrieval(self):
        """Evaluate all retrieval tests."""
        tests = self.tests
        total_tests = len(tests)
        for index, test in enumerate(tests):
            result = self.evaluate_retrieval(test)
            progress = (index + 1) / total_tests
            yield test, result, progress

    def evaluate_all_answers(self):
        """Evaluate all answers to tests using batched async execution."""
        tests = self.tests
        total_tests = len(tests)
        for index, test in enumerate(tests):
            result = self.evaluate_answer(test)[0]
            progress = (index + 1) / total_tests
            yield test, result, progress
