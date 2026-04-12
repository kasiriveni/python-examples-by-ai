# Example: Streaming Responses
# Demonstrates handling streaming responses with aiohttp

import aiohttp
import asyncio

async def fetch_stream(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            async for chunk in response.content.iter_chunked(1024):
                print(chunk.decode())

async def main():
    url = "https://httpbin.org/stream/5"
    await fetch_stream(url)

asyncio.run(main())
