from __future__ import annotations

from typing import List, Dict

from .llm import get_llm
import logging
import json

from .tools import TOOLS, TOOL_SPECS
log = logging.getLogger("agent")

class Agent:
    def __init__(self):
        self.llm = get_llm()
        self.messages: List[Dict] = [
            {
                "role": "system",
                "content": (
                    "You are a senior developer assistant. "
                    "Explain things clearly and step-by-step."
                ),
            }
        ]

    def ask(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})

        # First LLM call (may request tool)
        resp = self.llm.client.chat.completions.create(
            model=self.llm.model,
            messages=self.messages,
            tools=TOOL_SPECS,
            tool_choice="auto",
            temperature=0.2,
        )
        msg = resp.choices[0].message
        self.messages.append(msg)

        # If no tool requested -> return answer
        if not msg.tool_calls:
            answer = msg.content or ""
            self.messages.append({"role": "assistant", "content": answer})
            return answer

        # Execute tools
        for tc in msg.tool_calls:
            name = tc.function.name
            args = json.loads(tc.function.arguments or "{}")
            log.info("Tool call: %s args=%s", name, args)
            fn = TOOLS.get(name)
            result = fn(**args) if fn else {"error": f"Unknown tool: {name}"}

            self.messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps(result, ensure_ascii=False),
                }
            )
        log.info("Tool result: %s", result)

        # Second LLM call after tool results
        resp2 = self.llm.client.chat.completions.create(
            model=self.llm.model,
            messages=self.messages,
            temperature=0.2,
        )
        msg2 = resp2.choices[0].message
        answer2 = msg2.content or ""
        self.messages.append({"role": "assistant", "content": answer2})
        return answer2


def get_agent() -> Agent:
    return Agent()