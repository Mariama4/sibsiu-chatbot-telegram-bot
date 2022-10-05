import logging
import os
from src.controller.controller import messageController, frameQualifier
from src.frame.frame import Frame
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from src.logger.logger import LoggingMiddleware
from src.requests.http import Http
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
        filename="logs.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )


api = Http()

# API_TOKEN = api.get(
#     path=os.getenv('API_URL_CONFIGURATION')
# )['configuration'][0]['token']
API_TOKEN = os.getenv('token')

frame = Frame(
    api.get(
        path=os.getenv('API_URL_FRAME')
    )
)

FRAMES_ID = frame.getIdOfFrames()

bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


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



