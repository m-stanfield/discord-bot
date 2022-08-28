from __future__ import annotations
import discord
from discord.ext.commands import Bot
import asyncio
from discord.ext import tasks, commands
from src.cogs import ListenerCog, BaseCog, AudioCog, AdminCog
from src.database import DiscordDatabase, SettingsTable
from src.logger import Logger
from src.Settings import Settings
import time
from typing import Callable
import discord
import numpy as np
import os
import inspect

logger = Logger(__name__)


class DiscordBot(Bot):

    DEFAULT_KWARGS = {'description': "default description",
                      "command_prefix": "!", "intents": None}

    def __init__(self, **kwargs):
        self.queue = asyncio.Queue()
        kwargs = {**self.DEFAULT_KWARGS, **kwargs}
        if kwargs['intents'] is None:
            kwargs['intents'] = discord.Intents.all()

        super().__init__(
            description=kwargs.pop("description"),
            command_prefix=kwargs.pop("command_prefix"),
            intents=kwargs.pop("intents")
        )


        # adding all cogs to the bot
        self.add_cog(BaseCog(self))
        self.add_cog(AdminCog(self))
        self.add_cog(ListenerCog(self))
        self.add_cog(AudioCog(self))
        self.connection_status = False
        self.run_status = True
        self.ready = False

        

    def setDatabase(self, db:DiscordDatabase):
        self.db = db

    @staticmethod
    async def initialize_bot(**kwargs) -> DiscordBot:

        db: DiscordDatabase = None if "db" not in kwargs else kwargs.pop('db')
        if not(isinstance(db, DiscordDatabase)):
            database_path =  kwargs.pop("SQLITE_DB_PATH", Settings.get("SQLITE_DB_PATH"))
            database_name =  kwargs.pop("SQLITE_DB_FILE", Settings.get("SQLITE_DB_FILE"))
            db = await DiscordDatabase.initialize_database(database_path=database_path,database_name=database_name)
        bot = DiscordBot(**kwargs)
        bot.setDatabase(db)
        return bot

    async def close(self):
        await self.db.close()
        await super().close()

    async def runBot(self):
        self.processQueue.start()
        try:
            await self.start(Settings.get("DISCORD_TOKEN"))
        except KeyboardInterrupt:
            print('here')
            logger.info("KeyboardInterrupt: Exiting Program")
            await self.db.close()
            await self.close()

    async def setRunStatus(self, status: bool):
        self.run_status = status

    async def getRunStatus(self):
        return self.run_status

    async def getConnectionStatus(self):
        return self.connection_status

    async def playUserAudio(self, channel: discord.VoiceChannel, member:discord.Member, custom_audio:bool|None = None, queued_time:float|None = None):
        settings:SettingsTable = await self.db.getSettingEntry(member)
        percent_chance = np.random.uniform(0, 1.0)


        use_custom_audio:bool = (percent_chance < settings.custom_audio_relative_frequency) if custom_audio is None else custom_audio
        log_string = f"Attemping to play a audio clip with custom_audio initially being {custom_audio} overriden to {use_custom_audio} with a relative frequency of {settings.custom_audio_relative_frequency}  and a rolled value of {percent_chance}."
        logger.info(log_string)
        file_name:str = await self.db.getUserAudioFile(member = member, custom_audio=use_custom_audio)
        if file_name is not None and os.path.isfile(file_name):

            await self.playAudio(channel, file_name=file_name, volume=settings.volume, length=settings.length, queued_time=queued_time)

    async def playAudio(self, channel: discord.VoiceChannel, file_name: str, volume: float = 0.1, length: float = 3, queued_time:float|None = None):
        logger.debug(
            f"Attempting to play audio file {file_name} with volume {volume} and length {length} on channel {channel.name} on {channel.guild.name}")
        runtime = time.time()
        max_delay = float(Settings.get("MAX_PLAY_DELAY"))
        within_allowed_time = (runtime - queued_time) < max_delay if queued_time else True

        if self.voice_clients == [] and within_allowed_time:
            logger.info(f"Attempting to play audio file {file_name} with volume {volume} and length {length} on channel {channel.name} on {channel.guild.name}")            
            voice = await channel.connect(timeout=1.0)
            source = discord.PCMVolumeTransformer(
                discord.FFmpegPCMAudio(file_name), volume=volume)
            voice.play(source, after=lambda e: logger.info(
                'player error: %s' % e) if e else None)
            await asyncio.sleep(length)
            await voice.disconnect()
            
        elif not(within_allowed_time):
            logger.info(f"Could not play audio file due to queued time ({queued_time}) and run time ({runtime}) being greater than the maximum allowed time ({max_delay}).")
        else:
            logger.debug(
                f"Could not play audio due to a different connection already existing.")

    async def disconnect_timeout(self, timeout: float = 10.0, interval: float = 0.5):
        start_time = time.time()/1000
        disconnected = False
        while (time.time()/1000 - start_time <= timeout):
            if self.is_closed():
                logger.info("Bot has disconnected from discord")
                disconnected = True
                break
            else:
                time.sleep(interval)
        if not(disconnected):
            logger.info(
                f"Bot did not disconnet from discord after {timeout} seconds and timed out")
        return disconnected
    
    async def addItemToQueue(self, item):
        await self.queue.put(item)

    async def addMethodToQueue(self, func:Callable, *args, **kwargs):
        if not(self.ready):
            return
        if 'kwargs' in kwargs:
            kwargs = kwargs.pop('kwargs') | kwargs
        item = (func, args, kwargs)
        logger.debug("Queuing: " + str(item))
        return await self.addItemToQueue(item)

    def findMemberInVoiceChannel(self, ctx:discord.ApplicationContext) -> discord.VoiceChannel:
        for channel in ctx.guild.voice_channels:
            for member in channel.members:
                if member==ctx.author:
                    return channel
        return None

    @tasks.loop(seconds=0.05)
    async def processQueue(self):
        try:
            if not(self.queue.empty()):

                items = self.queue.get()
                method, args, kwargs = await items
                if (inspect.iscoroutinefunction(method)):
                    try:
                        await method(*args, **kwargs)
                    except Exception as e:
                        logger.critical(e)
                else:
                    method(*args, **kwargs)
        except Exception as err:
            logger.error(err, raiseError=err)






