import logging

import discord
import discord.ext
import discord.ext.commands
from bot import bot
from discord import Option
from discord.ext import commands
from player import soul_db


@bot.slash_command(name="player_remove", description="", guild_ids=['1218456392730411049'])
async def player_rm(
    ctx:    discord.ApplicationContext, 
    player: Option(discord.Member, description="", required=True) # type: ignore
    ) -> None:

    async with soul_db:
        try:
            await soul_db.delete("souls", f"discord_id = {player.id}")
            resp = "Пользователь успешно удален из БД"
        
        except Exception as err:
            logging.error(f"Error while remove player: {err}")
            resp = f"Произошла ошибка при удалении пользователя. Свяжитесь с администратором/разработчиком для решения проблемы"

    await ctx.respond(resp)
