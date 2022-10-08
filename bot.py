from config import *


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state("start")
    data = frame.frames.get('start')
    await messageController(data=data, message=message, bot=bot)


@dp.message_handler(state=FRAMES_ID)
async def echo(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    idFrame = await frameQualifier(frame=frame, message=message, state=state)
    await state.set_state(idFrame)
    data = frame.frames.get(idFrame)
    await messageController(data=data, message=message, bot=bot)


@dp.message_handler()
async def clientMissMatch(message: types.Message):
    await message.answer('oops!')



