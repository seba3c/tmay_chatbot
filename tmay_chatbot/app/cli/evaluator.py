import sys

from tmay_chatbot.app.base import CliApp
from tmay_chatbot.evaluation.eval import ChatbotEvaluator
from tmay_chatbot.evaluation.factory import get_chatbot_evaluator


class ChatbotEvaluatorCli(CliApp):
    def __init__(self, chatbot_evaluator: ChatbotEvaluator) -> None:
        self.chatbot_evaluator = chatbot_evaluator

    def run_hook(self, *args, **kwargs) -> None:
        if len(args) != 1:
            print("Usage: uv run python -m tmay_chatbot.app.cli.evaluator <test_row_number>")
            sys.exit(1)

        try:
            test_number = int(args[0])
        except ValueError:
            print("Error: test_row_number must be an integer")
            sys.exit(1)

        self.run_evaluation(test_number)

    def run_evaluation(self, test_number: int) -> None:
        tests = self.chatbot_evaluator.tests

        if test_number < 0 or test_number >= len(tests):
            print(f"Error: test_row_number must be between 0 and {len(tests) - 1}")
            sys.exit(1)

        test = tests[test_number]

        print(f"\n{'=' * 80}")
        print(f"Test #{test_number}")
        print(f"{'=' * 80}")
        print(f"Question: {test.question}")
        print(f"Keywords: {test.keywords}")
        print(f"Category: {test.category}")
        print(f"Reference Answer: {test.reference_answer}")

        print(f"\n{'=' * 80}")
        print("Retrieval Evaluation")
        print(f"{'=' * 80}")

        retrieval_result = self.chatbot_evaluator.evaluate_retrieval(test)

        print(f"MRR: {retrieval_result.mrr:.4f}")
        print(f"nDCG: {retrieval_result.ndcg:.4f}")
        print(
            f"Keywords Found: {retrieval_result.keywords_found}/{retrieval_result.total_keywords}"
        )
        print(f"Keyword Coverage: {retrieval_result.keyword_coverage:.1f}%")

        print(f"\n{'=' * 80}")
        print("Answer Evaluation")
        print(f"{'=' * 80}")

        answer_result, generated_answer, _retrieved_docs = self.chatbot_evaluator.evaluate_answer(
            test
        )

        print(f"\nGenerated Answer:\n{generated_answer}")
        print(f"\nFeedback:\n{answer_result.feedback}")
        print("\nScores:")
        print(f"  Accuracy: {answer_result.accuracy:.2f}/5")
        print(f"  Completeness: {answer_result.completeness:.2f}/5")
        print(f"  Relevance: {answer_result.relevance:.2f}/5")
        print(f"\n{'=' * 80}\n")


if __name__ == "__main__":
    ChatbotEvaluatorCli(chatbot_evaluator=get_chatbot_evaluator()).run(*sys.argv[1:])
