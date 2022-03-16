import unittest
import time
from src.database.Schema import BaseSchema, GuildSchema, NicknamesSchema, PyToSQLConverter, UserSchema, SCHEMA_DICT
from src.database.DiscordDataBase import DiscordDataBase


class Wrapper:
    class BaseSchema_tests(unittest.IsolatedAsyncioTestCase):

        def __init__(self, *arg, schema: BaseSchema, **kwargs):
            super().__init__(*arg, **kwargs)
            self._schema: BaseSchema = schema

        async def init_db(self, db_path: str = 'src/tests/database/test_schema.db') -> DiscordDataBase:
            db = DiscordDataBase(path=db_path)
            await db._deleteAllTables()
            await db.init()
            return db

        def test_inheritance(self):
            schema: BaseSchema = self._schema()
            assert isinstance(schema, BaseSchema)

        async def test_dbload(self):
            db = await self.init_db()
            assert isinstance(db, DiscordDataBase)

        def test_tableName(self):
            schema: BaseSchema = self._schema()
            tableName = type(schema).__name__.replace("Schema", "").lower()
            assert tableName in SCHEMA_DICT.keys()
            assert tableName == schema.getTableName()

        async def test_toSearch(self):
            db = await self.init_db()
            schema: BaseSchema = self._schema()
            schema.guild_id = 1
            schema.user_id = 2
            schema.guild_name = "test_name"
            schema_exists = await db.checkIfEntryExists(schema.getTableName(), schema.toDict())
            assert not(schema_exists)
            entry_exists = await db.setEntryValues(schema.getTableName(), search_values=schema.toSearch(), updated_values=schema.toDict())
            schema_exists = await db.checkIfEntryExists(schema.getTableName(), schema.toDict())
            assert entry_exists and schema_exists

        async def test_PyToSQLConverter(self):
            assert PyToSQLConverter('string') == ("TEXT", 'string')
            assert PyToSQLConverter("'string'") == ("TEXT", "'string'")
            assert PyToSQLConverter('1.0') == ("TEXT", '1.0')
            assert PyToSQLConverter(1.0) == ("REAL", 1.0)
            assert PyToSQLConverter(1) == ("INTEGER", 1)
            assert PyToSQLConverter(None) == ("BLOB", None)



class UserSchema_tests(Wrapper.BaseSchema_tests):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, schema=UserSchema, **kwargs)


class GuildSchema_tests(Wrapper.BaseSchema_tests):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, schema=GuildSchema, **kwargs)


class NicknamesSchema_tests(Wrapper.BaseSchema_tests):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, schema=NicknamesSchema, **kwargs)

    def test_timestamp(self):
        current_time = time.time()
        schema: NicknamesSchema = self._schema(reset=False)
        assert schema.timestamp == -1
        schema.setTime()
        assert schema.timestamp >= current_time

    def test_setTimestamp(self):
        timestamp = 10
        schema: NicknamesSchema = self._schema(
            table_dict={'timestamp': timestamp})
        print(schema.timestamp, timestamp, 'timestamp')
        assert schema.timestamp == timestamp


if __name__ == "__main__":
    unittest.main()
