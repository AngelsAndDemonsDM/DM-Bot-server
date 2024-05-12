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
    ctx: discord.ApplicationContext, 
    player: Option(discord.Member, description="", required=True) # type: ignore
    ) -> None:
    user = {"discord_id": player.id}

    try:
        found_users = await soul_db.find(user)
        if found_users:
            await soul_db.delete(found_users[0]["id"])
            resp = "Пользователь успешно удален из БД"
        else:
            resp = "Пользователь не найден в БД"
    except Exception as err:
        resp = f"Произошла ошибка при удалении пользователя: {err}"

    await ctx.respond(resp)
