import logging

import discord
import discord.ext
import discord.ext.commands
from bot import bot
from discord import Option
from discord.ext import commands
from player import soul_db


@bot.slash_command(name="player_add", description="", guild_ids=['1218456392730411049'])
async def player_add(
    ctx:    discord.ApplicationContext, 
    player: Option(discord.Member, description="", required=True) # type: ignore
    ) -> None:

    async with soul_db:
        try:
            await soul_db.insert("souls", {"discord_id": int(player.id), "name": str(player.name)})
            resp = "Пользователь успешно добавлен в БД"
        
        except Exception as err:
            logging.error(f"Error while add player: {err}")
            resp = f"Произошла ошибка при добавлении пользователя. Свяжитесь с администратором/разработчиком для решения проблемы"

    await ctx.respond(resp)
