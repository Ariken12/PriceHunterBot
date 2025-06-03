from .BaseAnswer.BaseAnswer import BaseAnswer


class NullAnswer(BaseAnswer):
    def __init__(self):
        pass

    def __call__(self, *args, **kwds):
        return None