# Example: HTTPX for Async HTTP Calls
# Demonstrates how to make async HTTP requests using HTTPX

import httpx
import asyncio

async def fetch_url(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        print(f"Fetched {url} with status {response.status_code}")

async def main():
    urls = [
        "https://example.com",
        "https://httpbin.org/get",
        "https://jsonplaceholder.typicode.com/posts"
    ]
    tasks = [fetch_url(url) for url in urls]
    await asyncio.gather(*tasks)

asyncio.run(main())
