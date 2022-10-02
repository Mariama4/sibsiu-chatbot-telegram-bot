import logging
import os
from src.controller.controller import messageController, frameQualifier
from src.frame.frame import Frame
from src.db.database import Database
from src.configuration.config import Config
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from src.logger.logger import LoggingMiddleware
from dotenv import load_dotenv

load_dotenv()


def onStart():
    # INIT DB CLASS
    db = Database(
        url=os.getenv('API_URL'),
        login=os.getenv('API_LOGIN'),
        password=os.getenv('API_PASSWORD'))
    db.login(url=os.getenv('API_URL_LOGIN'))
    # GET CONFIG FROM API
    configuration = Config(database=db, url=os.getenv('API_URL_CONFIGURATION'), public=os.getenv('API_PUBLIC'))
    # GET TOKEN FOR CONNECT TO BOT
    API_TOKEN = configuration.getToken()
    # Initialize bot and dispatcher
    bot = Bot(token=API_TOKEN)

    dp = Dispatcher(bot, storage=MemoryStorage())
    dp.middleware.setup(LoggingMiddleware())
    db = Database(
        url=os.getenv('API_URL'),
        login=os.getenv('API_LOGIN'),
        password=os.getenv('API_PASSWORD'))
    db.login(url=os.getenv('API_URL_LOGIN'))
    frame = Frame(database=db)
    frame.getFrames()
    FRAMES_ID_FOR_STATES = list(frame.getIdOfFrames())
    return db, configuration, bot, dp, frame, FRAMES_ID_FOR_STATES


DATABASE, CONFIGURATION, BOT, \
    DISPATCHER, FRAME, FRAMES_ID_FOR_STATES = onStart()


def onStop():
    pass


@DISPATCHER.message_handler(commands=['start'])
async def start(message: types.Message):
    state = DISPATCHER.current_state(user=message.from_user.id)
    await state.set_state("start")
    data = FRAME.frames.get('start')
    await messageController(database=DATABASE, data=data, message=message, state=state, bot=BOT,
                            configuration=CONFIGURATION)


@DISPATCHER.message_handler(state=FRAMES_ID_FOR_STATES)
async def echo(message: types.Message):
    state = DISPATCHER.current_state(user=message.from_user.id)
    idFrame = await frameQualifier(frame=FRAME, message=message, state=state)
    await state.set_state(idFrame)
    data = FRAME.frames.get(idFrame)
    await messageController(database=DATABASE, data=data, message=message, state=state, bot=BOT,
                            configuration=CONFIGURATION)


@DISPATCHER.message_handler()
async def fgh(message: types.Message):
    await message.answer('oops!')


async def onStartPolling(_):
    # Configure logging
    logging.basicConfig(
        # filename="logs.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    # me = await bot.me
    # logger.info(f'Бот запустился под ником {me.username}.')


if __name__ == '__main__':
    executor.start_polling(DISPATCHER,
                           skip_updates=True,
                           on_startup=onStartPolling)
    onStop()
