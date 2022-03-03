from src.logging.logger import Logger
from src.misc.Settings import Settings
import asyncio
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine
logger = Logger(__name__)
Settings.init()

class DataBase:
    #DEFAULT_KWARGS = {'path':':memory:'}#
    DEFAULT_KWARGS = {'path': 'data/database/discord_bot.db','schema_path':'settings/database/schema'}
    db:Engine|None = None

    def __init__(self, **kwargs):
        self._kwargs = {**self.DEFAULT_KWARGS, **kwargs}
        if self.db is None:
            self.db = create_async_engine("sqlite+aiosqlite:///"+self._kwargs['path'])
            logger.info(f"Data has been loaded from : {self._kwargs['path']}")

    async def close(self):
        logger.info(f"Attempting to close database")
        await self.db.dispose()
        logger.info(f"Database was successfully closed")


    async def execute(self, command, args=None):
        logger.info(f"SQL Command: {command}")
        print(command)
        async with self.db.begin() as conn:
            result = await conn.execute(text(command))

         #   if result.rowcount < 1:
            return result
           # else:
           #     return result.all()
 
    async def select(self, cmdstr):
        result = await self.execute(cmdstr)
        result = result.all()

        logger.info(result)
        if len(result) > 0:
            result = result[0]
        logger.info(result)
        if len(result) == 1:
            result = result[0]
        return result

    async def createTable(self, tableName, columns, column_types=None, column_defaults=None):
        # schema_list is tuple/list of tuples/lists of keyword/datatype pairs
        # so ((user_name, text))
        if column_types is not None and not(len(columns) == len(column_types)):
            errormsg = "Column name and type arrays need to have the same length"
            logger.error(errormsg)
            raise ValueError(errormsg)

        if column_defaults is not None and not(len(columns) == len(column_defaults)):
            errormsg = "Column name and s arrays need to have the same length"
            logger.error(errormsg)
            raise ValueError(errormsg)

        # generate command string for creating a table
        cmdstr = f"CREATE TABLE if not exists {tableName} ("
        for i in range(len(columns)):
            # for first element, skip the column
            if i > 0:
                cmdstr += ", "

            # write ? to position the column name
            cmdstr += f"{columns[i]}"

            # if column datatype is given, add ? for its position
            if column_types is not None:
                cmdstr += f" {column_types[i]}"

            if column_defaults is not None:
                cmdstr += f" DEFAULT {column_defaults[i]}"
        cmdstr += ")"

        await self.execute(cmdstr)
        return True

    async def insert(self, table: str, columns: list, values: list) -> bool:
        if not(len(columns) == len(values)):
            return False

        cmdstr = f"INSERT INTO {table}("

        for idx, elem in enumerate(columns):
            if not(idx == 0):
                cmdstr += ", "
            cmdstr += elem
        cmdstr += ") VALUES ("

        for idx, elem in enumerate(values):
            if idx > 0:
                cmdstr += ", "
            if type(elem) is str:
                cmdstr += f'"{elem}"'
            else:
                cmdstr += str(elem)
        cmdstr += ")"

        await self.execute(cmdstr)


        return True


    async def init(self):
        db_settings = Settings.get('DATA_BASE')
        print(db_settings)
        for key in db_settings:
            columns = []
            column_types = []
            column_defaults = []
            for elemName,(elemType, elemDefault) in db_settings[key].items():
                columns.append(elemName)
                column_types.append(elemType)
                column_defaults.append(elemDefault)
                print(key,elemName, elemDefault,elemType)
            print(key)
            await self.createTable(key.lower(), columns, column_types=column_types, column_defaults=column_defaults)



if __name__ == "__main__":
    Settings()
    async def main():
        db = DataBase()
        await db.init()
        await db.insert('users',['id'],[1])
        result = await db.select('users',['id'])
        await db.close()
        print(result)
    asyncio.run(main())
