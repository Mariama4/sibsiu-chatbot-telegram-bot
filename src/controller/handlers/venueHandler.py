from utils import keyboardBuilder
from aiogram.types import ParseMode


async def venueMessageHandler(data, message, bot):
    keyboard = keyboardBuilder(data['markup'])
    await bot.send_venue(
        chat_id=message.chat.id,
        latitude=data['venue_latitude'],
        longitude=data['venue_longitude'],
        title=data['venue_title'],
        address=data['venue_address'],
    )
    return await message.answer(
        text=data['venue_caption'],
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )