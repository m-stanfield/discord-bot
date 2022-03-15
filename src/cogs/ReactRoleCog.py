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



 # rough idea for how reaction roles might work
    """
    @slash_command
    def add_role(self, role, emoji, role_group, link=None, description=None):
        pass

    @slash_command
    def remove_role(self, role):
        pass

    @slash_command
    def remove_role_from_group(self, role, role_group):
        pass

    @slash_command
    def define_group(self, role_group, mutual_exclusive=False, *args, **kwargs):
        pass

    @slash_command
    def post_role_message(self, auto_sticky=True):
        pass

    @slash_command
    def reset_role_settings(self):
        pass

    """