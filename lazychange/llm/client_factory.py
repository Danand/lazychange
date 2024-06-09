from .client_base import ClientBase
from .clients.client_openai import ClientOpenAI
from .clients.client_test import ClientTest

def get_llm_client(
    llm: str,
    api_key: str | None,
) -> ClientBase:
    if llm == "test":
        return ClientTest()
    elif llm == "openai":
        client_openai = ClientOpenAI()

        client_openai.initialize(api_key)

        return client_openai
    else:
        raise ValueError("Invalid LLM")
