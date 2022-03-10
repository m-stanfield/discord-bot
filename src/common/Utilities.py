import discord

def memberToDict(member:discord.Member|None=None,**kwargs):
    member_dict = {}
    if member is not None:
        member_dict = {"guild_name":member.guild.name, 
                        "guild_id":member.guild.id,
                        "user_id":member.id, 
                        "user_name":member.name}
    member_dict = member_dict | kwargs
    return kwargs