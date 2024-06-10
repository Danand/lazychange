import os

from typing import cast

from ..client_base  import ClientBase

from pydantic.v1.types import SecretStr

from langchain_core.language_models.base import BaseLanguageModel
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

class ClientLangchain(ClientBase):
    def __init__(
        self,
        llm: str,
        api_key: str | None,
        model: str,
    ) -> None:
        self.client = self.resolve_client(
            llm=llm,
            api_key=api_key,
            model=model,
        )

    def resolve_client(
        self,
        llm: str,
        api_key: str | None,
        model: str,
    ) -> BaseLanguageModel[Any]:
        if llm == "openai":
            api_key = api_key \
                or os.getenv("OPENAI_API_KEY") \
                or os.getenv("OPENAI_TOKEN")

            if api_key is None:
                raise ValueError("Please provide a valid API key")

            return ChatOpenAI(
                api_key=SecretStr(api_key),
                model=model,
            )
        else:
            raise ValueError("Invalid LLM")

    def get_simple_answer(
        self,
        prompt: str,
    ) -> str:
        llm_chain = PromptTemplate.from_template("{prompt}") | self.client

        response = llm_chain.invoke({"prompt": prompt})

        answer = cast(str, response.content)

        return answer
