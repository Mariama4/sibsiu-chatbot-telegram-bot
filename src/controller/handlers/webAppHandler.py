from aiogram.types import ParseMode, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from src.controller.handlers.utils import keyboardBuilder


async def webAppHandler(data, message):
    keyboard = keyboardBuilder(data['markup'])
    keyboard.add(
        InlineKeyboardButton(
            text=data['web_app_button_text'],
            web_app=WebAppInfo(
                url=data['web_app']
            )
        )
    )
    return await message.answer(
        text=data['web_app_caption'],
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
