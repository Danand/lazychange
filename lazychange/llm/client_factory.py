from .client_base import ClientBase
from .clients.client_openai import ClientOpenAI
from .clients.client_test import ClientTest

def get_llm_client(
    llm: str,
    model: str,
    api_key: str | None,
) -> ClientBase:
    if llm == "test":
        return ClientTest()
    elif llm == "openai":
        return ClientOpenAI(api_key, model)
    else:
        raise ValueError("Invalid LLM")
