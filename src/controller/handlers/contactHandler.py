from src.controller.handlers.utils import keyboardBuilder
from aiogram.types import ParseMode


async def contactMessageHandler(data, message, bot):
    keyboard = keyboardBuilder(data['markup'])
    await bot.send_contact(
        chat_id=message.chat.id,
        phone_number=data['contact_phone_number'],
        first_name=data['contact_first_name'],
        last_name=data['contact_last_name']
    )
    return await message.answer(
        text=data['contact_caption'],
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )