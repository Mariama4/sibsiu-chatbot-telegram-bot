from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, CallbackQuery, ContentType, \
    ChatActions, ReplyKeyboardMarkup


async def frameQualifier(frame, message, state):
    async with state.proxy() as data:
        previousFrame = frame.frames.get(data.state)
        for index, value in enumerate(previousFrame['BUTTONS']):
            if value['TEXT'] == message.text:
                return value['REDIRECT_ON_ID_FRAME']


def messageController(database, data, message, state):
    # Определение типа сообщения
    match data['MESSAGE']['TYPE']:
        case "TEXT":
            return textMessageController(database, data, message)
        case "PHOTO":
            pass
        case _:
            # not found
            pass


def textMessageController(database, data, message):
    keyboard = keyboardController(data['BUTTONS'])
    return message.answer(text=data['MESSAGE']['TEXT'],
                          reply_markup=keyboard)


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



