from typing import overload
from src.database.BaseDataBase import BaseDataBase
from src.common.Settings import Settings
import asyncio
import discord
from discord.guild import Guild
from discord import Member
from src.common import Utilities as utils


USER_TABLE = 'user'


class DiscordDataBase(BaseDataBase):
    async def createNewMember(self,member_dict:dict):
        user_settings =    {"guild_name":member_dict["guild_name"], 
                            "guild_id":member_dict["guild_id"],
                            "user_id":member_dict["user_id"], 
                            "user_name":member_dict["user_name"]}

        print(user_settings)
        user_exists = await self.checkIfEntryExists(USER_TABLE,user_settings)
        print(user_exists)
        if not(user_exists):
            await self.insert(table=USER_TABLE,values=user_settings|{"nickname":member_dict['nick'],"default_nickname":member_dict['name']})
        
        user_exists = await self.checkIfEntryExists(USER_TABLE,user_settings)
        return user_exists

    async def setCustomAudio(self, member_dict:dict, value:int) -> None:
        user_exists = await self.checkIfEntryExists(USER_TABLE,**member_dict)
        if not(user_exists):
            await self.createNewMember(member_dict=member_dict)
        USER_ID_COLUMN = 'user_id'
        GUILD_ID_COLUMN = 'guild_id'
        
        values_where = {USER_ID_COLUMN:member_dict['user_id'],GUILD_ID_COLUMN:member_dict['guild_id']}
        updated_values = {'custom_audio':value}
        self.update(tableName=USER_TABLE,values_where=values_where,updated_values=updated_values)
        
        



        

if __name__ == "__main__":
    Settings()
    async def main():
        path = Settings.get("SQLITE_DB")
        print(path)
        db = DiscordDataBase(path=path)
        await db._deleteAllTables()
        await db.init(settings=Settings.get("DATA_BASE"))
        await db.createNewMember(utils.getFakeMember())
        await db.setCustomAudio(utils.getFakeMember(),0.827)
        await db.close()
    asyncio.run(main())

