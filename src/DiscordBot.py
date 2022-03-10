import discord
import asyncio
from src.database.BaseDataBase import BaseDataBase
from src.database.DiscordDataBase import DiscordDataBase
from src.common.Settings import Settings

from src.logging.logger import Logger


logger = Logger(__name__)

Settings.init()
class DiscordBot(discord.Bot):

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

        db:BaseDataBase = None if "db" not in kwargs else kwargs.pop('db')
        print(db)
        if not(isinstance(db,BaseDataBase)):
            path = Settings.get("SQLITE_DB") if "SQLITE_DB" not in kwargs else kwargs.pop("SQLITE_DB")
            db = DiscordDataBase(path=path)
        self.db = db


    
    async def run(self):
        await self.db.init()

        try:
            await self.start(Settings.get("DISCORD_TOKEN"))
        except KeyboardInterrupt:
            print('here')
            logger.info("KeyboardInterrupt: Exiting Program")
            await self.db.close()
            await self.close()
            



if __name__ == "__main__":
    async def main():
        print(Settings.get('SQLITE_DB'))
        bot = DiscordBot(SQLITE_DB=Settings.get('SQLITE_DB'))

        await bot.run()
    while True:
        asyncio.run(main())
    
