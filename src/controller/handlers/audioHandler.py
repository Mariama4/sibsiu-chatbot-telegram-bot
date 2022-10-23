from aiogram.types import ParseMode, InputFile
from src.controller.handlers.utils import keyboardBuilder


async def audioMessageHandler(data, message, bot, api_public):
    keyboard = keyboardBuilder(data['markup'])
    audio = InputFile.from_url(api_public + data['audio'])
    return await bot.send_audio(
        chat_id=message.chat.id,
        audio=audio,
        caption=data['audio_caption'],
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
