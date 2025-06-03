from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from .Markups import MENU_MARKUP
import logging


class StartCommand(CommandHandler):
    def __init__(self, core):
        self.core = core
        super().__init__('start', self.__handler)

    async def __handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = '''
*Привет*, я бот для уведомлений о продажах Wildberries! Добавь поисковые запросы и я сообщу, когда встречу предложения тебе по карману.
*Команды*:
/start - вывести меню
/add - добавить/изменить поисковый запрос
/remove - удалить поисковый запрос
/mylist - список поисковых запросов
'''
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=MENU_MARKUP, parse_mode='Markdown')
