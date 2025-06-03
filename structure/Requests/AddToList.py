from telegram.ext import ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters
from telegram import Update
from .Markups import MENU_MARKUP, CANCEL_MARKUP
import re


INPUT_SEARCH_STATE = 1
INPUT_COST_STATE = 2

NOT_COMMAND = filters.TEXT & ~filters.COMMAND

class AddToList(ConversationHandler):
    def __init__(self, core):
        self.core = core
        self.search_request = None
        self.cost = None
        super().__init__(
            entry_points=[CommandHandler('add', self.__start_handler)],
            states={
                INPUT_SEARCH_STATE: [MessageHandler(NOT_COMMAND, self.__search_handler)],
                INPUT_COST_STATE: [MessageHandler(NOT_COMMAND, self.__cost_handler)],
            },
            fallbacks=[CommandHandler('cancel', self.__cancel_handler)],
        )

    async def __start_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.core.init_chat(update.effective_chat.id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Введите поисковый запрос', reply_markup=CANCEL_MARKUP)
        return INPUT_SEARCH_STATE

    async def __search_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.search_request = update.message.text
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Введите цену (в руб.)')
        return INPUT_COST_STATE
    
    async def __cost_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text.replace(' ', '').replace(',', '.')
        if not re.fullmatch(r'((?<![\w.])[+]?(?:\d+\.\d+|\d+\.|\.\d+|\d+))', answer):
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Введите число (руб.)')
            return INPUT_COST_STATE
        self.core.add_sub(update.effective_chat.id, self.search_request, float(answer))
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Добавлено', reply_markup=MENU_MARKUP)
        return ConversationHandler.END
    
    async def __cancel_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Возврат в меню', reply_markup=MENU_MARKUP)
        return ConversationHandler.END