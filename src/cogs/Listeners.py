from discord.ext import commands
import discord


import asyncio

from src.logging.logger import Logger
from src.common.Settings import Settings
logger = Logger(__name__)


class Listeners(commands.Cog):
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if not(after.channel == None) and not(after.channel == before.channel) and not(member.name == Settings.get("BOT_NAME")) and self.bot.voice_clients == []:
            pass
