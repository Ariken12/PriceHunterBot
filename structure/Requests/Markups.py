from telegram import ReplyKeyboardMarkup

MENU_MARKUP = ReplyKeyboardMarkup(
    [['/add', '/remove', '/mylist']],
    resize_keyboard=True)

CANCEL_MARKUP = ReplyKeyboardMarkup(
    [['/cancel']],
    resize_keyboard=True)

REMOVE_MARKUP = ReplyKeyboardMarkup(
    [['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], ['/cancel']],
    resize_keyboard=True
)