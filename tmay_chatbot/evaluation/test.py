import json
from pathlib import Path

from tmay_chatbot.evaluation.models import TestQuestion

TEST_FILE = str(Path(__file__).parent / "tests.jsonl")


class TestLoader:
    def load_tests(self, jsonl_path) -> list[TestQuestion]:
        """Load test questions from JSONL file."""
        tests = []
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line.strip())
                tests.append(TestQuestion(**data))
        return tests
