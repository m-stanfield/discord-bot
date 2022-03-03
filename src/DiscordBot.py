import discord
import asyncio
from src.database.DataBase import DataBase
from src.misc.Settings import Settings

from src.logging.logger import Logger

from src.cogs.cog_generators.image_cog_gen import generate_images
generate_images()

from src.cogs.base_cog import base
from src.cogs.audio_cog import audio
from src.cogs.image_cog import images
from src.cogs.user_cog import users
from src.cogs.guild_cog import guilds
from src.cogs.general_cog import general

import src.functions.profile_fun as pf
logger = Logger(__name__)

Settings.init()
class DiscordBot(discord.ext.commands.Bot):

    DEFAULT_KWARGS = {'description':"default description","command_prefix":"!","intents":None}
    def __init__(self, **kwargs):
        kwargs = {**self.DEFAULT_KWARGS,**kwargs}
        if kwargs['intents'] is None:
            kwargs['intents'] = discord.Intents.all()

        super().__init__(
            description=kwargs.pop("description"),
            command_prefix=kwargs.pop("command_prefix"),
            intents=kwargs.pop("intents")
        )

        db:DataBase = None if "db" not in kwargs else kwargs.pop('db')
        print(db)
        if not(isinstance(db,DataBase)):
            db = DataBase(path=Settings.get('SQLITE_DB'))
        self.db = db
        self.add_cog(base(self))
        self.add_cog(users(self))
        self.add_cog(general(self))
        self.add_cog(audio(self))
        self.add_cog(images(self))
        self.add_cog(guilds(self))

    
    async def run(self):
        try:
            await self.start(Settings.get("DISCORD_TOKEN"))
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt: Exiting Program")
            await self.db.close()
            await self.logout()
            



if __name__ == "__main__":
    async def main():
        print(Settings.get('SQLITE_DB'))
        bot = DiscordBot(SQLITE_DB=Settings.get('SQLITE_DB'))

        await bot.run()

    asyncio.run(main())
    
