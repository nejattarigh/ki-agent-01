from __future__ import annotations

from openai import OpenAI

from .config import get_settings


class LLMClient:
    def __init__(self):
        settings = get_settings()
        self.model = settings.openai_model
        self.client = OpenAI(api_key=settings.openai_api_key)

    def chat(self, messages):
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.2,
        )
        return resp.choices[0].message.content or ""


def get_llm() -> LLMClient:
    return LLMClient()