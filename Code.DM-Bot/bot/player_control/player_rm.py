import logging

import discord
import discord.ext
import discord.ext.commands
from bot import bot
from bot.player_control.player_file_work import load_players, save_players
from discord.ext import commands
from player import PlayerSoul


@bot.command()
async def player_rm(ctx: discord.ext.commands.Context, player: discord.Member) -> None:
    try:
        data: list[PlayerSoul] = load_players()
        
        if not data:
            await ctx.send("Не удалось найти БД.")
            return
        
        for soul in data:
            if soul.id == player.id:
                data.remove(soul)
                save_players(data)
                await ctx.send(f"{player.name} был найден и удалён из базы данных.")
                return
            
        await ctx.send(f"{player.name} не был найден в базе данных")
        return
    except Exception as err:
        logging.error(f"player_control player_rm: {err}")
    
@player_rm.error
async def player_rm_bad_argument(ctx: discord.ext.commands.Context, error) -> None:
    if isinstance(error, commands.BadArgument):
        await ctx.send("В качестве первого аргуметна необходим ID пользователя дискорд или просто упомяните его.")
        return
