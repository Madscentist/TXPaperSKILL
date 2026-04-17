"""
Simple OpenAI-compatible LLM client for the PaperSkill factory.
Supports both local and remote endpoints via environment variables.
"""
import os
import json
from typing import List, Dict, Optional

try:
    import requests
except ImportError:
    requests = None


class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("PAPERSKILL_API_KEY", "")
        self.base_url = os.getenv("PAPERSKILL_BASE_URL", "http://localhost:18080/v1")
        self.model = os.getenv("PAPERSKILL_MODEL", "gemma4:31b-64k")
        self.timeout = int(os.getenv("PAPERSKILL_TIMEOUT", "120"))

    def chat(self, system: str, user: str, temperature: float = 0.3) -> str:
        """Call the LLM with a simple system+user message pair."""
        if requests is None:
            raise RuntimeError("The 'requests' library is required for LLM calls. Install it via pip.")

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            "temperature": temperature,
        }

        url = self.base_url.rstrip("/") + "/chat/completions"
        resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]


def llm_extract_phrases_and_logic(section: str, report_summary: str) -> Dict[str, List[str]]:
    """
    Use LLM to extract preferred_phrases and logic_pattern for a section
    based on the aggregation report summary.
    """
    client = LLMClient()
    system = (
        "You are an expert academic writing analyst. "
        "Given a section name and an aggregation report summary of an author's papers, "
        "generate complete sentence templates and logical patterns that represent this author's writing style for that section. "
        "Output ONLY a valid JSON object with two keys: "
        "'preferred_phrases' (list of 5-8 complete sentence templates or starter phrases, not single words) and "
        "'logic_pattern' (list of 1-3 strings describing the rhetorical flow). "
        "Do not include markdown formatting or explanations."
    )
    user = (
        f"Section: {section}\n\n"
        f"Report Summary:\n{report_summary}\n\n"
        "Generate the author's typical sentence templates (full phrases, not isolated words) and logical patterns for this section."
    )
    raw = client.chat(system, user, temperature=0.3)
    # Clean up possible markdown fences
    text = raw.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    return json.loads(text)
