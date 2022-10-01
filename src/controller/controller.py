from aiogram.types import ReplyKeyboardMarkup, InputFile
from aiogram import types


async def frameQualifier(frame, message, state):
    async with state.proxy() as data:
        previousFrame = frame.frames.get(data.state)
        for index, value in enumerate(previousFrame['BUTTONS']):
            if value['TEXT'] == message.text:
                return value['REDIRECT_ON_ID_FRAME']


def messageController(database, data, message, state, bot):
    # Определение типа сообщения
    match data['MESSAGE']['TYPE']:
        case "TEXT":
            return textMessageController(database, data, message)
        case "PHOTO":
            return photoMessageController(database, data, message, bot)
        case "MEDIA_GROUP":
            return mediaGroupMessageController(data, message, bot)
        case "VIDEO_NOTE":
            return videoNoteMessageController(data, message, bot)
        case "VENUE":
            return 0
        case _:
            # not found
            pass


def textMessageController(database, data, message):
    keyboard = keyboardController(data['BUTTONS'])
    return message.answer(text=data['MESSAGE']['TEXT'],
                          reply_markup=keyboard)


def photoMessageController(database, data, message, bot):
    keyboard = keyboardController(data['BUTTONS'])
    return bot.send_photo(
        chat_id=message.chat.id,
        caption=data['MESSAGE']['CAPTION'],
        photo=data['MESSAGE']['PHOTO_URL'],
        reply_markup=keyboard
    )


async def mediaGroupMessageController(data, message, bot):
    keyboard = keyboardController(data['BUTTONS'])
    mediaGroup = mediaGroupController(data['MESSAGE']['MEDIA'])
    await bot.send_media_group(chat_id=message.chat.id,
                               media=mediaGroup)
    return await message.answer(text=data['MESSAGE']['CAPTION'],
                                reply_markup=keyboard)


async def videoNoteMessageController(data, message, bot):
    keyboard = keyboardController(data['BUTTONS'])
    await bot.send_video_note(chat_id=message.chat.id,
                              video_note=InputFile.from_url(data['MESSAGE']['VIDEO_NOTE_URL'],
                                                            data['MESSAGE']['VIDEO_NOTE_URL']))
    return await message.answer(text=data['MESSAGE']['CAPTION'],
                                reply_markup=keyboard)


def mediaGroupController(media):
    mediaGroup = types.MediaGroup()
    for index, value in enumerate(media):
        mediaGroup.attach_photo(value['URL'])

    return mediaGroup


def keyboardController(buttons):
    REPLY_KEYBOARD = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=False
    )
    list(
        map(
            lambda x:
            REPLY_KEYBOARD.add(x['TEXT']),
            buttons
        )
    )
    return REPLY_KEYBOARD
