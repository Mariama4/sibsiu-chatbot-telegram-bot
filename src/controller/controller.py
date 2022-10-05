from aiogram.types import ReplyKeyboardMarkup, InputFile, ParseMode, InlineKeyboardButton
from aiogram import types
from aiogram.types.web_app_info import WebAppInfo
import os
from dotenv import load_dotenv

load_dotenv()

API_PUBLIC = os.getenv('API_PUBLIC')


async def frameQualifier(frame, message, state):
    async with state.proxy() as data:
        previousFrame = frame.frames.get(data.state)
        for index, value in enumerate(previousFrame['BUTTONS']):
            if value['TEXT'] == message.text:
                return value['REDIRECT_ON_ID_FRAME']


def messageController(data, message, bot):
    # Определение типа сообщения
    match data['MESSAGE']['TYPE']:
        case "TEXT":
            return textMessageController(data, message)
        case "PHOTO":
            return photoMessageController(data, message, bot)
        case "MEDIA_GROUP":
            return mediaGroupMessageController(data, message, bot)
        case "VIDEO_NOTE":
            return videoNoteMessageController(data, message, bot)
        case "VENUE":
            return venueMessageController(data, message, bot)
        case "CONTACT":
            return contactMessageController(data, message, bot)
        case "WEB_APP":
            return webAppController(data, message)
        case _:
            # not found
            pass


def textMessageController(data, message):
    keyboard = keyboardController(data['BUTTONS'])
    return message.answer(text=data['MESSAGE']['TEXT'],
                          parse_mode=ParseMode.HTML,
                          reply_markup=keyboard)


def photoMessageController(data, message, bot):
    keyboard = keyboardController(data['BUTTONS'])
    photo = InputFile.from_url(API_PUBLIC + data['MESSAGE']['PHOTO'])
    return bot.send_photo(
        chat_id=message.chat.id,
        caption=data['MESSAGE']['PHOTO_CAPTION'],
        parse_mode=ParseMode.HTML,
        photo=photo,
        reply_markup=keyboard
    )


async def mediaGroupMessageController(data, message, bot):
    keyboard = keyboardController(data['BUTTONS'])
    mediaGroup = mediaGroupController(data['MESSAGE']['MEDIA_GROUP'])
    await bot.send_media_group(chat_id=message.chat.id,
                               media=mediaGroup)
    return await message.answer(text=data['MESSAGE']['MEDIA_CAPTION'],
                                parse_mode=ParseMode.HTML,
                                reply_markup=keyboard)


async def videoNoteMessageController(data, message, bot):
    keyboard = keyboardController(data['BUTTONS'])
    video_note = API_PUBLIC + data['MESSAGE']['VIDEO_NOTE']
    await bot.send_video_note(chat_id=message.chat.id,
                              video_note=InputFile.from_url(video_note,
                                                            data['MESSAGE']['VIDEO_NOTE']))
    return await message.answer(text=data['MESSAGE']['VIDEO_NOTE_CAPTION'],
                                parse_mode=ParseMode.HTML,
                                reply_markup=keyboard)


async def venueMessageController(data, message, bot):
    keyboard = keyboardController(data['BUTTONS'])
    await bot.send_venue(
        chat_id=message.chat.id,
        latitude=data['MESSAGE']['VENUE_LATITUDE'],
        longitude=data['MESSAGE']['VENUE_LONGITUDE'],
        title=data['MESSAGE']['VENUE_TITLE'],
        address=data['MESSAGE']['VENUE_ADDRESS'],
    )
    return await message.answer(
        text=data['MESSAGE']['VENUE_CAPTION'],
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )


async def contactMessageController(data, message, bot):
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


def webAppController(data, message):
    keyboard = keyboardController(data['BUTTONS'])
    keyboard.add(
        InlineKeyboardButton(
            text=data['MESSAGE']['WEB_APP_CAPTION'],
            web_app=WebAppInfo(
                url=data['MESSAGE']['WEB_APP']
            )
        )
    )
    return message.answer(
        text=data['MESSAGE']['WEB_APP_TEXT'],
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )


def mediaGroupController(media):
    mediaGroup = types.MediaGroup()
    for index, value in enumerate(media):
        mediaGroup.attach_photo(
            InputFile.from_url(API_PUBLIC+value)
        )

    return mediaGroup


def keyboardController(buttons):
    REPLY_KEYBOARD = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=False
    )
    list(
        map(
            lambda x:
            REPLY_KEYBOARD.add(
                InlineKeyboardButton(text=x['TEXT'])
            ),
            buttons
        )
    )
    return REPLY_KEYBOARD
