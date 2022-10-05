from aiohttp import web
import os
from dotenv import load_dotenv
load_dotenv()


async def handle(request):
    return web.Response(text='Hi!')


async def toggleBot(request):
    pass


app = web.Application()
app.add_routes([
    web.get('/', handle),
    web.get('/togglebot', toggleBot)
])

if __name__ == '__main__':
    web.run_app(app)
