import os

import click

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
