from aiogram.types import ParseMode
from src.controller.handlers.utils import keyboardBuilder


async def textMessageHandler(data, message):
    keyboard = keyboardBuilder(data['markup'])
    return await message.answer(text=data['text'],
                                parse_mode=ParseMode.HTML,
                                reply_markup=keyboard)
