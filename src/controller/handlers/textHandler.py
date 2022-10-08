from aiogram.types import ParseMode
from utils import keyboardBuilder


def textMessageHandler(data, message):
    keyboard = keyboardBuilder(data['markup'])
    return message.answer(text=data['text'],
                          parse_mode=ParseMode.HTML,
                          reply_markup=keyboard)
