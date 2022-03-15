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
USER_TABLE = 'user'

logger = Logger(__name__)

class DiscordDataBase(BaseDataBase):
    async def createNewMember(self, new_values: UserSchema):
        result = await self.setEntryValues(new_values.getTableName(),search_values=new_values)
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
        columns = ['nickname','timestamp']
        if isinstance(member_values, BaseSchema):
            member_values = member_values.toDict() 
        nickname_user = NicknamesSchema(table_dict = member_values)
        nickname_user.drop(columns)
        results = await self.select(tableName=NicknamesSchema.getTableName(), values_where=nickname_user.toDict(), columns=columns)
        df = pd.DataFrame(results,columns=columns)
        df.sort_values(by=columns[1],inplace=True, ascending=False)
        
        number_values = number_of_nicknames if len(df) > number_of_nicknames else len(df)

        output_string = f".\nNicknames for user: <@{nickname_user.user_id}>"
        output_string += "```"

        if number_values > 0:
            for i in range(number_values):
                output_string += f"\nOn {time.ctime(df.iloc[i][columns[1]])} {nickname_user.user_name}'s nickname was changed to {df.iloc[i][columns[0]]}"
        else:
            output_string += "\nNo recorded nicknames for this user"
        output_string += "```"
        return output_string

    async def _updateNickname(self, before:discord.Member, after:discord.Member):
         if before.display_name != after.display_name:
            search_user = utils.memberToSchema(member=after)
            nickname_info = NicknamesSchema(table_dict=search_user.toDict())
            if nickname_info.nickname is None:
                nickname_info.nickname = nickname_info.user_name
            nickname_info.setTime()
            search_info = nickname_info.copy()
            search_info.drop(['nickname'])
            await self.setEntryValues(nickname_info.getTableName(),search_values=search_info,updated_values=nickname_info)


    async def updateUserInformation(self, before:discord.Member, after:discord.Member):
        # TODO: Generalize to discord.User
       await self._updateNickname(before, after)




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
