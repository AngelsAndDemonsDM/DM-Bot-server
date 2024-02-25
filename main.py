import asyncio

from tests.test_file_work import TestFileWorkDef


async def main():
    await TestFileWorkDef()

if __name__ == "__main__":
	asyncio.run(main())
