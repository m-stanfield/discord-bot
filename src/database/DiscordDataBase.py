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
                            "user_id":member_dict["id"], 
                            "user_name":member_dict["name"]}

        print(user_settings)
        user_exists = await self.checkIfEntryExists(USER_TABLE,user_settings)
        print(user_exists)
        if not(user_exists):
            await self.insert(table=USER_TABLE,values=user_settings|{"nickname":member_dict['nick'],"default_nickname":member_dict['name']})
        
        user_exists = await self.checkIfEntryExists(USER_TABLE,user_settings)
        return user_exists

    

        

if __name__ == "__main__":
    Settings()
    async def main():
        path = Settings.get("SQLITE_DB")
        print(path)
        db = DiscordDataBase(path=path)
        await db._deleteAllTables()
        await db.init(settings=Settings.get("DATA_BASE"))
        await db.createNewMember(utils.memberToDict(guild_name='Guild Namea',guild_id='Guild ID', id='User ID', name='Name',nick='NickName'))
        await db.close()
    asyncio.run(main())

