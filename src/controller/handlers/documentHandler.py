from src.controller.handlers.utils import keyboardBuilder
from aiogram.types import ParseMode


def documentMessageHandler(data, message, bot, api_public):
    keyboard = keyboardBuilder(data['markup'])
    document = api_public + data['document']
    return bot.send_document(
        chat_id=message.chat.id,
        document=document,
        caption=data['document_caption'],
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
