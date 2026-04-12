# aiohttp: Async Web Framework

from aiohttp import web

async def handle(request):
    return web.Response(text="Hello, aiohttp!")

app = web.Application()
app.router.add_get('/', handle)

if __name__ == "__main__":
    web.run_app(app)
