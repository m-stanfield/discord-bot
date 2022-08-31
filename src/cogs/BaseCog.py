from typing import TYPE_CHECKING
from discord.client import Client
import discord
from discord import Option, guild_only
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

    @slash_command(description="Brighten someone's day by posting an inspirational image!")
    async def inspire(self, ctx:ApplicationContext, 
                            member: Option(discord.Member,description="Whoever you want to inspire!", default = None)):
        output = ""
        if isinstance(member, discord.Member):
            output += utils.memberToMentionString(member=member)
            output += "\n"
        output += inspirobot.generate().url
        await self.bot.addMethodToQueue(ctx.respond,output)

    @slash_command(description= "Rolls dice. !roll <dice string>. Dice string exmaple: 1d20 -4d2 + 8 -2d2")
    async def roll(self, ctx:ApplicationContext, 
                         roll_string:Option(str, description="Dice you want to be rolled.", default="1d100")):
        await self.bot.addMethodToQueue(ctx.respond, utils.roll_dice(roll_string))

    @slash_command(description="A history of which nicknames you have had.")
    @guild_only()
    async def nicknames(self, ctx:ApplicationContext, 
                              number:Option(int, description="The number of nicknames to show.", default = 10), 
                              member:Option(discord.Member, description="The user who you want to see a nickname history for.", default = None)):
        member = member if member is not None else ctx.author
        nicknames = await self.bot.db.getNicknameEntries(member,number_of_entries=number)
        if nicknames is None:
            await self.bot.addMethodToQueue(ctx.respond, "No nicknames found")
            return

        output = "```\nNicknames"
        entry:NicknamesTable
        for entry in nicknames:
            if not(isinstance(nicknames, list)):
                entry = entry[0]
            timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(entry.time))
            output += f"\n{timestr}: {entry.display_name}"
        output += "```"

        await self.bot.addMethodToQueue(ctx.respond, output)
         

