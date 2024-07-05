import os
import shutil
import unittest

import aiosqlite

from Code.db_work import AsyncDB


class TestAsyncDB(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        pass

    async def asyncTearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
