import openai
import json
import logging
from service.config import OPENAI_API_KEY

# — Configure a simple logger —
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load your API key
openai.api_key = OPENAI_API_KEY

def extract_fields(markdown: str, fields: list[str]) -> dict:
    """
    Send a Markdown document to GPT‑4 and extract only the requested fields as JSON.
    Logs the raw LLM output for debugging.
    """
    prompt = f"""
You are an expert data extractor.  Return **ONLY** a single JSON object with these keys: {fields}.
Do **not** include any additional text, explanation, or markdown fences—just the JSON.

```markdown
{markdown}
```"""

    # Call the new v1 OpenAI Python interface
    resp = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )

    raw = resp.choices[0].message.content.strip()
    logger.info("Raw LLM output:\n%s", raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        logger.error("Failed to parse JSON from LLM output")
        raise ValueError(
            f"LLM did not return valid JSON.\nError: {e}\nRaw output:\n{raw}"
        )
