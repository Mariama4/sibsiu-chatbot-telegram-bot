from aiogram.types import ParseMode, InputFile
from src.controller.handlers.utils import keyboardBuilder


async def voiceMessageHandler(data, message, bot, api_public):
    keyboard = keyboardBuilder(data['markup'])
    voice = InputFile.from_url(api_public + data['voice'])
    return await bot.send_voice(
        chat_id=message.chat.id,
        voice=voice,
        caption=data['voice_caption'],
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
