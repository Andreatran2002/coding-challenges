import asyncio
from time import sleep

async def main():
    loop = asyncio.get_event_loop()

    async def hello_task():
        print("Hello from async thread!")
        await asyncio.sleep(1)
        print("Hello from async thread! 2")
        sleep(1)
        print("Hello from async thread! 3")
        await asyncio.sleep(1)
        print("Hello from async thread! 4")
        await asyncio.sleep(1)
        print("Hello from async thread! 5")
        await asyncio.sleep(1)
    print("Hello from main thread! 1")
    await hello_task()
    print("Hello from main thread!")

if __name__ == "__main__":
    asyncio.run(main())