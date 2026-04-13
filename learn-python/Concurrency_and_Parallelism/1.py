import asyncio

async def main():
    print('Hello ... 1')
    await asyncio.sleep(1)
    print('... World2!')



def test():
    print('Hello ...')
    print('... World!')

print('Running test function:')
test()
print('Running async function:')
asyncio.run(main())
