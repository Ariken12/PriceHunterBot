from abc import ABC, abstractmethod


class BaseAction(ABC):
    def __init__(self):
        super().__init__()
        self.answer = None

    def __call__(self, context):
        return self.answer(context)