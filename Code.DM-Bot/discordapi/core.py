import discord
from discord.ext import commands

global BOT

async def bot_main(token):
    intents = discord.Intents.all()
    global BOT
    BOT = commands.Bot(command_prefix='!', intents=intents, help_command=None)
    BOT.start(token)
