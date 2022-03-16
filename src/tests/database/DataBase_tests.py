from lib2to3.pytree import Base
import unittest
import asyncio
from src.database.DiscordDataBase import DiscordDataBase

from src.database.BaseDataBase import BaseDataBase
from src.database.Schema import UserSchema, SCHEMA_DICT


class BaseDataBase_tests(unittest.IsolatedAsyncioTestCase):
    TEST_DATABASE = 'src/tests/database/test.db'
    TEST_SCHEMA = {'table_one': {"test_INTEGER": ('INTEGER', 1), "test_TEXT": ("TEXT", 'abcd'), "test_REAL": ("REAL", 3.14159), "test_BLOB": ("BLOB", 1.28187138)},
                   'table_two': {"test_INTEGER": ('INTEGER', 10), "test_TEXT": ("TEXT", 'dcba'), "test_REAL": ("REAL", 1.183), "test_BLOB": ("BLOB", "TEXTBLOB")}}

    def __init__(self, *args, database: BaseDataBase | None = None, **kwargs):
        self.database: BaseDataBase = database if database is not None else BaseDataBase
        super().__init__(*args, **kwargs)

    async def test_Init(self):
        db: BaseDataBase = self.database(path=self.TEST_DATABASE)
        await db._deleteAllTables()
        await db.init(settings=self.TEST_SCHEMA)

        for table in self.TEST_SCHEMA.keys():
            result = await db.getColumnNames(table)
            assert set(result) == set(self.TEST_SCHEMA[table])
        await db._deleteAllTables()

    async def test_getColumnNames(self):
        db: BaseDataBase = self.database(path=self.TEST_DATABASE)
        await db._deleteAllTables()
        await db.init(settings=self.TEST_SCHEMA)
        for key in self.TEST_SCHEMA:
            columns = await db.getColumnNames(key)
            assert set(columns) == set(self.TEST_SCHEMA[key])
        await db._deleteAllTables()

    async def test_InvalidColumnInsert(self):
        db: BaseDataBase = self.database(path=self.TEST_DATABASE)
        await db._deleteAllTables()
        await db.init(settings=self.TEST_SCHEMA)

        insert1 = {'aaaatest_INTEGER': 10831, 'test_TEXT': "test_text"}
        result = await db.insert('table_one', insert1)
        assert result == False
        await db._deleteAllTables()

    async def test_ValidColumnInsert(self):
        db: BaseDataBase = self.database(path=self.TEST_DATABASE)
        await db._deleteAllTables()
        await db.init(settings=self.TEST_SCHEMA)

        insert1 = {'test_INTEGER': 10831, 'test_TEXT': "test_text"}
        selection = await db.select(tableName='table_one', values_where=insert1)
        result = await db.insert('table_one', insert1)
        selection = await db.select(tableName='table_one', values_where=insert1)

        assert result != False
        await db._deleteAllTables()

    async def test_buildSelectString(self):

        db: BaseDataBase = self.database(path=self.TEST_DATABASE)
        await db._deleteAllTables()
        await db.init(settings=self.TEST_SCHEMA)

        cmdstr = db._buildSelectString(
            'table_one', {'test_INTEGER': 1, 'test_TEXT': 'abcd'})
        target_cmd = "SELECT * FROM table_one WHERE test_INTEGER = 1 AND test_TEXT = 'abcd'"
        assert cmdstr == target_cmd

        cmdstr = db._buildSelectString(
            'table_one', {'test_INTEGER': 1, 'test_TEXT': 'abcd'}, columns=['test_INTEGER'])
        target_cmd = "SELECT test_INTEGER FROM table_one WHERE test_INTEGER = 1 AND test_TEXT = 'abcd'"
        assert cmdstr == target_cmd
        await db._deleteAllTables()

    async def test_buildInsertString(self):

        db: BaseDataBase = self.database(path=self.TEST_DATABASE)
        await db._deleteAllTables()
        await db.init(settings=self.TEST_SCHEMA)

        cmdstr = db._buildInsertString(
            'table_one', {'test_INTEGER': 1, 'test_TEXT': 'abcd'})
        target_cmd = "INSERT INTO table_one (test_INTEGER, test_TEXT) VALUES (1, 'abcd')"
        assert cmdstr == target_cmd
        await db._deleteAllTables()

    async def test_checkIfEntryExists(self):
        db: BaseDataBase = self.database(path=self.TEST_DATABASE)
        await db._deleteAllTables()
        await db.init(settings=self.TEST_SCHEMA)
        table = list(self.TEST_SCHEMA.keys())[0]
        schema = dict(self.TEST_SCHEMA[table])

        for key in schema:
            val = schema[key][1]
            if type(val) is int or type(val) is float:
                val = val*2
            elif type(val) is str:
                val = 'inserted entry'
            schema[key] = val

        for key, val in schema.items():
            result = await db.checkIfEntryExists(tableName=table, values={key: val})
            assert result == False
        result = await db.checkIfEntryExists(tableName=table, values=schema)
        assert result == False
        insert = await db.insert(table=table, values=schema)
        result = await db.checkIfEntryExists(tableName=table, values=schema)
        assert result == True

        for key, val in schema.items():
            result = await db.checkIfEntryExists(tableName=table, values={key: val})
            assert result == True
        await db._deleteAllTables()

    async def test_SchemaInit(self):
        db: BaseDataBase = self.database(path=self.TEST_DATABASE)
        await db._deleteAllTables()
        await db.init()
        tables = await db.getTableNames()
        assert set(tables) == set(SCHEMA_DICT.keys())
        for table in set(tables):
            columns = await db.getColumnNames(tableName=table)
            assert set(columns) == set(SCHEMA_DICT[table])

    async def test_setEntryValues(self):

        db: BaseDataBase = self.database(path=self.TEST_DATABASE)
        await db._deleteAllTables()
        await db.init()
        user = UserSchema()
        user.user_id = 178937428979
        user.guild_id = 184387172189
        user.ban = 1
        user.default_nickname = "updated uesr default nick name"
        entryExists = await db.checkIfEntryExists(UserSchema.getTableName(), user.toDict())
        assert entryExists == False
        await db.setEntryValues(tableName=UserSchema.getTableName(), search_values=user.toSearch(), updated_values=user.toDict())
        entryExists = await db.checkIfEntryExists(UserSchema.getTableName(), user.toDict())
        assert entryExists == True


class DiscordDataBase_tests(BaseDataBase_tests):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, database=DiscordDataBase, **kwargs)

    async def test_Test(self):
        pass


if __name__ == "__main__":
    unittest.main()

    async def main():
        db = BaseDataBase(path=BaseDataBase_tests.TEST_DATABASE)
        await db.init()
        await db._deleteAllTables()
        await db.close()
    # asyncio.run(main())
