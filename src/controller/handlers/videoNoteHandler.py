from utils import keyboardBuilder
from aiogram.types import ParseMode, InputFile


async def videoNoteMessageHandler(data, message, bot, api_public):
    keyboard = keyboardBuilder(data['markup'])
    video_note = api_public + data['video_note']
    await bot.send_video_note(chat_id=message.chat.id,
                              video_note=InputFile.from_url(video_note,
                                                            data['video_note']))
    return await message.answer(text=data['video_note_caption'],
                                parse_mode=ParseMode.HTML,
                                reply_markup=keyboard)
