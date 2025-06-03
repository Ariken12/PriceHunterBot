from telegram.ext import MessageHandler, ContextTypes
from telegram import Update
from ..Actions.NullAction import NullAction

class NullRequest(MessageHandler):
    def __init__(self, core):
        super().__init__(None, self.__handler)


    async def __handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass
