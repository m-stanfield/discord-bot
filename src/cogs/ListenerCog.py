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
import datetime

logger = Logger(__name__)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.DiscordBot import DiscordBot


class ListenerCog(commands.Cog):
    def __init__(self, bot):
        self.bot:DiscordBot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if not(after.channel == None) and not(after.channel == before.channel) and not(member.name == Settings.get("BOT_NAME")) and self.bot.voice_clients == []:
            pass

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        pass

    @commands.Cog.listener()
    async def on_ready(self):
        # Note: may be ran multiple times.
        pass

    @commands.Cog.listener()
    async def on_connect(self):
        logger.info("Bot has connected to Discord")

    @commands.Cog.listener()
    async def on_disconnect(self):
        logger.info("Bot has disconnected from Discord")

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        pass

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        pass

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member | discord.User):
        pass

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.Member | discord.User):
        pass

    @commands.Cog.listener()
    async def on_reaction_clear(self, message: discord.Message, reactions: list[discord.Reaction]):
        pass

    @commands.Cog.listener()
    async def on_reaction_clear_emoji(self, reaction: discord.Reaction):
        pass

    @commands.Cog.listener()
    async def on_guild_channel_pins_update(self, channel: discord.abc.GuildChannel, last_pint: datetime.datetime | None = None):
        pass

    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        pass

    @commands.Cog.listener()
    async def on_member_remove(self, member:discord.Member):
        pass

    @commands.Cog.listener()
    async def on_member_update(self, before:discord.Member, after:discord.Member):
        pass

    @commands.Cog.listener()
    async def on_user_update(self, before:discord.User, after:discord.User):
        # TODO: Implement auto-replacement of previous user info to  current discord info
        pass

    

