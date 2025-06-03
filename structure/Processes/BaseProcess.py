from abc import ABC, abstractmethod


class BaseProcess(ABC):
    def __init__(self, name, interval, start_delay, core=None):
        self.interval = interval
        self.start_delay = start_delay
        self.__name__ = name
        self.core = core

    @abstractmethod
    def __call__(self, update, context):
        pass