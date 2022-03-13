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


class ReactRoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot:DiscordBot = bot