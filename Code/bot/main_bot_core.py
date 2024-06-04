import discord
import discord.ext
import discord.ext.commands
from bot import bot
from bot.help_command import help
from bot.player_control import player_add, player_rm
from db_work import SettingsManager
from discord.ext import commands


@bot.command()
async def ping(ctx: discord.ext.commands.Context):
    await ctx.send(f"Pong in ({round(bot.latency * 1000)}ms)")

async def bot_start():
    settings_manager: SettingsManager = SettingsManager()
    settings_manager.start()
    await bot.start(await settings_manager.get_setting("token"))
