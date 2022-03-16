from re import search
from src.database.Schema import BaseSchema, GuildSchema, NicknamesSchema, UserSchema
from src.database.BaseDataBase import BaseDataBase
from src.common.Settings import Settings
from src.logging.logger import Logger
import asyncio
import discord
from discord.guild import Guild
from discord import Member
from src.common import Utilities as utils
from typing import Any
import time
import pandas as pd

logger = Logger(__name__)


class DiscordDataBase(BaseDataBase):
    async def createNewMember(self, new_values: UserSchema):
        result = await self.setEntryValues(new_values.getTableName(), search_values=new_values)
        return result

    async def setMemberValues(self, member_values: dict | UserSchema, updated_values: dict[Any] | UserSchema) -> bool:
        member_values = member_values if not(isinstance(
            member_values, UserSchema)) else member_values.toDict()
        updated_values = updated_values if not(isinstance(
            updated_values, UserSchema)) else updated_values.toDict()
        success = await self.setEntryValues(UserSchema.getTableName(), search_values=member_values, updated_values=updated_values)
        return success

    async def setGuildValues(self, guild_values: dict | GuildSchema, updated_values: dict[Any] | GuildSchema) -> bool:
        guild_values = guild_values if not(isinstance(
            guild_values, GuildSchema)) else guild_values.toDict()
        updated_values = updated_values if not(isinstance(
            updated_values, GuildSchema)) else updated_values.toDict()
        success = await self.setEntryValues(GuildSchema.getTableName(), search_values=guild_values, updated_values=updated_values)
        return success

    async def getMemberNicknames(self, member_values: dict | UserSchema, number_of_nicknames: int = 5):
        columns = ['nickname', 'timestamp']
        if isinstance(member_values, BaseSchema):
            member_values = member_values.toDict()
        nickname_user = NicknamesSchema(table_dict=member_values)
        nickname_user.drop(columns)
        results = await self.select(tableName=NicknamesSchema.getTableName(), values_where=nickname_user.toDict(), columns=columns)
        df = pd.DataFrame(results.values, columns=results.keys())
        df.sort_values(by=columns[1], inplace=True, ascending=False)

        number_values = number_of_nicknames if len(
            df) > number_of_nicknames else len(df)

        output_string = f".\nNicknames for user: <@{nickname_user.user_id}>"
        output_string += "```"

        if number_values > 0:
            for i in range(number_values):
                output_string += f"\nOn {time.ctime(df.iloc[i][columns[1]])} {nickname_user.user_name}'s nickname was changed to {df.iloc[i][columns[0]]}"
        else:
            output_string += "\nNo recorded nicknames for this user"
        output_string += "```"
        return output_string

    async def _generateAudio(self, user:UserSchema|NicknamesSchema) -> str:
        user = user if isinstance(user, UserSchema) else UserSchema(table_dict=user.toDict())
        old_values = await self.getValues(user)
        old_values.fromDict(user.toDict())
        return self.audioGen.generateNickname(user)

    async def _updateUser(self, user: UserSchema, regen_audio: bool):
        nickname_info = NicknamesSchema(table_dict=user.toDict())
        if nickname_info.nickname is None:
            nickname_info.nickname = nickname_info.user_name
        nickname_info.setTime()

        if regen_audio:
           user.default_audio_path = await self._generateAudio(nickname_info)

        await self.setEntryValues(user.getTableName(), search_values=user.toSearch(), updated_values=user)
        await self.setEntryValues(nickname_info.getTableName(), search_values=nickname_info.toSearch(), updated_values=nickname_info)


    async def updateMember(self, member: discord.Member, regen_audio: bool):
        search_user = utils.memberToSchema(member=member)
        await self._updateUser(user=search_user, regen_audio=regen_audio)

    async def updateGuild(self, guild: discord.Guild, regen_audio: bool):
        result = True
        for member in guild.members:
            temp = await self.updateMember(member=member, regen_audio=regen_audio)
            result = temp if result else False  # if previous results were true, return temp
        return result

    async def updateAllGuilds(self, guilds: list[discord.Guild], regen_audio: bool):
        result = True
        for guild in guilds:
            temp = await self.updateGuild(guild=guild, regen_audio=regen_audio)
            result = temp if result else False  # if previous results were true, return temp
        return result

    async def getValues(self, user:BaseSchema):
        full_user = user.copy()
        results = await self.select(tableName=user.getTableName(), values_where=user.toSearch(), columns=user.allKeys())
        full_user.fromDict(results)
        return full_user

if __name__ == "__main__":
    Settings()

    async def main():
        path = Settings.get("SQLITE_DB")
        print(path)
        db = DiscordDataBase(path=path)
        await db._deleteAllTables()
        await db.init(settings=Settings.get("DATA_BASE"))
        await db.createNewMember(utils.getFakeMember())
      #  await db.setMemberCustomAudio(utils.getFakeMember(), 0.827)
        await db.close()
    asyncio.run(main())
