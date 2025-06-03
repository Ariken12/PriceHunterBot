from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from .Markups import MENU_MARKUP
import logging


class ShowList(CommandHandler):
    def __init__(self, core):
        self.core = core
        super().__init__('mylist', self.__handler)

    async def __handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id not in self.core.all_subs:
            self.core.all_subs[update.effective_chat.id] = {}
        message = '''
Ваш список поисковых запросов:\n''' + '\n'.join([f'{i+1}. {query} за {self.core.all_subs[update.effective_chat.id][query]} руб.' 
                                             for i, query in enumerate(self.core.all_subs[update.effective_chat.id])])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=MENU_MARKUP)
