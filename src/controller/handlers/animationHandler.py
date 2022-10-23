from aiogram.types import ParseMode, InputFile
from src.controller.handlers.utils import keyboardBuilder


async def animationMessageHandler(data, message, bot, api_public):
    keyboard = keyboardBuilder(data['markup'])
    animation = InputFile.from_url(api_public + data['animation'])
    return await bot.send_animation(
        chat_id=message.chat.id,
        animation=animation,
        caption=data['animation_caption'],
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
