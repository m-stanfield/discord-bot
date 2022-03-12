import discord
from discord.ext.commands import Bot

import src.logging.logger as Logger
from src.database.BaseDataBase import BaseDataBase
from src.database.DiscordDataBase import DiscordDataBase
from src.common.Settings import Settings
import src.cogs.OwnerCommands as OwnerCommands


logger = Logger.Logger(__name__)


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
        self.add_cog(OwnerCommands.OwnerCommands(self))

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

    def getRunStatus(self):
        return self.run_status


