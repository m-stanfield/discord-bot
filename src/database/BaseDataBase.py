from src.logging.logger import Logger
from src.common.Settings import Settings
import asyncio
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine
from typing import Any
logger = Logger(__name__)
Settings.init()

# TODO:
#   1) Add ability to edit cells on conditions, UPDATE sql command
#       

class BaseDataBase:
    #DEFAULT_KWARGS = {'path':':memory:'}#
    DEFAULT_KWARGS = {'path': 'data/database/discord_bot.db'}
    db:Engine|None = None

    def __init__(self, **kwargs):
        self._kwargs = {**self.DEFAULT_KWARGS, **kwargs}
        self._schema:dict[list[str]] = {}
        if self.db is None:
            self.db = create_async_engine("sqlite+aiosqlite:///"+self._kwargs['path'])
            logger.info(f"Data has been loaded from : {self._kwargs['path']}")


    async def close(self):
        logger.info(f"Attempting to close database")
        await self.db.dispose()
        logger.info(f"Database was successfully closed")

    async def delete(self, tableName:str):
        if tableName in self._schema:
            self._schema.pop(tableName)
            cmdstr = f"DROP TABLE {tableName}"
            await self.execute(cmdstr)
            result = True
        else:
            result = False        
        return result
    
    async def _deleteTables(self, tableList:list[str]):
        for table in tableList:
            await self.delete(table)


    async def _deleteAllTables(self):
        keys = await self.getTableNames()
        print('keys: ',keys)
        if len(keys) > 0:
            print('keys: ',keys)

            await self._deleteTables(keys)
        self._schema = {}


    async def _clearAllTables(self):
        keys = await self.getTableNames()



    async def getTableNames(self) -> list[str]:
        cmdstr = "SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';"
        exe_output = await self.execute(command=cmdstr)
        results = []
        for exe_tuple in exe_output.all():
            results.append(exe_tuple[0])
        return results


    async def execute(self, command, args=None):
        logger.info(f"SQL Command: {command}")
        async with self.db.begin() as conn:
            result = await conn.execute(text(command))
            return result

 
    async def select(self, tableName:str, values_where:dict[Any]|None=None,columns:list[str]|None=None)-> list[Any]:
        cmdstr = self._buildSelectString(columns=columns, tableName=tableName, values_where=values_where)
        result = await self.execute(cmdstr)
        result = result.all()
        return result

    def _buildSelectString(self, tableName:str, values_where:dict[Any]|None=None,columns:list[str]|None=None) -> str:
        cmdstr = f"SELECT "
        if columns is None:
            cmdstr += "*"
        else:
            for i, column in enumerate(columns):
                if i > 0:
                    cmdstr += ", "
                cmdstr += column
            
            
        cmdstr += f" FROM {tableName}"
        if values_where is not None:
            cmdstr += " WHERE "
            for idx, (column, value) in enumerate(values_where.items()):
                if not(idx == 0):
                    cmdstr += " AND "
                cmdstr += f"{column} = "
                if type(value) is str:
                    cmdstr += f"'{value}'"
                else:
                    cmdstr += f"{value}"
        return cmdstr

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

        current_table = await self.getTableNames()
        table_did_not_exists = tableName not in current_table
        print('table_did_not_exists',table_did_not_exists)
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

        result = await self.execute(cmdstr)

        table_columns = await self.getColumnNames(tableName=tableName)
        self._schema[tableName] = list(table_columns)

        if table_did_not_exists:
            values = dict(zip(columns,column_defaults))
            await self.insert(table=tableName,values=values)
        return True

    def _buildInsertString(self, table:str, values:dict[str]) -> str:
        cmdstr = f"INSERT INTO {table} ("

        for idx, elem in enumerate(values.keys()):
            if not(idx == 0):
                cmdstr += ", "
            cmdstr += elem
        cmdstr += ") VALUES ("

        for idx, elem in enumerate(values.values()):
            if idx > 0:
                cmdstr += ", "
            if type(elem) is str:
                cmdstr += f"'{elem}'"
            else:
                cmdstr += str(elem)
        cmdstr += ")"
        return cmdstr

    async def insert(self, table: str, values:dict[str]) -> bool:
        if not(set(values.keys()).issubset(set(self._schema[table]))):
            return False
        cmdstr = self._buildInsertString(table=table, values=values)
        result = await self.execute(cmdstr)
        return result


    async def init(self, settings:dict[str,tuple[str,Any]]|None = None, **kwargs):
        db_settings = settings if settings is not None else Settings.get('DATA_BASE')
        for key in db_settings:
            columns = []
            column_types = []
            column_defaults = []
            for elemName,(elemType, elemDefault) in db_settings[key].items():
                columns.append(elemName)
                column_types.append(elemType)
                column_defaults.append(elemDefault)
            await self.createTable(key.lower(), columns, column_types=column_types, column_defaults=column_defaults)

    async def getColumnNames(self,tableName):
        result = await self.execute(f"SELECT * FROM {tableName}")
        return list(result.keys())

    async def checkIfEntryExists(self, tableName:str, values:dict[Any]):
        result = await self.select(tableName=tableName, values_where=values)
        return len(result) > 0

    async def update(self, tableName:str, values_where:dict[Any], updated_values:dict[Any]):
        cmdstr = self._updateEntryString(tableName=tableName, values_where=values_where, updated_values=updated_values)
        print(cmdstr)
        result = await self.execute(cmdstr)
        return result


    def _updateEntryString(self, tableName:str, values_where:dict[Any], updated_values:list[str]):
        cmdstr = f"UPDATE {tableName} SET"
        first_entry = True
        for column, value in updated_values.items():
            if not(first_entry):
                cmdstr += ","
            else:
                first_entry = False
            if type(value) is str:
                cmdstr += f" {column} = '{value}'"

            else:
                cmdstr += f" {column} = {value}"
        cmdstr += " WHERE"
        first_entry = True

        for column, value in values_where.items():
            if not(first_entry):
                cmdstr += " AND "
            else:
                first_entry = False

            if type(value) is str:
                cmdstr += f" {column} = '{value}'"

            else:
                cmdstr += f" {column} = {value}"

        return cmdstr
        


if __name__ == "__main__":
    Settings()
    async def main():
        TEST_SCHEMA = {'table_one':{"test_INTEGER":('INTEGER',1),"test_TEXT":("TEXT",'abcd'),"test_REAL":("REAL",3.14159),"test_BLOB":("BLOB",1.28187138)}, 
                            'table_two':{"test_INTEGER":('INTEGER',10),"test_TEXT":("TEXT",'dcba'),"test_REAL":("REAL",1.183),"test_BLOB":("BLOB","TEXTBLOB")}}
        db = BaseDataBase(path='src/tests/database/test.db',settings=TEST_SCHEMA)
        await db.init(settings=TEST_SCHEMA)

        await db._deleteAllTables()

        await db.init(settings=TEST_SCHEMA)
        for i in range(10):
            await db.insert('table_one',{"test_INTEGER":100})

        await db.insert('table_one',{"test_INTEGER":1346789326247819})
        await db.insert('table_one',{"test_INTEGER":100, 'test_TEXT':'test insert'})

        await db.update('table_one',values_where={'test_INTEGER':1346789326247819},updated_values={'test_INTEGER':-3})
        await db.update('table_one',values_where={'test_INTEGER':100,'test_TEXT':"test insert"},updated_values={'test_REAL':-1.17371})

        #await db.init(settings=TEST_SCHEMA)


        #await db.insert('table_one',{"test_INTEGER":100})

        await db.close()
    asyncio.run(main())
