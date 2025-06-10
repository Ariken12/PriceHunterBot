from telegram.ext import ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters
from telegram import Update
from .Markups import MENU_MARKUP, REMOVE_MARKUP
import re


INPUT_REMOVE_STATE = 1
NOT_COMMAND = filters.TEXT & ~filters.COMMAND


class RemoveFromList(ConversationHandler):
    def __init__(self, core):
        self.core = core
        self.requests = []
        super().__init__(
            entry_points=[CommandHandler('remove', self.__start_handler)],
            states={
                INPUT_REMOVE_STATE: [MessageHandler(NOT_COMMAND, self.__request_handler)]
            },
            fallbacks=[CommandHandler('cancel', self.__cancel_handler)],
        )

    async def __start_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.core.init_chat(update.effective_chat.id)
        self.requests = list(self.core.get_subs(update.effective_chat.id).keys())
        message = '''
Список поисковых запросов:\n''' + '\n'.join(
    [f'{i+1}. {query}' 
     for i, query in enumerate(self.core.get_subs(update.effective_chat.id))]) + '''
Введите номер поискового запроса, который вы хотите удалить. (Разделение по запятым)'''
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=REMOVE_MARKUP)
        return INPUT_REMOVE_STATE

    async def __request_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text.replace(' ', '')
        if not re.fullmatch(r'((\d+)\,?)+', answer):
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Введите номера поискового запроса через запятую')
            return INPUT_REMOVE_STATE
        answer = answer.split(',')
        errors = []
        for number in answer:
            if int(number)-1 >= len(self.core.get_subs(update.effective_chat.id)):
                errors.append(number)
                continue
            self.core.remove_sub(update.effective_chat.id, self.requests[int(number)-1])
        if len(errors) > 0:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Номер(а) {", ".join(errors)} не существует')
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Удалено', reply_markup=MENU_MARKUP)
        return ConversationHandler.END
    
    async def __cancel_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Возврат в меню', reply_markup=MENU_MARKUP)
        return ConversationHandler.END