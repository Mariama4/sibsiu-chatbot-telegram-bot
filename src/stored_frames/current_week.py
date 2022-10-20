import datetime

from aiogram.types import ReplyKeyboardMarkup


def getWeek():
    nums = int(datetime.datetime.utcnow().isocalendar()[1])
    x = datetime.datetime.today()
    print(x.weekday())
    # четная
    if (nums % 2) == 0:
        if x.weekday() == 6:
            return 'Следующая неделя - НЕЧЕТНАЯ (ВВЕРХ)'
        else:
            return 'Текущая неделя - ЧЕТНАЯ (НИЗ)'
    # нечетная
    if (nums % 2) != 0:
        if x.weekday() == 6:
            return 'Следующая неделя - ЧЕТНАЯ (НИЗ)'
        else:
            return 'Текущая неделя - НЕЧЕТНАЯ (ВВЕРХ)'


async def current_week(data, message, bot, dp):
    CHAT_ID = message.chat.id
    state = dp.current_state(user=message.from_user.id)
    await state.set_state("start")
    text = getWeek()
    KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=True)
    KEYBOARD.add('Назад')
    await bot.send_message(CHAT_ID,
                           text=text,
                           reply_markup=KEYBOARD)

