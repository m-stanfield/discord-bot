from pydoc import describe
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
from src.logger import Logger
import inspirobot
import os
import pathlib
import re
from discord import Option, guild_only, user_command
import src.Utilities as utils
from typing import Union

import numpy as np

from src.database.schema import (GUILD_TABLE, NICKNAME_TABLE, SETTING_TABLE,
                                 USER_TABLE, Base, GuildsTable, NicknamesTable, SettingsTable,
                                 UsersTable)
import gtts.lang
logger = Logger(__name__)

if TYPE_CHECKING:
    from src.DiscordBot import DiscordBot
SAY_DEFAULT = gtts.lang.tts_langs()["en"]
SAY_LANGS_DICT = {word:key for key, word in gtts.lang.tts_langs().items()}
SAY_LANGS_CHOICES = list(SAY_LANGS_DICT.keys())


async def get_lang(ctx: discord.AutocompleteContext):
    """Returns a list of colors that begin with the characters entered so far."""
    return [lang for lang in SAY_LANGS_CHOICES if lang.lower().startswith(ctx.value.lower())]

class AudioCog(commands.Cog):
    def __init__(self, bot):
        logger.info("Loading Audio Cog")
        self.bot: DiscordBot = bot

    @slash_command(description="Play a custom phrase audio clip")
    @guild_only()
    async def say(self, ctx:ApplicationContext, 
                        text:Option(str, name="text",  description="Phrase to play"), 
                        lang:Option(str, name="lang",  description="The 'accents' used.", default=SAY_DEFAULT,required=False, autocomplete=get_lang)):
        channel:discord.VoiceChannel = self.bot.findMemberInVoiceChannel(ctx=ctx)
        if not(channel):
            await self.bot.addMethodToQueue(ctx.author.send, "For the say command to work, you are required to be in a voice channel I can see.")
            await self.bot.addMethodToQueue(ctx.delete)
            return
        cleaned_text = re.sub("[^A-Za-z0-9 ]+", '', text) # removes all character except alphanumeric and spaces
        file_name = self.bot.db.generateAndGetSayClip(text = cleaned_text, lang = SAY_LANGS_DICT[lang])
        await ctx.delete()
        if os.path.exists(file_name):
            await self.bot.addMethodToQueue(self.bot.playAudio,channel = channel, file_name = file_name, volume = 1.0, length = 3)
    
    @slash_command(description="Plays a user's audio clip.")
    @guild_only()
    async def play(self, ctx:ApplicationContext, 
                         member:Option(discord.Member, description="Who's audio should I play?"), 
                         custom_audio:Option(bool, description="Should custom clip (True) or nickname (False) be used?", default=None)):
        channel:discord.VoiceChannel = self.bot.findMemberInVoiceChannel(ctx=ctx)
        queued_time = time.time()
        await ctx.delete()
        await self.bot.addMethodToQueue(self.bot.playUserAudio, channel, member, custom_audio = custom_audio, queued_time=queued_time)

    @user_command()
    async def play_audio(self, ctx:ApplicationContext, member:discord.Member):
        await self.play(ctx=ctx, member = member, custom_audio = None)

    @slash_command(description="Adjust the volume for your custom audio clip.")
    @guild_only()
    async def volume(self, ctx:ApplicationContext, 
                           volume:Option(float, description="The audio value to set, suggested value <0.5.", min_value=0.0)):
        await ctx.delete()
        if not(type(volume) == float):
            return

        updated_member:discord.Member = ctx.author
        logger.info(f"Setting volume for member {updated_member.id} on {updated_member.guild.id} to a volume of {volume}")
        async with self.bot.db._async_session() as session: 
            setting:SettingsTable = await self.bot.db.getSettingEntry(member=updated_member, session=session)
            setting.volume = volume
            await session.commit()

    @slash_command(description="Sets the length of an custom audio clip.")
    @guild_only()
    async def length(self, ctx:ApplicationContext,
                           length:Option(float, description="Length of clip (max 3 seconds)", min_value=0, max_value=3)):
        await ctx.delete()
        if not(type(length) == float):
            return
        length = length if length < 3.0 else 3.0
        updated_member:discord.Member = ctx.author
        logger.info(f"Setting length for member {updated_member.id} on {updated_member.guild.id} to a length of {length}")
        async with self.bot.db._async_session() as session: 
            setting:SettingsTable = await self.bot.db.getSettingEntry(member=updated_member, session=session)
            setting.length = length
            await session.commit()

    @slash_command(description="Sets the rate of custom audio plays.")
    @guild_only() 
    async def custom_audio(self, ctx:ApplicationContext, 
                                 ratio:Option(float, description="Rate of custom audio. 0 is never 1 is always.",min_value=0, max_value=1)):
        await ctx.delete()
        if not(type(ratio) == float):
            return

        updated_member:discord.Member = ctx.author
        logger.info(f"Setting custom audio relative frequency for member {updated_member.id} on {updated_member.guild.id} to a length of {ratio}")
        async with self.bot.db._async_session() as session: 
            setting:SettingsTable = await self.bot.db.getSettingEntry(member=updated_member, session=session)
            setting.custom_audio_relative_frequency = ratio
            await session.commit()

    @slash_command(description="Should I play your audio if you are the only one on a voice channel?")
    @guild_only()
    async def solo_play(self, ctx:ApplicationContext, enable:Option(bool, description="Enable (true) or Disable (false)")):
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

    @slash_command(description="Upload a custom audio clip for when you join a voice channel.")
    @guild_only()
    async def upload_audio(self, ctx:ApplicationContext, 
                                 attachment:Option(discord.Attachment, description="The mp3 file to set as your custom audio.")):
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

          

