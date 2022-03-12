import discord
from discord.ext.commands.context import Context
from typing import Any
from src.logging.logger import Logger

logger = Logger(__name__)


"""
author <class 'discord.Member'>
guild <class 'discord.guild.Guild'>
ctx <class 'discord.ext.commands.context.Context'>
"""

guild_keys = ['guild_name', 'guild_id']
member_keys = ['guild_name', 'guild_id', 'id', 'name']


def memberToMentionString(member: discord.Member | dict) -> str:
    if isinstance(member, discord.Member):
        user_id = member.id
    elif isinstance(member, dict):
        user_id = member['id']
    else:
        logger.error(
            f"Invalid member object, can not create mention from member {str(member)}.")
        return ""
    return f"<@{user_id}>"


def memberToDict(member: discord.Member | None = None, **kwargs) -> dict[Any]:
    member_dict = {}
    if member is not None:
        member_dict = {"guild_name": member.guild.name,
                       "guild_id": member.guild.id,
                       "id": member.id,
                       "name": member.name,
                       "nickname": member.nick}
    kwargs = dict([v for v in kwargs.items() if v[0] in member_keys])
    member_dict = member_dict | kwargs
    print(dict)
    return member_dict


def guildToDict(guild: discord.guild.Guild | None = None, **kwargs) -> dict[Any]:
    guild_dict = {}
    if guild is not None:
        guild_dict = {"guild_name": guild.name,
                      "guild_id": guild.id}
    kwargs = dict([v for v in kwargs.items() if v[0] in guild_keys])
    guild_dict = guild_dict | kwargs
    return guild_dict


def ctxToDict(ctx: Context | None = None, **kwargs) -> dict[Any]:
    member = None if ctx is None else ctx.author
    guild = None if ctx is None else ctx.guild
    member_dict = memberToDict(member=member, **kwargs)
    guild_dict = guildToDict(guild=guild, **kwargs)
    ctx_dict = {'author': member_dict, 'guild': guild_dict}
    return ctx_dict


def getFakeMember() -> dict[Any]:
    return memberToDict(guild_name='Faked Member Guild Name', guild_id='Faked Member Guild ID', id='Faked Member ID', name='Faked Member User Name')


def getFakeGuild() -> dict[Any]:
    return guildToDict(guild_name='Faked Member Guild Name', guild_id='Faked Member Guild ID')


def getFakeCtx() -> dict[Any]:
    member = getFakeMember()
    guild = getFakeGuild()
    combined_dict = member | guild
    return ctxToDict(**combined_dict)


if __name__ == "__main__":
    print(getFakeMember())
    print(getFakeGuild())
    print(getFakeCtx())
