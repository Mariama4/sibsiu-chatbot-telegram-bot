from src.controller.handlers.utils import keyboardBuilder
from aiogram.types import ParseMode


async def audioMessageHandler(data, message, bot, api_public):
    keyboard = keyboardBuilder(data['markup'])
    audio = api_public + data['audio']
    return bot.send_audio(
        chat_id=message.chat.id,
        audio=audio,
        caption=data['audio_caption'],
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )