from .client_base import ClientBase
from .clients.client_langchain import ClientLangchain
from .clients.client_test import ClientTest

def get_llm_client(
    llm: str,
    model: str,
    api_key: str | None,
) -> ClientBase:
    if llm == "test":
        return ClientTest()
    else:
        return ClientLangchain(
            llm=llm,
            api_key=api_key,
            model=model,
        )
