import os
from dotenv import load_dotenv
from handlers import *

load_dotenv()

API_PUBLIC = os.getenv('API_PUBLIC')


async def frameQualifier(frame, message, state):
    async with state.proxy() as data:
        previousFrame = frame.frames.get(data.state)
        for index, value in enumerate(previousFrame['markup']):
            if value['text'] == message.text:
                return value['callback']
        return 'start'


def messageController(data, message, bot):
    # Определение типа сообщения
    match data['type']:
        case "text":
            return textMessageHandler(data, message)
        case "photo":
            return photoMessageHandler(data, message, bot, API_PUBLIC)
        case "media_group":
            return mediaGroupMessageHandler(data, message, bot, API_PUBLIC)
        case "video_note":
            return videoNoteMessageHandler(data, message, bot, API_PUBLIC)
        case "venue":
            return venueMessageHandler(data, message, bot)
        case "contact":
            return contactMessageHandler(data, message, bot)
        case "web_app":
            return webAppHandler(data, message)
        case "document":
            return documentMessageHandler(data, message, bot, API_PUBLIC)
        case "location":
            return locationMessageHandler(data, message, bot)
        case _:
            # not found
            pass
