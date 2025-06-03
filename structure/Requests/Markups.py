from telegram import ReplyKeyboardMarkup

MENU_MARKUP = ReplyKeyboardMarkup(
    [['/add', '/remove', '/mylist']],
    resize_keyboard=True)

CANCEL_MARKUP = ReplyKeyboardMarkup(
    [['/cancel']],
    resize_keyboard=True)