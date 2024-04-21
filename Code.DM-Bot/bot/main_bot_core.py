import discord
from base_classes import FileWork
from discord.ext import commands

from . import bot

TOKEN_PATH: str = "secrets/token"

@bot.command()
async def ping(ctx: discord.Interaction):
    await ctx.send(f"Pong in ({round(bot.latency * 1000)}ms)")

async def main():
    await bot.start(FileWork(TOKEN_PATH).load_data())