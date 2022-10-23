from aiogram.types import ParseMode, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo


async def webAppHandler(data, message):
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=False
    )

    keyboard.add(
        InlineKeyboardButton(
            text=data['web_app_button_text'],
            web_app=WebAppInfo(
                url=data['web_app']
            )
        )
    )

    list(
        map(
            lambda x:
            keyboard.add(
                InlineKeyboardButton(text=x['text'])
            ),
            data['markup']
        )
    )

    return await message.answer(
        text=data['web_app_caption'],
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
