import logging

import discord
import discord.ext
import discord.ext.commands
from bot import bot
from discord import Option
from discord.ext import commands
from player import soul_db


# TODO: оформелине через дискорд эмбарг(maybe)
@bot.slash_command(name="player_add", description="", guild_ids=['1218456392730411049'])
async def player_add(
    ctx:    discord.ApplicationContext, 
    player: Option(discord.Member, description="", required=True) # type: ignore
    ) -> None:
    user = {"disord_id": player.id, "name": player.name}

    try:  
        await soul_db.add(user)
        resp = "Пользователь успешно добавлен в БД"
    except Exception as err:
        resp = f"Пользователь не был добавлен в БД. Ошибка: {err}"

    await ctx.respond(resp)
