import pytest
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_openai(monkeypatch):
    class DummyClient:
        def generate_text(self, *args, **kwargs):
            return None
    monkeypatch.setattr('scripts.openai.openai_utils.OpenAIClient', lambda: DummyClient())