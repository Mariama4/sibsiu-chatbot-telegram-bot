import logging
import os
from src.controller.controller import messageController, frameQualifier
from src.frame.frame import Frame
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from src.logger.logger import LoggingMiddleware
from src.requests.http import Http
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    filename="logs.log",
    level=logging.NOTSET,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)


api = Http()

API_TOKEN = api.get(
    path=os.getenv('API_URL_CONFIGURATION')
)['result'][0]['token']
# API_TOKEN = os.getenv('TOKEN')

frame = Frame(
    api.get(
        path=os.getenv('API_URL_FRAME')
    )
)

FRAMES_ID = frame.getIdOfFrames()

bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
