from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from .Markups import MENU_MARKUP
import logging


class ShowList(CommandHandler):
    def __init__(self, core):
        self.core = core
        super().__init__('mylist', self.__handler)

    async def __handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = '''
Ваш список поисковых запросов:\n''' + '\n'.join([f'{i+1}. {query} за {item['price']} руб. ({"Найдено" if item["founded"] else "Не найдено"})'
                                             for i, (query, item) in enumerate(self.core.get_subs(update.effective_chat.id).items())])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=MENU_MARKUP)
