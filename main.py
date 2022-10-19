from aiohttp import web
from subprocess import Popen

routes = web.RouteTableDef()
app = web.Application()


class Bot:
    def __init__(self):
        self._poll = None
        self._process = None

    def setProcess(self, process):
        self._process = process
        self._poll = self._process.poll()

    def getPoll(self):
        self._poll = self._process.poll()
        return self._poll

    def terminate(self):
        self._process.terminate()


async def runBot():
    bot.setProcess(Popen(['python3', 'bot.py']))


async def stopBot():
    bot.terminate()


async def botStatus():
    return bot.getPoll()


@routes.get('/start')
async def start(req):
    await runBot()
    return web.Response(text="Running bot...")


@routes.get('/stop')
async def stop(req):
    await stopBot()
    return web.Response(text="Stopping bot...")


@routes.get('/status')
async def status(req):
    status = await botStatus()
    return web.Response(text=status)

if __name__ == "__main__":
    # install mypy для типизации
    bot = Bot()
    app.add_routes(routes)
    web.run_app(app)
