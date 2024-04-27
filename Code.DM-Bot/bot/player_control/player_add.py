import logging
import discord
import discord.ext
import discord.ext.commands
from bot import bot
from bot.player_control.player_file_work import (create_dir, load_players,
                                                 save_players)
from discord.ext import commands
from player import PlayerSoul


# Добавить красивое оформелине через дискорд эмбарг(когда ни будь когда не будет в падлу)
@bot.command()
async def player_add(ctx: discord.ext.commands.Context, player: discord.Member) -> None:
    try:
        data: list[PlayerSoul] = load_players()

        if not data:
            create_dir()
            data: list[PlayerSoul] = []
            await add_payer_to_bd(ctx, data, PlayerSoul(player.id, player.name))
            return
        
        for soul in data:
            if soul.id == player.id:
                await ctx.send(f"Игрок {player.name} уже находился в базе данных")
                return

        await add_payer_to_bd(ctx, data, PlayerSoul(player.id, player.name))
        return
    except Exception as err:
        logging.error(f"player_control.player_add error: {err}")

@player_add.error
async def player_add_bad_argument(ctx: discord.ext.commands.Context, error) -> None:
    if isinstance(error, commands.BadArgument):
        await ctx.send("В качестве первого аргуметна необходим ID пользователя дискорд или просто упомяните его.")
        return

async def add_payer_to_bd(ctx: discord.ext.commands.Context, data_list: list[PlayerSoul], player: PlayerSoul) -> None:
    data_list.append(player)
    save_players(data_list)

    await ctx.send(f"Игрок {player.name} успешно добавлен в базу данных")
