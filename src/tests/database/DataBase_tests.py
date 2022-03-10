import unittest
import asyncio

from src.database.DataBase import DataBase

class DataBase_tests(unittest.IsolatedAsyncioTestCase):
    TEST_DATABASE = 'src/tests/database/test.db'
    TEST_SCHEMA = {'table_one':{"test_INTEGER":('INTEGER',1),"test_TEXT":("TEXT",'abcd'),"test_REAL":("REAL",3.14159),"test_BLOB":("BLOB",1.28187138)}, 
                     'table_two':{"test_INTEGER":('INTEGER',10),"test_TEXT":("TEXT",'dcba'),"test_REAL":("REAL",1.183),"test_BLOB":("BLOB","TEXTBLOB")}}
    async def test_Init(self):
        db = DataBase(path=self.TEST_DATABASE)
        await db._deleteAllTables()
        await db.init(settings=self.TEST_SCHEMA)

        for table in self.TEST_SCHEMA.keys():
            result = await db.getColumnNames(table)
            assert set(result) == set(self.TEST_SCHEMA[table])

    async def test_getColumnNames(self):
        db = DataBase(path=self.TEST_DATABASE)
        await db._deleteAllTables()
        await db.init(settings=self.TEST_SCHEMA)  
        for key in self.TEST_SCHEMA:
            columns = await db.getColumnNames(key)
            assert set(columns) == set(self.TEST_SCHEMA[key])
                
    async def test_InvalidColumnInsert(self):
        db = DataBase(path=self.TEST_DATABASE)
        await db._deleteAllTables()
        await db.init(settings=self.TEST_SCHEMA)

        insert1 = {'aaaatest_INTEGER':10831, 'test_TEXT':"test_text"}
        result =  await db.insert('table_one',insert1)
        assert result == False

    async def test_ValidColumnInsert(self):
        db = DataBase(path=self.TEST_DATABASE)
        await db._deleteAllTables()
        await db.init(settings=self.TEST_SCHEMA)

        insert1 = {'test_INTEGER':10831, 'test_TEXT':"test_text"}
        selection = await db.select(tableName='table_one',values_where=insert1)
        result =  await db.insert('table_one',insert1)
        selection = await db.select(tableName='table_one',values_where=insert1)

        assert result != False

    async def test_buildSelectString(self):
        
        db = DataBase(path=self.TEST_DATABASE)
        await db._deleteAllTables()
        await db.init(settings=self.TEST_SCHEMA)

        cmdstr = db._buildSelectString('table_one',{'test_INTEGER':1,'test_TEXT':'abcd'})
        target_cmd = "SELECT * FROM table_one WHERE test_INTEGER = 1 AND test_TEXT = 'abcd'"
        assert cmdstr == target_cmd

        cmdstr = db._buildSelectString('table_one',{'test_INTEGER':1,'test_TEXT':'abcd'},columns=['test_INTEGER'])
        target_cmd = "SELECT test_INTEGER FROM table_one WHERE test_INTEGER = 1 AND test_TEXT = 'abcd'"
        assert cmdstr == target_cmd

    async def test_buildInsertString(self):
        
        db = DataBase(path=self.TEST_DATABASE)
        await db._deleteAllTables()
        await db.init(settings=self.TEST_SCHEMA)

        cmdstr = db._buildInsertString('table_one',{'test_INTEGER':1,'test_TEXT':'abcd'})
        target_cmd = "INSERT INTO table_one (test_INTEGER, test_TEXT) VALUES (1, 'abcd')"
        assert cmdstr == target_cmd



if __name__ == "__main__":
    unittest.main()
    async def main():
        db = DataBase(path=DataBase_tests.TEST_DATABASE)
        await db.init()
        await db._deleteAllTables()
        await db.close()
    asyncio.run(main())