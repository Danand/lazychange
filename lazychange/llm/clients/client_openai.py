import os

import click

from typing import cast

from openai import OpenAI

from ..client_base import ClientBase

class ClientOpenAI(ClientBase):
    client: OpenAI

    def __init__(
        self,
        api_key: str | None,
        model: str,
    ) -> None:
        api_key = api_key \
            or os.getenv("OPENAI_API_KEY") \
            or os.getenv("OPENAI_TOKEN")

        if not api_key:
            raise click.ClickException(
                "OpenAI API key must be provided through " \
                "`--api-key`, " \
                "`OPENAI_API_KEY` or " \
                "`OPENAI_TOKEN`."
            )

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def get_simple_answer(
        self,
        content: str,
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": content,
                },
            ],
        )

        answer = cast(str, response.choices[0].message.content)

        return answer.strip()
