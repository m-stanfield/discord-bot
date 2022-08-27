import datetime
from typing import TYPE_CHECKING

import discord
from discord.ext import commands
from src.logger import Logger
from src.Settings import Settings

logger = Logger(__name__)

if TYPE_CHECKING:
    from src.DiscordBot import DiscordBot


class ListenerCog(commands.Cog):
    def __init__(self, bot):
        logger.info("Loading Listener Cog")

        self.bot: DiscordBot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if not(after.channel == None) and not(after.channel == before.channel) and not(member.name in Settings.get("BOT_NAMES")):
            await self.bot.addMethodToQueue(self.bot.playUserAudio, after.channel, member)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        pass

    @commands.Cog.listener()
    async def on_ready(self):
        # Note: may be ran multiple times.
        logger.info("Updating all guild information")
        await self.bot.db.updateAllGuilds(guilds=self.bot.guilds, regenerate_audio=True)
        logger.info("Completed updating all guild information")

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
    async def on_member_join(self, member: discord.Member):
        await self.bot.addMethodToQueue(self.bot.db.updateMember, member=member)
        await self.bot.addMethodToQueue(self.bot.db.generateMemberAudio, member=member)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        pass

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        successful = True
        logger.info("Attempting to update member info for member %s in guild %s"%(after.name, after.guild))
        successful = successful and await self.bot.addMethodToQueue(self.bot.db.updateMember, member=after,previous_member=before, regenerate_audio=True)

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        # TODO: Implement auto-replacement of previous user info to  current discord info
        pass
