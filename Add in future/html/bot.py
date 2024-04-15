import discord
from discord.ext import commands


BOT = None
BOT_TOKEN = "MTIyNzkyNjEzODQwMDI3NjU2MQ.GDLOtJ.MzJgySrXPntmrriEZ5UK_91Rc1Dk8QJYpGtwDk"

def get_bot() -> commands.Bot:
    intents = discord.Intents.all()
    return commands.Bot(command_prefix='!', intents=intents, help_command=None)

async def bot_start() -> None:
    global BOT
    
    if not BOT:
        BOT = get_bot()
    
    await BOT.start(BOT_TOKEN)

def bot_status() -> str:
    global BOT

    if BOT and BOT.is_ready():
        status = '<span style="color: green;">online</span>'
    else:
        status = '<span style="color: red;">offline</span>'
    
    return status