from .BaseAction.BaseAction import BaseAction
from ..Answers import NullAnswer


class NullAction(BaseAction):
    def __init__(self):
        self.answer = NullAnswer


