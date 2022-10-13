from aiogram.types import ParseMode
from src.controller.handlers.utils import keyboardBuilder


async def locationMessageHandler(data, message, bot):
    keyboard = keyboardBuilder(data['markup'])
    await bot.send_location(
        chat_id=message.chat.id,
        latitude=data['location_latitude'],
        longitude=data['location_longitude'],
        horizontal_accuracy=data['location_horizontal_accuracy']
    )
    return await message.answer(text=data['location_caption'],
                                parse_mode=ParseMode.HTML,
                                reply_markup=keyboard)
