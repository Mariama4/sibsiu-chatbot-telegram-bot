from aiogram.types import ParseMode, InputFile
from src.controller.handlers.utils import keyboardBuilder


# ПЕРЕПРОВЕРИТЬ
async def videoMessageHandler(data, message, bot, api_public):
    keyboard = keyboardBuilder(data['markup'])
    video = InputFile.from_url(api_public + data['video'])
    return await bot.send_video(
        chat_id=message.chat.id,
        video=video,
        caption=data['video_caption'],
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
