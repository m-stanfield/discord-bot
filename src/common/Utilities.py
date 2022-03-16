import discord
from discord.ext.commands.context import Context
from src.database.Schema import UserSchema, GuildSchema, NicknamesSchema
from typing import Any
from src.logging.logger import Logger
import numpy as np
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


def memberToSchema(member: discord.Member | None = None, **kwargs) -> UserSchema:
    member_dict = {}
    if member is not None:
        member_dict = {"guild_name": member.guild.name,
                       "guild_id": member.guild.id,
                       "user_id": member.id,
                       "user_name": member.name,
                       "nickname": member.nick}
    kwargs = dict([v for v in kwargs.items() if v[0] in member_keys])
    member_dict = member_dict | kwargs
    return UserSchema(table_dict=member_dict)


def guildToDict(guild: discord.guild.Guild | None = None, **kwargs) -> GuildSchema:
    guild_dict = {}
    if guild is not None:
        guild_dict = {"guild_name": guild.name,
                      "guild_id": guild.id}
    kwargs = dict([v for v in kwargs.items() if v[0] in guild_keys])
    guild_dict = guild_dict | kwargs
    return GuildSchema(table_dict=guild_dict)


def ctxToDict(ctx: Context | None = None, **kwargs) -> dict[GuildSchema, UserSchema]:
    member = None if ctx is None else ctx.author
    guild = None if ctx is None else ctx.guild
    user_schema = memberToSchema(member=member, **kwargs)
    guild_schema = guildToDict(guild=guild, **kwargs)
    ctx_dict = {'author': user_schema, 'guild': guild_schema}
    return ctx_dict


def getFakeMember() -> UserSchema:
    return memberToSchema(guild_name='Faked Member Guild Name', guild_id='Faked Member Guild ID', id='Faked Member ID', name='Faked Member User Name')


def getFakeGuild() -> GuildSchema:
    return guildToDict(guild_name='Faked Member Guild Name', guild_id='Faked Member Guild ID')


def getFakeCtx() -> dict[GuildSchema, UserSchema]:
    member = getFakeMember()
    guild = getFakeGuild()
    combined_dict = member | guild
    return ctxToDict(**combined_dict)


def roll_dice(args):
    """Inputs: Dice roll represented in terms of XdY+AxB-Z"""
    # await ctx.message.delete()
    # loading dic string from args
    diceString = ''
    for ele in args:
        diceString += ele

    def diceRoller(diceString):
        # rolls dice of single type(ie 5d6 rolls 5 six sided dice)

        a = diceString.split('d')
        numDice = int(a[0])
        diceSize = int(a[1])

        roll = np.random.randint(1, diceSize+1, numDice)
        diceInfo = {}
        diceInfo['size'] = diceSize
        diceInfo['number'] = numDice
        return roll, diceInfo

    # formatting string to enable parsing
    # parsing works by removing spaces, spliting on + signs, the spliting on - signs
    # everything in first layer of splitstr adds together.
    # eerything in second layer of splitstr gets subtracted
    diceString = diceString.replace(' ', '')
    splitstr = diceString.split('+')
    for ii in range(len(splitstr)):
        splitstr[ii] = splitstr[ii].split('-')
    output = ''
    result = 0

    # enumerating over all of splitstings and strings contined by it
    for ii, dicelist in enumerate(splitstr):
        for jj, dicestring in enumerate(dicelist):
            # if 'd' exists send string to be rolled.
            # othewise its constant and just add it to the roll
            if dicestring.find('d') != -1:
                roll, diceInfo = diceRoller(dicestring)
            else:
                roll = np.array([int(dicestring)])
                diceInfo = None

            # Adds roll to roll total and builds output string based on results
            if jj == 0:
                result += np.sum(roll)
                if ii == 0:
                    for kk, num in enumerate(roll):
                        if kk == 0:
                            output += '(%d' % num
                        else:
                            output += ' + %d' % num
                    output += ')'

                else:
                    for kk, num in enumerate(roll):
                        if kk == 0:
                            output += ' + (%d' % num
                        else:
                            output += ' + %d' % num
                    output += ')'

            else:
                result -= np.sum(roll)
                if ii == 0:
                    for kk, num in enumerate(roll):
                        if kk == 0:
                            output += '(%d' % num
                        else:
                            output += ' + %d' % num
                    output += ')'

                else:
                    for kk, num in enumerate(roll):
                        if kk == 0:
                            output += ' - (%d' % num
                        else:
                            output += ' + %d' % num
                    output += ')'
            if diceInfo is not None:
                output += f"[{diceInfo['number']}d{diceInfo['size']}]"
    return 'Total: %d    Breakdown: %s' % (result, output)


if __name__ == "__main__":
    print(getFakeMember())
    print(getFakeGuild())
    print(getFakeCtx())
    print(roll_dice("5d20+181+3d3+10d100"))
