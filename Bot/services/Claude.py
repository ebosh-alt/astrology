import logging

import anthropic

from Bot.entity.NatalChart import ElementNatalChart
from Bot.services.GetMessage import get_mes

logger = logging.getLogger("__name__")


class Claude:
    def __init__(self) -> None:
        self.model = "claude-3-opus-20240229"
        self.client = anthropic.Anthropic()
        self.temperature = 0.5
        self.id = "fc7305ab-231a-4586-bab1-6a035fa16bc9"

    def get_answer(self, question, natal_chart):
        message = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            temperature=0.0,
            system=get_mes("service_claude"),
            messages=[
                {"role": "user", "content": get_mes("user_openai", question=question, natal_chart=natal_chart)}
            ]
        )
        return message.content[0].text
