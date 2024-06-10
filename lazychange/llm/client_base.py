class ClientBase:
    def get_simple_answer(
        self,
        prompt: str,
    ) -> str:
        raise NotImplementedError()
