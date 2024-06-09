from ..client_base import ClientBase

from collections import deque
from typing import Deque

class ClientTest(ClientBase):
    _answer_queue: Deque[str] = deque()

    @staticmethod
    def enqueue_answer(answer: str) -> None:
        ClientTest._answer_queue.append(answer)

    def initialize(self, api_key: str | None) -> None:
        pass

    def get_simple_answer(
        self,
        content: str,
        model: str,
    ) -> str:
        if ClientTest._answer_queue:
            return ClientTest._answer_queue.popleft()
        else:
            raise ValueError("No test answers enqueued")
