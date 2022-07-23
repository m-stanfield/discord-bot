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
from src.database.schema import Base, USER_TABLE, GUILD_TABLE, SETTING_TABLE, NICKNAME_TABLE, Guilds, Users, Nicknames, Settings
from src.database.BaseDatabase import BaseDataBase
import discord
logger = Logger(__name__)

class DiscordDatabase(BaseDataBase):

    async def updateMember(self, member:discord.Member):
        member_id = member.id
        guild_id = member.guild.id
        user:Users = await self.getUserEntry(member=member)
        setting:Settings = await self.getSettingEntry(member=member)

    async def getSettingEntry(self, member:discord.Member):
        stmt = select(Settings).where(Settings.user_id == member.id, Settings.guild_id == member.guild.id)
        async with self._async_session() as session:  
            result = await self.execute(session, stmt)
        return result

    async def getUserEntry(self, member:discord.Member):
        stmt = select(Users).where(Users.user_id == member.id)
        async with self._async_session() as session:  
            result = await self.execute(session, stmt)
        return result

    async def getGuildEntry(self, guild:discord.Guild):
        stmt = select(Guilds).where(Guilds.guild_id == guild.id)
        async with self._async_session() as session:  
            result = await self.execute(session, stmt)
        return result

    async def getNicknameEntries(self, member:discord.Member, number_of_entries:int=None):
        stmt = select(Nicknames).where(Nicknames.user_id == member.id, Nicknames.guild_id == member.guild.id).order_by(Nicknames.time.desc())
        print(stmt)
        async with self._async_session() as session:  
            result = await self.execute(session, stmt)
        return result if result is None or number_of_entries is None or len(result) < number_of_entries  else result[:number_of_entries]





if __name__ == "__main__":
    pass
