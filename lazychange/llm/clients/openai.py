import os

import click

from typing import cast

from openai import OpenAI

def get_llm_client(api_key: str | None) -> OpenAI:
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

    return OpenAI(api_key=api_key)

def get_simple_answer(
    openai_client: OpenAI,
    content: str,
    model: str,
) -> str:
    response = openai_client.chat.completions.create(
        model=model,
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
