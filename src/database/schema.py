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

logger = Logger(__name__)
Base = declarative_base()
USER_TABLE = 'Users'
GUILD_TABLE = 'Guilds'
SETTING_TABLE = 'Settings'
NICKNAME_TABLE = 'Nicknames'


class Users(Base):
    __tablename__ = USER_TABLE

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, unique=True)

    def __repr__(self):
        return f"<{USER_TABLE}(id={self.id}, user_id={self.user_id})>"

class Nicknames(Base):
    __tablename__ = NICKNAME_TABLE

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(f"{USER_TABLE}.user_id"), nullable=False, )
    guild_id = Column(Integer, ForeignKey(f"{GUILD_TABLE}.guild_id"), nullable=False)
    nickname = Column(String)
    time = Column(Float, nullable=False)

    user_relationship = relationship(USER_TABLE, primaryjoin=f"and_({USER_TABLE}.user_id == {__tablename__}.user_id)")
    guild_relationship = relationship(GUILD_TABLE, primaryjoin=f"and_({GUILD_TABLE}.guild_id == {__tablename__}.guild_id)")

    def __repr__(self):
        return f"<{NICKNAME_TABLE}(id={self.id}, user_id={self.user_id}, nickname={self.nickname}, time={self.time})>"



class Guilds(Base):
    __tablename__ = GUILD_TABLE

    id = Column(Integer, primary_key=True)
    guild_id = Column(Integer, nullable=False, unique=True)
    guild_name = Column(String, nullable=False)
    audio_enabled = Column(Boolean, nullable=False, default=True)
    custom_audio_enabled = Column(Boolean, nullable=False, default=True)
    say_enabled = Column(Boolean, nullable=False, default=True)
    inspire_enabled = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<{GUILD_TABLE}(id={self.id}, guild_id={self.guild_id}, guild_name={self.guild_name}, audio_enabled={self.audio_enabled}, custom_audio_enabled={self.custom_audio_enabled},say_enabled={self.say_enabled}, inspire_enabled={self.inspire_enabled})>"


class Settings(Base):
    __tablename__ = SETTING_TABLE

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(
        f"{USER_TABLE}.user_id"), nullable=False)
    guild_id = Column(Integer, ForeignKey(
        f"{GUILD_TABLE}.guild_id"), nullable=False)
    nickname = Column(String, default=None)
    volume = Column(Float, nullable=False, default=0.3)
    length = Column(Float, nullable=False, default=3.0)
    superuser = Column(Boolean, nullable=False, default=False)
    banned = Column(Boolean, nullable=False, default=False)
    banned_count = Column(Integer, nullable=False, default=0)
    custom_audio_relative_frequency = Column(
        Float, nullable=False, default=0.5)
    logging_enabled = Column(Boolean, nullable=False, default=False)
    solo_audio_play = Column(Boolean, nullable=False, default=True)
    audio_enabled = Column(Boolean, nullable=False, default=True)
    unique_id_1 = UniqueConstraint("user_id", "guild_id")

    user_relationship = relationship(USER_TABLE, primaryjoin=f"and_({USER_TABLE}.user_id == {__tablename__}.user_id)")
    guild_relationship = relationship(GUILD_TABLE, primaryjoin=f"and_({GUILD_TABLE}.guild_id == {__tablename__}.guild_id)")

    def __repr__(self):
        return f"<{SETTING_TABLE}(id={self.id}, user_id={self.user_id}, guild_id={self.guild_id})>"


if __name__ == "__main__":
    async def main():
        from src.database.DiscordDatabase import DiscordDatabase

        class FakeGuild:
            def __init__(self, **kwargs):
                self.id = kwargs.pop("id",10)
            def __str__(self):
                output = ""
                for key, item in self.__dict__.items():
                    if not(key.startswith("_")):
                        output += f"\n<{key}: {str(item)}>"
                return output

        class FakedMember:
            def __init__(self, **kwargs):
                self.id = kwargs.pop("id",10)
                self.guild:FakeGuild = kwargs.pop("guild", None)
            def __str__(self):
                output = ""
                for key, item in self.__dict__.items():
                    if not(key.startswith("_")):
                        output += f"\n<{key}: {str(item)}>"
                return output
            
        db = await DiscordDatabase.initialize_database()
        print(db._async_session)
        fake_member = FakedMember(guild=FakeGuild(id=34))
        user: Users = Users(user_id=fake_member.id)
        guild: Guilds = Guilds(id=138, guild_id=fake_member.guild.id, guild_name="abcd")
        setting: Settings = Settings(user_id=fake_member.id, guild_id=fake_member.guild.id)

        print(user)
        print(guild)
        print(setting)

        # an Engine, which the Session will use for connection
        # resources

        # create session and add objects
        
        await db.insert([user, guild])
        max_iter = 5
        for i in range(max_iter):
            for j in range(max_iter):
                user_id = fake_member.id+i-2
                guild_id = fake_member.guild.id+j-2
                setting: Settings = Settings(user_id=user_id, guild_id=guild_id)
                t = i*max_iter + j 
                nickname:Nicknames = Nicknames(user_id=fake_member.id, guild_id=fake_member.guild.id, nickname="abcd"+str(t),time=t)
                await db.insert([nickname])
        for table in [Users, Guilds, Settings, Nicknames]:
            result = await db.getTable(table)
            print(table.__tablename__)
            for a in result:
                print(a)

        #stmt = select(Users).where(Users.user_id == 14)
       # result = await db.execute(stmt)
        #print(result)
        stmt = select(Settings)
        print(stmt)
        result = await db.execute(stmt)
        print(result)


        result = await db.getSettingEntry(fake_member)
        print(result)
        result = await db.getUserEntry(fake_member)
        print(result)            
        result = await db.getGuildEntry(fake_member.guild)
        print(result)          
        result = await db.getNicknameEntries(fake_member, number_of_entries=3)
        print(result)   
        print(fake_member)

    asyncio.run(main())