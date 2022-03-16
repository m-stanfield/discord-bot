import discord
from discord.ext.commands import Bot
import asyncio


from src.logging.logger import Logger
from src.database.BaseDataBase import BaseDataBase
from src.database.DiscordDataBase import DiscordDataBase
from src.common.Settings import Settings

# cogs
from src.cogs.BaseCog import BaseCog
from src.cogs.ListenerCog import ListenerCog
from src.cogs.OwnerCog import OwnerCog
from src.cogs.ReactRoleCog import ReactRoleCog

import time
logger = Logger(__name__)


class DiscordBot(Bot):

    DEFAULT_KWARGS = {'description': "default description",
                      "command_prefix": "!", "intents": None}

    def __init__(self, **kwargs):
        kwargs = {**self.DEFAULT_KWARGS, **kwargs}
        if kwargs['intents'] is None:
            kwargs['intents'] = discord.Intents.all()

        super().__init__(
            description=kwargs.pop("description"),
            command_prefix=kwargs.pop("command_prefix"),
            intents=kwargs.pop("intents")
        )

        db: BaseDataBase = None if "db" not in kwargs else kwargs.pop('db')
        if not(isinstance(db, BaseDataBase)):
            path = Settings.get(
                "SQLITE_DB") if "SQLITE_DB" not in kwargs else kwargs.pop("SQLITE_DB")
            db = DiscordDataBase(path=path)
        self.db = db

        #adding all cogs to the bot
        self.add_cog(BaseCog(self))
        self.add_cog(ListenerCog(self))
        self.add_cog(OwnerCog(self))
        self.add_cog(ReactRoleCog(self))

        self.run_status = True

    async def close(self):
        await self.db.close()
        await super().close()

    async def run(self):
        await self.db.init()

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

    async def playAudio(self, channel:discord.VoiceChannel, file_name:str, volume:float=0.1, length:float=3):
        logger.debug(f"Attempting to play audio file {file_name} with volume {volume} and length {length} on channel {channel.name} on {channel.guild.name}")

        if self.voice_clients == []:
            logger.info(f"Playing")
            voice = await channel.connect(timeout=1.0)
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(file_name),volume=volume)
            voice.play(source,after=lambda e: logger.info('player error: %s' %e) if e else None)
            await asyncio.sleep(length)
            await voice.disconnect()   
            logger.info(f"Attempting to play audio file {file_name} with volume {volume} and length {length} on channel {channel.name} on {channel.guild.name}")
        else:
            logger.debug(f"Could not play audio due to a different connection already existing.")



    async def disconnect_timeout(self, timeout:float=10.0,interval:float=0.5):
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
            logger.info(f"Bot did not disconnet from discord after {timeout} seconds and timed out")
        return disconnected