import asyncio


async def print(text, delay): # Плавный вывод в консоль
    for char in text:
        print(char, end='', flush=True)
        await asyncio.sleep(delay)
