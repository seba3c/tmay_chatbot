import math


class EvalMetricCalculatorService:
    """Evaluation metrics for retrieval performance."""

    def calculate_mrr(self, keyword: str, retrieved_docs: list) -> float:
        """Calculate reciprocal rank for a single keyword (case-insensitive)."""
        keyword_lower = keyword.lower()
        for rank, doc in enumerate(retrieved_docs, start=1):
            if keyword_lower in doc.content.lower():
                return 1.0 / rank
        return 0.0

    def calculate_dcg(self, relevances: list[int], k: int) -> float:
        """Calculate Discounted Cumulative Gain."""
        dcg = 0.0
        for i in range(min(k, len(relevances))):
            dcg += relevances[i] / math.log2(i + 2)  # i+2 because rank starts at 1
        return dcg

    def calculate_ndcg(self, keyword: str, retrieved_docs: list, k: int = 10) -> float:
        """Calculate nDCG for a single keyword (binary relevance, case-insensitive)."""
        keyword_lower = keyword.lower()

        # Binary relevance: 1 if keyword found, 0 otherwise
        relevances = [
            1 if keyword_lower in doc.content.lower() else 0 for doc in retrieved_docs[:k]
        ]

        # DCG
        dcg = self.calculate_dcg(relevances, k)

        # Ideal DCG (best case: keyword in first position)
        ideal_relevances = sorted(relevances, reverse=True)
        idcg = self.calculate_dcg(ideal_relevances, k)

        return dcg / idcg if idcg > 0 else 0.0
