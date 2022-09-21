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
from discord import Option, guild_only, user_command, default_permissions
import src.Utilities as utils
from typing import Union

import numpy as np

from src.database.schema import (GUILD_TABLE, NICKNAME_TABLE, SETTING_TABLE,
                                 USER_TABLE, Base, EmotesTable, GuildsTable, NicknamesTable, SettingsTable,
                                 UsersTable)
import gtts.lang
logger = Logger(__name__)

if TYPE_CHECKING:
    from src.DiscordBot import DiscordBot




class EmoteCog(commands.Cog):
    def __init__(self, bot):
        logger.info("Loading Emote Cog")

        self.bot: DiscordBot = bot

    async def autocomplete_emote(self, ctx: discord.AutocompleteContext):
        results = await self.bot.db.getAllGuildEmoteEntries(guild=ctx.interaction.guild)
        if (results):
            return [result[0].emote_name for result in results if result[0].emote_name.lower().startswith(ctx.value.lower())] if type(results) == list else [results.emote_name]
        return []

    @slash_command(description="Post a custom server emote!")
    @guild_only()
    async def emote(self, ctx:ApplicationContext, emote_name:Option(str, description="The name of the emote to post.",autocomplete=autocomplete_emote)):
        result = await self.bot.db.getGuildEmoteEntry(ctx.guild, emote_name)
        if result:
            path = result.path
            if path:
                await self.bot.addMethodToQueue(ctx.respond,file = discord.File(path))
                return
        ctx.author.send(f"No emote with the name {emote_name} found in the server {ctx.guild.name}.")


    @default_permissions(administrator=True)
    @slash_command(description="Upload a custom server emote.")
    @guild_only()
    async def upload_emote(self, ctx:ApplicationContext, 
                                 emote_name:Option(str, description="The name that will be used by the emote",required=True),
                                 attachment:Option(discord.Attachment, description="The image file to set as a server emote."),
                                 overwrite:Option(bool, description="Overwrite emote name if it already exists", default=False)):
   
        await ctx.delete()
        IMAGE_FORMATS:tuple = (".png",".jpeg",".tiff",".tif",".jpg", ".gif", ".bmp")
        file_name:str = attachment.filename


        base_path = Settings.get(['data','images','emotes'])
        extension = pathlib.Path(attachment.filename).suffix
        path = os.path.join(base_path, f"{ctx.guild_id}_{emote_name}{extension}")

        if not(attachment):
            await ctx.author.send("No attachment was sent with custom audio upload slash command")
            return
        if not(file_name.lower().endswith(IMAGE_FORMATS)):
            await ctx.author.send("Audio files must be one of the following image types: " + IMAGE_FORMATS)
            return
        if os.path.isfile(path) and not(overwrite):
            await ctx.author.send("Image file already exists for this guild. Upload under a new name or overwrite the previous image.")
            return

        await self.bot.addMethodToQueue(self._upload_image,ctx=ctx, path=path, emote_name = emote_name, attachment=attachment)

    async def _upload_image(self, ctx:ApplicationContext, path:str, emote_name: str, attachment:discord.Attachment):
        async with self.bot.db._async_session() as session: 
            result = await self.bot.db.getGuildEmoteEntry(ctx.guild, emote_name,session=session)

            print(result)
            if result:
                result.path = path
            else:
                emoteEntry = EmotesTable()
                emoteEntry.guild_id = ctx.guild_id
                emoteEntry.emote_name = emote_name
                emoteEntry.path = path
                print(emoteEntry)
                await self.bot.db.insert(emoteEntry)
        
        await attachment.save(pathlib.Path(path))
        file = await attachment.to_file()
        await ctx.author.send(f"The following image file has been set as a custom emote on {ctx.guild}",file=file)