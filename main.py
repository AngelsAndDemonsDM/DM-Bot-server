import asyncio

from tests.test_file_work import test_FileWork
from tests.test_tag_system import test_TagData, test_TagsManager


async def run_tests():
    await test_FileWork()
    await test_TagData()
    await test_TagsManager()

async def main():
    pass

if __name__ == "__main__":
	asyncio.run(main())
