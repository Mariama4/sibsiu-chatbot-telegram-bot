from utils import keyboardBuilder, mediaGroupBuilder
from aiogram.types import ParseMode


# добавить определение типа для правильной вставки медиа
async def mediaGroupMessageHandler(data, message, bot, api_public):
    keyboard = keyboardBuilder(data['markup'])
    mediaGroup = mediaGroupBuilder(data['media_group'], api_public)
    await bot.send_media_group(chat_id=message.chat.id,
                               media=mediaGroup)
    return await message.answer(text=data['media_group_caption'],
                                parse_mode=ParseMode.HTML,
                                reply_markup=keyboard)
