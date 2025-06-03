from abc import ABC, abstractmethod


class BaseAnswer(ABC):
    @abstractmethod
    def __call__(self, context):
        return context