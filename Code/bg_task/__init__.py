from bot import bot_start
from db_work import SettingsManager


async def main_bg_task():
    settings_manager = SettingsManager()
    
    if await settings_manager.get_setting("bot.auto_start"):
        await bot_start()
