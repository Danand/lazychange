class ClientBase:
    def initialize(self, api_key: str | None) -> None:
     raise NotImplementedError()

    def get_simple_answer(
        self,
        content: str,
        model: str,
    ) -> str:
        raise NotImplementedError()
