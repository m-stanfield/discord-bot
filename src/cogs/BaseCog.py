from typing import TYPE_CHECKING
from discord.client import Client
import discord
import asyncio
from src.database.schema import NicknamesTable
from src.database import BaseDataBase
from src.Settings import Settings
from discord.ext import commands
from discord.ext.commands import Bot
import time
from discord.commands import slash_command, ApplicationContext
from src.logger import Logger
import inspirobot
import datetime

import src.Utilities as utils

import numpy as np


logger = Logger(__name__)

if TYPE_CHECKING:
    from src.DiscordBot import DiscordBot


class BaseCog(commands.Cog):
    def __init__(self, bot):
        logger.info("Loading Base Cog")

        self.bot: DiscordBot = bot

    @slash_command()
    async def inspire(self, ctx:ApplicationContext, member: discord.Member | None = None):
        output = ""
        if isinstance(member, discord.Member):
            output += utils.memberToMentionString(member=member)
            output += "\n"
        output += inspirobot.generate().url
        await self.bot.addMethodToQueue(ctx.respond,output)

    @slash_command()
    async def roll(self, ctx:ApplicationContext, roll_string=""):
        '''Rolls dice. !roll <dice string>. Dice string exmaple: 1d20 -4d2 + 8 -2d2'''
        await self.bot.addMethodToQueue(ctx.respond, utils.roll_dice(roll_string))

    @slash_command()
    async def nicknames(self, ctx:ApplicationContext, number:int = 10):
        nicknames = await self.bot.db.getNicknameEntries(ctx.author,number_of_entries=number)
        if nicknames is None:
            await self.bot.addMethodToQueue(ctx.respond, "No nicknames found")
            return
        if type(nicknames) is not list:
            nicknames = [nicknames]
        output = "```\nNicknames"
        entry:NicknamesTable
        for entry in nicknames:
            if len(nicknames) > 0:
                entry = entry[0]
            timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(entry.time))
            output += f"\n{timestr}: {entry.display_name}"
        output += "```"

        await self.bot.addMethodToQueue(ctx.respond, output)
         

