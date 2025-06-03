from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, InlineQueryHandler


class DebugRequest(InlineQueryHandler):
    def __init__(self, core):
        self.core = core
        super().__init__(None, self.__handler)

    async def __handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        debug_message = f'Request: {update.effective_message.to_json()}\n'
        debug_message += f'ChatId: {update.effective_chat.id}\n'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=debug_message)
