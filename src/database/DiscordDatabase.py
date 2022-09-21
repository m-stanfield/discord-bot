import asyncio
import os
import re
from ast import For
from contextlib import asynccontextmanager, contextmanager
from enum import unique

import discord
import sqlalchemy
from gtts import gTTS
from sqlalchemy import (Boolean, Column, Float, ForeignKey, Index, Integer,
                        String, UniqueConstraint, text)
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.orm import (Session, declarative_base, relationship,
                            sessionmaker)
from src.database.BaseDatabase import BaseDataBase
from src.database.schema import (GUILD_TABLE, NICKNAME_TABLE, SETTING_TABLE,
                                 USER_TABLE, Base, GuildsTable, NicknamesTable, SettingsTable,
                                 UsersTable, EmotesTable)
from src.Settings import Settings
from src.logger import Logger

REGEX = re.compile('[^a-zA-Z]')
logger = Logger(__name__)

class DiscordDatabase(BaseDataBase):

    async def addMember(self, member:discord.Member, session:Session|None=None):
        user:UsersTable = await self.getUserEntry(member=member, session=session)
        if user is None:
            user = UsersTable.memberToEntry(member)
            await self.insert(user)

        settings:SettingsTable = await self.getSettingEntry(member=member, session=session)
        if settings is None:
            settings = SettingsTable.memberToEntry(member)
            await self.insert(settings)
        user = await self.getUserEntry(member=member, session=session)
        settings = await self.getSettingEntry(member=member, session=session)
        return user, settings


    async def updateMember(self, member:discord.Member, previous_member:discord.Member|None = None, regenerate_audio:bool = False):
        session:Session
        if member is None:
            return

        if previous_member is not None and member.display_name != previous_member.display_name:
            nickname:NicknamesTable = NicknamesTable.memberToEntry(member=member)
            await self.insert(nickname)
            
        async with self._async_session() as session: 
            user:UsersTable = await self.getUserEntry(member=member, session=session)
            setting:SettingsTable = await self.getSettingEntry(member=member, session=session)


            if user is None or setting is None:
                user, setting = await self.addMember(member=member, session=session)

            user.user_name = member.name

            setting.display_name = member.display_name
            await session.commit()

            audio_file = await self.getUserAudioFile(member, False)
            if audio_file is None or regenerate_audio:
                await self.generateMemberAudio(member)

    async def updateAllGuilds(self, guilds:list[discord.Guild], regenerate_audio: bool = False):
        guild:discord.Guild
        for guild in guilds:
            if guild is not None:
                await self.updateEntireGuild(guild = guild, regenerate_audio = regenerate_audio)


    async def updateEntireGuild(self, guild:discord.Guild, regenerate_audio: bool = False):
        member:discord.Member
        for member in guild.members:
            if member is not None:
                await self.updateMember(member=member, regenerate_audio=regenerate_audio)

    async def getSettingEntry(self, member:discord.Member, session:Session|None=None):
        stmt = select(SettingsTable).where(SettingsTable.user_id == member.id, SettingsTable.guild_id == member.guild.id)
        return await self.execute(stmt, session)

    async def getUserEntry(self, member:discord.Member, session:Session|None=None):
        stmt = select(UsersTable).where(UsersTable.user_id == member.id)
        return await self.execute(stmt, session)

    async def getGuildEntry(self, guild:discord.Guild, session:Session|None=None):
        stmt = select(GuildsTable).where(GuildsTable.guild_id == guild.id)
        return await self.execute(stmt, session)

    async def getGuildEmoteEntry(self, guild:discord.Guild, image_name:str, session:Session|None=None):
        stmt = select(EmotesTable).where(EmotesTable.guild_id == guild.id, EmotesTable.emote_name == image_name )
        return await self.execute(stmt, session)

    async def getAllGuildEmoteEntries(self, guild:discord.Guild, session:Session|None=None):
        stmt = select(EmotesTable).where(EmotesTable.guild_id == guild.id)
        return await self.execute(stmt, session)

    async def getNicknameEntry(self, member:discord.Member, session:Session|None=None):
        stmt = select(NicknamesTable).where(NicknamesTable.user_id == member.id, NicknamesTable.guild_id == member.guild.id)
        return await self.execute(stmt, session)

    async def getNicknameEntries(self, member:discord.Member, number_of_entries:int=None):
        stmt = select(NicknamesTable).where(NicknamesTable.user_id == member.id, NicknamesTable.guild_id == member.guild.id).order_by(NicknamesTable.time.desc())
        result = await self.execute(stmt)
        if not(isinstance(result, list)):
            result = [result]
        return result if result is None or number_of_entries is None or isinstance(result, NicknamesTable) or len(result) < number_of_entries  else result[:number_of_entries]

    async def generateMemberAudio(self, member:discord.Member) -> bool:
        nickname = REGEX.sub("", member.display_name)
        filename = self._generateMP3Name(member)
        path = os.path.join(Settings.get(['data','audio','nicknames']), filename)

        ttsSuccessful = self._generateTTS(text=nickname, path=path)
        result_str = "successful" if ttsSuccessful else "failed" 
        if ttsSuccessful:
            logger.info("Generation of new member audio for nickname %s was %s for user %s in guild %s at file %s"%(nickname,result_str, member.name, member.guild.name,filename))
        else:
            logger.info("Generation of new member audio for nickname %s was %s for user %s in guild %s at file %s"%(nickname, result_str, member.name, member.guild.name,filename))
        return ttsSuccessful

    async def getUserAudioFile(self, member:discord.Member, custom_audio:bool=False):
        if custom_audio:
            logger.info("Attemping to load custom audio")
            base_path = Settings.get(['data','audio','custom'])
        else:
            logger.info("Attemping to load nickname audio")
            base_path = Settings.get(['data','audio','nicknames']) 
        path = os.path.join(base_path, self._generateMP3Name(member))

        if custom_audio and not(os.path.isfile(path)):
            logger.info(f"Failed to load custom audio as {path} is not a file")
            path = await self.getUserAudioFile(member=member, custom_audio=False)
        return path if path is not None and os.path.isfile(path) else None

    def generateAndGetSayClip(self, text:str, lang:str = "en") -> str:
        base_path = Settings.get(['data','audio','sayin'])
        full_path = os.path.join(base_path, "say_in.mp3")
        logger.info(f"Attempting to generate audio file to say {text} in language {lang} at {full_path}")

        successful = self._generateTTS(text = text, path = full_path, lang = lang )
        if successful:
            logger.info(f"Audio File Stored at {full_path}")

            return full_path
        else:
            logger.warning(f"Failed to save audio file at {full_path}")
            return None



    def _generateMP3Name(self, member:discord.Member) -> str:
        return f"guild{member.guild.id}_member{member.id}.mp3"

    def _generateTTS(self, text:str, path:str, lang:str='en') -> bool:
        if os.path.isfile(path):
            os.remove(path)
        try:
            myobj = gTTS(text=text,lang=lang,slow=False)
            myobj.save(path)
            successful = os.path.isfile(path)
        except Exception as err:
            logger.critical("Error in _generateTTS call: " + err)
            successful = False
        return successful

if __name__ == "__main__":
    async def main():
        db = await DiscordDatabase.initialize_database(Settings.get(['data','database']))
        class Guild:
            id = 134
            name = "test guild name"
        class Member:
            id = 10
            user_id = 3178913
            name = "test name"
            display_name = "test nickname"
            guild = Guild()
        await db.addMember(Member())
        await db.generateMemberAudio(Member())
        await db.updateMember(Member())
    asyncio.run(main())
