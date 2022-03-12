from discord.client import Client
import discord
import asyncio
from src.database.BaseDataBase import BaseDataBase
from src.database.DiscordDataBase import DiscordDataBase
from src.common.Settings import Settings
import src.common.Utilities as utils 
from discord.ext import commands
from discord.ext.commands import Bot
import time
from discord.commands import slash_command
from discord.ext.commands.context import Context
from src.logging.logger import Logger


logger = Logger(__name__)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.DiscordBot import DiscordBot


class OwnerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot:DiscordBot = bot

    @commands.command()
    @commands.is_owner()
    async def shutdown(self,ctx:Context):
        await self.bot.setRunStatus(False)
        await self.bot.close()

    @commands.command()
    @commands.is_owner()
    async def example(self,ctx:Context,*args):
        '''Text-to-speech of whatever is said after !say command'''
        print('author',type(ctx.author))
        print(ctx.author)
        print('guild',type(ctx.guild))
        print(ctx.guild)
        print('ctx',type(ctx))
        print('ctx.author.guild',type(ctx.author.guild))
        print(ctx.author.guild)
        print("Bot Name: ",Settings.get("BOT_NAME"))
        await ctx.send(f"Mention using author: {utils.memberToMentionString(ctx.author)}")
        await ctx.send(f"Mention using dict: {utils.memberToMentionString(utils.memberToDict(ctx.author))}")

    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx, *args):
        logger.info("Restarting the modules")
        await self.bot.close()

