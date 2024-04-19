# import discord
# from discord.ext import commands

# BOT_TOKEN = "MTIyNzkyNjEzODQwMDI3NjU2MQ.GDLOtJ.MzJgySrXPntmrriEZ5UK_91Rc1Dk8QJYpGtwDk"

# class BotWeb:
#     def __init__(self, token: str):
#         self._token = token
#         self._bot: commands.Bot = None
    
#     def _setup(self) -> None:
#         intents = discord.Intents.all()
#         self._bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

#     async def start(self) -> None:
#         if self._bot:
#             return
        
#         self._setup()
#         await self._bot.start(self._token)
    
#     def status(self) -> bool:
#         return self._bot and self._bot.is_ready()

#     def status_str_html(self) -> str:
#         if self.status():
#             status = '<span style="color: green;">online</span>'
#         else:
#             status = '<span style="color: red;">offline</span>'
        
#         return status
    
#     @property
#     def bot(self):
#         return self._bot
