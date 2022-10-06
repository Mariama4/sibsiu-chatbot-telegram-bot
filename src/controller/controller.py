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
        for index, value in enumerate(previousFrame['markup']):
            if value['text'] == message.text:
                return value['callback']


def messageController(data, message, bot):
    # Определение типа сообщения
    match data['type']:
        case "text":
            return textMessageController(data, message)
        case "photo":
            return photoMessageController(data, message, bot)
        case "media_group":
            return mediaGroupMessageController(data, message, bot)
        case "video_note":
            return videoNoteMessageController(data, message, bot)
        case "venue":
            return venueMessageController(data, message, bot)
        case "contact":
            return contactMessageController(data, message, bot)
        case "web_app":
            return webAppController(data, message)
        case _:
            # not found
            pass


def textMessageController(data, message):
    keyboard = keyboardController(data['markup'])
    return message.answer(text=data['text'],
                          parse_mode=ParseMode.HTML,
                          reply_markup=keyboard)


def photoMessageController(data, message, bot):
    keyboard = keyboardController(data['markup'])
    photo = InputFile.from_url(API_PUBLIC + data['photo'])
    return bot.send_photo(
        chat_id=message.chat.id,
        caption=data['photo_caption'],
        parse_mode=ParseMode.HTML,
        photo=photo,
        reply_markup=keyboard
    )


async def mediaGroupMessageController(data, message, bot):
    keyboard = keyboardController(data['markup'])
    mediaGroup = mediaGroupController(data['media_group'])
    await bot.send_media_group(chat_id=message.chat.id,
                               media=mediaGroup)
    return await message.answer(text=data['media_group_caption'],
                                parse_mode=ParseMode.HTML,
                                reply_markup=keyboard)


async def videoNoteMessageController(data, message, bot):
    keyboard = keyboardController(data['markup'])
    video_note = API_PUBLIC + data['video_note']
    await bot.send_video_note(chat_id=message.chat.id,
                              video_note=InputFile.from_url(video_note,
                                                            data['video_note']))
    return await message.answer(text=data['video_note_caption'],
                                parse_mode=ParseMode.HTML,
                                reply_markup=keyboard)


async def venueMessageController(data, message, bot):
    keyboard = keyboardController(data['markup'])
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


async def contactMessageController(data, message, bot):
    keyboard = keyboardController(data['markup'])
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


def webAppController(data, message):
    keyboard = keyboardController(data['markup'])
    keyboard.add(
        InlineKeyboardButton(
            text=data['web_app_button_text'],
            web_app=WebAppInfo(
                url=data['web_app']
            )
        )
    )
    return message.answer(
        text=data['web_app_caption'],
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
                InlineKeyboardButton(text=x['text'])
            ),
            buttons
        )
    )
    return REPLY_KEYBOARD
