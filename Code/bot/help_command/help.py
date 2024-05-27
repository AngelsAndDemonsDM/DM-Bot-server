import discord
import discord.ext
import discord.ext.commands
from bot import bot
from discord.ext import commands

from .player_control import pl_con


@bot.command()
async def help(ctx: discord.ext.commands.Context, tabs: str = None) -> None:
    match tabs:
        case "player_control" | "pc" | "уп" | "управление игроками":
            await ctx.send(pl_con())

        case _:
            await ctx.send(
f"""
Команда help не обнаружила {tabs}.
Доступные разделы help:
```
- player_control | pc: управление игроками
```
"""
)
