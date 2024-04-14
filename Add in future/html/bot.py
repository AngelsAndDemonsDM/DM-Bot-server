import discord
from discord.ext import commands


BOT = None
BOT_STATUS = "N/D"
BOT_TOKEN = "MTIyNzkyNjEzODQwMDI3NjU2MQ.GDLOtJ.MzJgySrXPntmrriEZ5UK_91Rc1Dk8QJYpGtwDk"

def get_bot() -> commands.Bot:
    intents = discord.Intents.all()
    return commands.Bot(command_prefix='!', intents=intents, help_command=None)

async def bot_start() -> None:
    global BOT
    
    if not BOT:
        BOT = get_bot()
    
    await BOT.start(BOT_TOKEN)

async def bot_shutdown() -> None:
    global BOT

    if BOT:
        await BOT.close()

def bot_status() -> str:
    global BOT
    global BOT_STATUS

    if BOT and BOT.is_ready():
        BOT_STATUS = '<span style="color: green;">online</span>'
    else:
        BOT_STATUS = '<span style="color: red;">offline</span>'
    
    return BOT_STATUS