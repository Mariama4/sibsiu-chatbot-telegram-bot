from aiogram.types import ParseMode, InputFile
from src.controller.handlers.utils import keyboardBuilder


async def documentMessageHandler(data, message, bot, api_public):
    keyboard = keyboardBuilder(data['markup'])
    document = InputFile.from_url(api_public + data['document'])
    return await bot.send_document(
        chat_id=message.chat.id,
        document=document,
        caption=data['document_caption'],
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
