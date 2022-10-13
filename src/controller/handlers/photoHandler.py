from aiogram.types import ParseMode, InputFile
from src.controller.handlers.utils import keyboardBuilder


async def photoMessageHandler(data, message, bot, api_public):
    keyboard = keyboardBuilder(data['markup'])
    photo = InputFile.from_url(api_public + data['photo'])
    return await bot.send_photo(
        chat_id=message.chat.id,
        caption=data['photo_caption'],
        parse_mode=ParseMode.HTML,
        photo=photo,
        reply_markup=keyboard
    )
