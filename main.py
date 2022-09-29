from code_tests_examples.tests import testAuth, testGetFrames
from src.controller.controller import messageController, frameQualifier
from src.frame.frame import Frame
from src.db.database import Database
import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from src.logger.logger import LoggingMiddleware
from dotenv import load_dotenv
load_dotenv()


API_TOKEN = os.getenv('API_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

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


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state("start")
    data = frame.frames.get('start')
    await messageController(database=db, data=data, message=message, state=state, bot=bot)


@dp.message_handler(state=FRAMES_ID_FOR_STATES)
async def echo(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    idFrame = await frameQualifier(frame=frame, message=message, state=state)
    await state.set_state(idFrame)
    data = frame.frames.get(idFrame)
    await messageController(database=db, data=data, message=message, state=state, bot=bot)


@dp.message_handler()
async def fgh(message: types.Message):
    await message.answer('oops!')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
