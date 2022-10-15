from config import *


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    frameId = 'start'
    await state.set_state(frameId)
    data = frame.frames.get(frameId)
    await messageController(data=data, message=message, bot=bot)
    # logging
    await httpLogger.checkUser(message)
    await httpLogger.sendAction(message)
    await httpLogger.sendFrameAction(message, frameId)


@dp.message_handler(state=FRAMES_ID)
async def echo(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    frameId = await frameQualifier(frame=frame, message=message, state=state)
    await state.set_state(frameId)
    data = frame.frames.get(frameId)
    await messageController(data=data, message=message, bot=bot)
    # logging
    await httpLogger.sendAction(message)
    await httpLogger.sendFrameAction(message, frameId)


@dp.message_handler()
async def clientMissMatch(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    frameId = '*'
    await state.set_state(frameId)
    data = frame.frames.get(frameId)
    await messageController(data=data, message=message, bot=bot)
    # logging
    await httpLogger.sendAction(message)
    await httpLogger.sendFrameAction(message, frameId)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
