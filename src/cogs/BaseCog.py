from typing import TYPE_CHECKING
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
from discord.commands import slash_command, ApplicationContext
from src.logging.logger import Logger
import inspirobot


logger = Logger(__name__)

if TYPE_CHECKING:
    from src.DiscordBot import DiscordBot


class BaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot

    @slash_command()
    async def inspire(self, ctx:ApplicationContext, member: discord.Member | None = None):
        output = ""
        if isinstance(member, discord.Member):
            output += utils.memberToMentionString(member=member)
            output += "\n"
        output += inspirobot.generate().url
        await ctx.respond(output)

    @slash_command()
    async def roll(self, ctx:ApplicationContext, roll_string=""):
        '''Rolls dice. !roll <dice string>. Dice string exmaple: 1d20 -4d2 + 8 -2d2'''
        await ctx.respond(utils.roll_dice(roll_string))

    @slash_command()
    async def nicknames(self, ctx:ApplicationContext, member: discord.Member | None = None, number: int = 5):
        member = member if member is not None else ctx.author
        member = utils.memberToSchema(member)
        nickname_str = await self.bot.db.getMemberNicknames(member_values=member, number_of_nicknames=number)
        await ctx.respond(nickname_str)

    @slash_command()
    async def play(self, ctx:ApplicationContext, member: discord.Member | None = None, custom_audio:float=None):
        channel = ctx.author.voice.channel
        if channel is not None:
            member = member if member is not None else ctx.author
            user = utils.memberToSchema(member=member)
            user = await self.bot.db.getValues(user=user)
            await self.bot.playUserAudio(channel, member)

