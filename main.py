import asyncio

from tests.test_file_work import test_FileWork


async def run_tests():
    await test_FileWork()
async def main():
    pass

if __name__ == "__main__":
	asyncio.run(main())
