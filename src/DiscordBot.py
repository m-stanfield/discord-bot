import discord
import asyncio
from src.database.DataBase import DataBase
from src.misc.Settings import Settings

from src.logging.logger import Logger

logger = Logger(__name__)

SETTINGS = Settings()



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

        db:DataBase = None if "db" not in kwargs else kwargs.pop('db')
        print(db)
        if not(isinstance(db,DataBase)):
            db = DataBase(path=kwargs.get('SQLITE_DB'))
        self.db = db
    
    async def run(self):
        try:
            await self.start(SETTINGS.get("DISCORD_TOKEN"))
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt: Exiting Program")
            await self.db.close()
            await self.logout()
            



if __name__ == "__main__":
    async def main():
        print(SETTINGS.get('SQLITE_DB'))
        bot = DiscordBot(SQLITE_DB=SETTINGS.get('SQLITE_DB'))
        await bot.run()

    asyncio.run(main())
    