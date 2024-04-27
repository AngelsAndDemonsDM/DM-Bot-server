import discord
import discord.ext
import discord.ext.commands
from bot import bot
from discord.ext import commands
from player import PlayerSoul

from . import create_dir, load_players, save_players


# Добавить красивое оформелине через дискорд эмбарг(когда ни будь когда не будет в падлу)
@bot.command()
async def player_add(ctx: discord.ext.commands.Context, player: discord.Member) -> None:
    
    data = load_players()

    if not data:
        create_dir()
    
    player_soul = PlayerSoul(player.id, player.name)
    if not player_soul in data:
        data.append(player_soul)
        save_players(data)
        await ctx.send(f"Игрок {player.name} успешно добавлен в базу данных")
        return

    await ctx.send(f"Игрок {player.name} уже находился в базе данных")
    return

@player_add.error
async def player_add_bad_argument(ctx: discord.ext.commands.Context, error) -> None:
    if isinstance(error, commands.BadArgument):
        await ctx.send("В качестве первого аргуметна необходим ID пользователя дискорд или просто упомяните его.")
        return
