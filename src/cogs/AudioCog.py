from typing import TYPE_CHECKING
from discord.client import Client
import discord
import asyncio
from src.database import BaseDataBase
from src.Settings import Settings
from discord.ext import commands
from discord.ext.commands import Bot
import time
from discord.commands import slash_command, ApplicationContext
from discord import option
from src.logger import Logger
import inspirobot
import os
import pathlib

import src.Utilities as utils

import numpy as np

from src.database.schema import (GUILD_TABLE, NICKNAME_TABLE, SETTING_TABLE,
                                 USER_TABLE, Base, GuildsTable, NicknamesTable, SettingsTable,
                                 UsersTable)

logger = Logger(__name__)

if TYPE_CHECKING:
    from src.DiscordBot import DiscordBot


class AudioCog(commands.Cog):
    def __init__(self, bot):
        logger.info("Loading Audio Cog")
        self.bot: DiscordBot = bot

    @slash_command()
    async def say(self, ctx:ApplicationContext, text:str, lang:str = "en"):
        channel:discord.VoiceChannel = self.bot.findMemberInVoiceChannel(ctx=ctx)
        file_name = self.bot.db.generateAndGetSayClip(text = text, lang = lang)
        await ctx.delete()
        if os.path.exists(file_name):
            await self.bot.addMethodToQueue(self.bot.playAudio,channel = channel, file_name = file_name, volume = 1.0, length = 3)

    @slash_command()
    async def play(self, ctx:ApplicationContext, member:discord.Member, custom_audio:bool|None = None):
        channel:discord.VoiceChannel = self.bot.findMemberInVoiceChannel(ctx=ctx)
        await ctx.delete()
        await self.bot.addMethodToQueue(self.bot.playUserAudio, channel, member, custom_audio = custom_audio)

    @slash_command()
    async def volume(self, ctx:ApplicationContext, volume:float = 0.3, member:discord.Member|None = None):
        await ctx.delete()
        if not(type(volume) == float):
            return

        updated_member:discord.Member = ctx.author
        logger.info(f"Setting volume for member {updated_member.id} on {updated_member.guild.id} to a volume of {volume}")
        async with self.bot.db._async_session() as session: 
            setting:SettingsTable = await self.bot.db.getSettingEntry(member=updated_member, session=session)
            setting.volume = volume
            await session.commit()

    @slash_command()
    async def length(self, ctx:ApplicationContext, length:float = 0.3, member:discord.Member|None = None):
        await ctx.delete()
        if not(type(length) == float):
            return

        updated_member:discord.Member = ctx.author
        logger.info(f"Setting volume for member {updated_member.id} on {updated_member.guild.id} to a length of {length}")
        async with self.bot.db._async_session() as session: 
            setting:SettingsTable = await self.bot.db.getSettingEntry(member=updated_member, session=session)
            setting.length = length
            await session.commit()

    @slash_command()
    async def solo_play(self, ctx:ApplicationContext, enable:bool):
        await ctx.delete()
        if not(type(enable) == bool):
            ctx.author.send("Improper slash command arguments. Solo play slash command requires a true/false value.")
            return

        updated_member:discord.Member = ctx.author
        logger.info(f"Setting solo play for member {updated_member.id} on {updated_member.guild.id} to {enable}")
        async with self.bot.db._async_session() as session: 
            setting:SettingsTable = await self.bot.db.getSettingEntry(member=updated_member, session=session)
            setting.solo_audio_play = enable
            await session.commit()

    @slash_command()
    @option("attachment", discord.Attachment, description="The mp3 file to set as your custom audio.")
    async def upload_audio(self, ctx:ApplicationContext, attachment: discord.Attachment):
        await ctx.delete()
        memberForAudio = ctx.author # TODO: add optional super call
        if not(attachment):
            await ctx.author.send("No attachment was sent with custom audio upload slash command")
            return
        if not(attachment.filename.endswith(".mp3")):
            await ctx.author.send("Audio files must be .mp3 files")
            return
        await self.bot.addMethodToQueue(self._upload_audio,ctx=ctx, attachment=attachment, member = memberForAudio)

    async def _upload_audio(self, ctx:ApplicationContext, attachment: discord.Attachment, member:discord.Member):
        base_path = Settings.get(['data','audio','custom'])
        path = os.path.join(base_path, self.bot.db._generateMP3Name(member))
        await attachment.save(pathlib.Path(path))
        file = await attachment.to_file()
        await member.send(f"The following audio file has been set as your custom audio on {ctx.guild}",file=file)

          

