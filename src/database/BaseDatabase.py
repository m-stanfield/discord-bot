from ast import For
from contextlib import contextmanager, asynccontextmanager
from enum import unique
from src.logger import Logger
import sqlalchemy
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint, ForeignKey, Index, Float
import os
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine
from src.database.schema import Base, USER_TABLE, GUILD_TABLE, SETTING_TABLE, NICKNAME_TABLE, GuildsTable, UsersTable, NicknamesTable, SettingsTable

logger = Logger(__name__)


class BaseDataBase:
    _engine:sqlalchemy.engine.Engine|None = None
    _async_session = None


    @classmethod
    async def initialize_database(cls, database_path:str='memory', database_name:str|None="database.db"):
        if cls._engine is None:

            if database_path == "memory":
                database_loc = ":memory:"
            else:
                database_loc = os.path.join(database_path, database_name)
                if not(os.path.isdir(database_path)):
                    os.mkdir(database_path)
            databaseExists = os.path.exists(database_loc)
            cls._engine: sqlalchemy.engine.Engine = create_async_engine(f'sqlite+aiosqlite:///{database_loc}')
            if not(databaseExists):
                async with cls._engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)
            cls._async_session = sessionmaker(cls._engine, expire_on_commit=False, class_=AsyncSession)        
        return cls()

    async def insert(self, row, session:Session|None=None):
        if row is None:
            return
            
        rows = row if type(row) == list else [row]

        if session:
            async with session.begin():
                session.add_all(rows)
        else:
            async with self._async_session() as session:  
                async with session.begin():
                    session.add_all(rows)

    async def getTable(self, table):
        async with self._async_session() as session:
            stmt = select(table)
            result = await self.execute(stmt=stmt, session=session)
        return result


    async def execute(self, stmt:str, session:Session|None = None):
        if session:
            sql_results = await session.execute(stmt)
        else:
            async with self._async_session() as session:  
                sql_results = await session.execute(stmt)
        results = []
        for row in sql_results:
            results.append(row)
        return self._clean_result(results)

    def _clean_result(self, result):
        if result is None or len(result) < 1:
            return None
        elif len(result) == 1:
            return result[0][0]
        elif len(result) > 1:
            return result
        
        return None

    async def close(self):
        logger.info(f"Attempting to close database")
        await self._engine.dispose()
        logger.info(f"Database was successfully closed")

        