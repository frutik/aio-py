import os
import aiohttp
import asyncio

from sanic import Sanic
from sanic.response import json

from app.utils.helper import hello_world

SANIC_PREFIX = "SANIC_"

app = Sanic()


@app.listener('before_server_start')
async def init(app, loop):
    app.aiohttp_session = aiohttp.ClientSession(loop=loop)


# @app.listener('after_server_stop')
# async def finish(app, loop):
#     loop.run_until_complete(app.session.close())
#     loop.close()


@app.route("/hello-world")
async def test(request):
    return json(hello_world())

async def function_1():
    url = "https://api.github.com/repos/channelcat/sanic"
    async with app.aiohttp_session.get(url) as response:
        return await response.json()

async def function_2():
    url = "https://api.github.com/repos/channelcat/sanicw"
    async with app.aiohttp_session.get(url) as response:
        return await response.json()


@app.route("/search")
async def search(request):
    print(request.headers.get('user-agent'))

    resp = await asyncio.gather(function_1(), function_2())
    return json({'resp': resp})


app.static('/static', './static')  # while in docker files from static will be served by ngnix
if __name__ == "__main__":
    for k, v in os.environ.items():
        if k.startswith(SANIC_PREFIX):
            _, config_key = k.split(SANIC_PREFIX, 1)
            app.config[config_key] = v
    app.run(host="0.0.0.0", port=8000, workers=1, debug=True)
