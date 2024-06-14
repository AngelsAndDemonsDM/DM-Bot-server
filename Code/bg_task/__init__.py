from Code.bot import bot_start
from Code.db_work import SettingsManager


async def main_bg_task():
    settings_manager = SettingsManager()
    
    if settings_manager.get_setting("bot.auto_start"):
        await bot_start()
