from aiogram.types import ReplyKeyboardMarkup, InputFile, InlineKeyboardButton
from aiogram import types


def mediaGroupBuilder(media, api_public):
    mediaGroup = types.MediaGroup()
    for index, value in enumerate(media):
        mediaGroup.attach_photo(
            InputFile.from_url(api_public + value)
        )

    return mediaGroup


def keyboardBuilder(buttons):
    reply_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=False
    )
    list(
        map(
            lambda x:
            reply_markup.add(
                InlineKeyboardButton(text=x['text'])
            ),
            buttons
        )
    )
    return reply_markup
