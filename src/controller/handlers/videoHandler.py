from aiogram.types import ParseMode
from src.controller.handlers.utils import keyboardBuilder


# ПЕРЕПРОВЕРИТЬ
async def videoMessageHandler(data, message, bot, api_public):
    keyboard = keyboardBuilder(data['markup'])
    video = api_public + data['video']
    return bot.send_video(
        chat_id=message.chat.id,
        video=video,
        caption=data['video_caption'],
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )