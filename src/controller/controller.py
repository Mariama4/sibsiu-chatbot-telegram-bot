from aiogram.types import ReplyKeyboardMarkup, InputFile, ParseMode, InputMedia
from aiogram import types


async def frameQualifier(frame, message, state):
    async with state.proxy() as data:
        previousFrame = frame.frames.get(data.state)
        for index, value in enumerate(previousFrame['BUTTONS']):
            if value['TEXT'] == message.text:
                return value['REDIRECT_ON_ID_FRAME']


def messageController(database, data, message, state, bot, configuration):
    # Определение типа сообщения
    match data['MESSAGE']['TYPE']:
        case "TEXT":
            return textMessageController(data, message, bot, configuration)
        case "PHOTO":
            return photoMessageController(data, message, bot, configuration)
        case "MEDIA_GROUP":
            return mediaGroupMessageController(data, message, bot, configuration)
        case "VIDEO_NOTE":
            return videoNoteMessageController(data, message, bot, configuration)
        case "VENUE":
            return venueMessageController(data, message, bot, configuration)
        case "CONTACT":
            return contactMessageController(data, message, bot, configuration)
        case _:
            # not found
            pass


def textMessageController(data, message, bot, configuration):
    keyboard = keyboardController(data['BUTTONS'])
    return message.answer(text=data['MESSAGE']['TEXT'],
                          parse_mode=ParseMode.HTML,
                          reply_markup=keyboard)


def photoMessageController(data, message, bot, configuration):
    keyboard = keyboardController(data['BUTTONS'])
    photo = configuration.getPublicUrl() + data['MESSAGE']['PHOTO']
    return bot.send_photo(
        chat_id=message.chat.id,
        caption=data['MESSAGE']['PHOTO_CAPTION'],
        parse_mode=ParseMode.HTML,
        photo=photo,
        reply_markup=keyboard
    )


async def mediaGroupMessageController(data, message, bot, configuration):
    keyboard = keyboardController(data['BUTTONS'])
    mediaGroup = mediaGroupController(data['MESSAGE']['MEDIA_GROUP'], configuration)
    await bot.send_media_group(chat_id=message.chat.id,
                               media=mediaGroup)
    return await message.answer(text=data['MESSAGE']['MEDIA_CAPTION'],
                                parse_mode=ParseMode.HTML,
                                reply_markup=keyboard)


async def videoNoteMessageController(data, message, bot, configuration):
    keyboard = keyboardController(data['BUTTONS'])
    video_note = configuration.getPublicUrl() + data['MESSAGE']['VIDEO_NOTE']
    await bot.send_video_note(chat_id=message.chat.id,
                              video_note=InputFile.from_url(video_note,
                                                            data['MESSAGE']['VIDEO_NOTE']))
    return await message.answer(text=data['MESSAGE']['VIDEO_NOTE_CAPTION'],
                                parse_mode=ParseMode.HTML,
                                reply_markup=keyboard)


async def venueMessageController(data, message, bot, configuration):
    keyboard = keyboardController(data['BUTTONS'])
    await bot.send_venue(
        chat_id=message.chat.id,
        latitude=data['MESSAGE']['VENUE_LATITUDE'],
        longitude=data['MESSAGE']['VENUE_LONGITUDE'],
        title=data['MESSAGE']['VENUE_TITLE'],
        address=data['MESSAGE']['VENUE_ADDRESS'],
        # reply_markup=keyboard
    )
    return await message.answer(
        text=data['MESSAGE']['VENUE_CAPTION'],
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )


async def contactMessageController(data, message, bot, configuration):
    keyboard = keyboardController(data['BUTTONS'])
    await bot.send_contact(
        chat_id=message.chat.id,
        phone_number=data['MESSAGE']['CONTACT_PHONE_NUMBER'],
        first_name=data['MESSAGE']['CONTACT_FIRST_NAME'],
        last_name=data['MESSAGE']['CONTACT_LAST_NAME']
    )
    return await message.answer(
        text=data['MESSAGE']['CONTACT_CAPTION'],
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )


def mediaGroupController(media, configuration):
    mediaGroup = types.MediaGroup()
    publicUrl = configuration.getPublicUrl()
    for index, value in enumerate(media):
        mediaGroup.attach_photo(publicUrl+value)

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
