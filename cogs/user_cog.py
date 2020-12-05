from discord.ext import commands
import numpy as np
import os
import sys
sys.path.append('functions')
import discord
import profile_fun as pf

class users(commands.Cog):
    def __init__(self, bot):
        print('Cog Loaded: users')
        self.bot = bot
        
    @commands.command()
    @commands.is_owner()
    async def create_superuser(self,ctx, playerID=None, value=True):
        '''Promotes user to superuser. Only usable by bot owner'''
        member = pf.find_member(ctx.author.guild,ctx,playerID)
        await self.set_value(ctx.author.guild,member,'superuser',bool(value))
        
    @commands.command()  
    async def reset_profile(self,ctx):
        '''Resets all profile settings to defaults a given server'''

        dic = {'user_name':member.name,'guild_name':member.guild.name}
        print('Reseting profile for {user_name} in {guild_name}'.format(**dic))
        member = await self.find_supermember(ctx,playerID)
        await self.delete_user(ctx.guild,member)
        await self.generate_user(ctx.guild,member)
        
    @commands.command()  
    async def test_update(self,ctx):
        await self.bot.db.execute("UPDATE users SET default_nickname = 'changed name' WHERE guild_id = %d AND user_id = %d;"%(ctx.guild.id,ctx.author.id))
    
    @commands.command()
    async def default_nickname(self, ctx, nickname, playerID=None):
        '''Sets default nickname of users. !default_nickname "<nickname>" @<mention>. @<mention> only works for superusers'''
        member = await self.find_supermember(ctx,playerID)
        oldNickname = await self.pull_value(ctx.author.guild,member,'default_nickname')
        await self.set_value(ctx.author.guild,member,'default_nickname',nickname)
        await ctx.send('Default Nickname set from %s to %s for %s'%(oldNickname,nickname,member.name))    
    
    @commands.command()
    async def reset_nickname(self, ctx, playerID=None):
        '''Resets nickname of users to default value. !reset_nickname @<mention>. @<mention> only works for superusers'''

        member = await self.find_supermember(ctx,playerID)
        print(member,type(member))
        oldNickname = await self.pull_value(ctx.author.guild,member,'default_nickname')
        await member.edit(nick=str(oldNickname))
        await ctx.send('Nickname reset to %s for %s'%(oldNickname,member.name))
    @commands.command()
    async def volume(self, ctx,volume: float,playerID=None):
        '''Sets volume of users to included value. !volume <value> @<mention>. @<mention> only works for superusers'''

        member = await self.find_supermember(ctx,playerID)
        oldVolume = await self.pull_value(ctx.author.guild,member,'volume')
        await self.set_value(ctx.author.guild,member,'volume',volume)
        await ctx.send('Volume set from %0.3f to %0.3f for %s'%(oldVolume,volume,member.name))
           
    @commands.command()
    async def custom_audio(self, ctx,custom_audio: float,playerID=None):
        '''Sets rate of playing custom audio intro of users to included value. !custom_audio <value> @<mention>. @<mention> only works for superusers'''

        member = await self.find_supermember(ctx,playerID)
        oldcustom_audio = await self.pull_value(ctx.author.guild,member,'custom_audio')
        await self.set_value(ctx.author.guild,member,'custom_audio',custom_audio)
        await ctx.send('custom_audio set from %0.2f to %0.2f for %s'%(oldcustom_audio,custom_audio,member.name))
        
    @commands.command()
    async def length(self, ctx,length: float,playerID=None):
        '''Sets length of custom audio intro of users to included value. !length <value> @<mention>. @<mention> only works for superusers'''

        member = await self.find_supermember(ctx,playerID)
        oldLength = await self.pull_value(ctx.author.guild,member,'length')
        superuser = await self.check_super(ctx.author.guild,member)
        #print(length)
        if not(superuser):
            length = np.min((length,3.0))    
        await self.set_value(ctx.author.guild,member,'length',length)
        await ctx.send('Length set from %0.3f to %0.3f for %s'%(oldLength,length,member.name))
        
    @commands.command()
    async def solo_play(self,ctx,playerID=None):
        '''Sets if intro plays if only user on voice channel. !solo_play <value> @<mention>. @<mention> only works for superusers'''

        member = await self.find_supermember(ctx,playerID)
        val = await self.pull_value(ctx.author.guild,member,'solo_play')
        await self.set_value(ctx.author.guild,member,'solo_play',val==0)
        
    @commands.command()
    async def unify_settings(self,ctx,playerID=None):
        '''Sets all other server settings to current servers settings. !unify_settings @<mention>. @<mention> only works for superusers'''

        member = await self.find_supermember(ctx,playerID)

        mainRow = await self.bot.db.fetchrow("SELECT * FROM users WHERE guild_id = %d AND user_id = %d"%(ctx.author.guild.id,member.id))

        allRow = await self.bot.db.fetch("SELECT * FROM users WHERE user_id = %d"%(member.id))

        for row in allRow:
            for key in dict(row):
                if key not in ('id','guild_name','guild_id','user_id','user_name','superuser','ban','ban_count'):
                    guild = discord.utils.find(lambda g: g.id == row['guild_id'],self.bot.guilds)
                    await self.set_value(guild,member,key,mainRow[key])

            
    @commands.command()
    async def settings(self,ctx,playerID=None):
        '''Sends settings for current server. !settings @<mention>. @<mention> only works for superusers'''

        member = await self.find_supermember(ctx,playerID)
        settings = await self.pull_user(ctx.author.guild,member)
        string = '```\nSettings for %s on %s\n'%(member.name,ctx.author.guild)
        maxKey = 0
        for key in dict(settings):
            curKey = len(key)
            
            if curKey > maxKey:
                maxKey = curKey
                
        for key in dict(settings):
            curKey = len(key)
            string += ' '*(maxKey-curKey) + key + ':  ' + str(settings[key]) + '\n'
        string += '```'
        
        await ctx.author.send(string)
        #await self.set_value(ctx.author.guild,member,'solo_play',val==0)
        
    async def check_super(self,guild,member):
        return await self.pull_value(guild,member,'superuser')
        
    async def set_value(self,guild,member,key,value):
        dic = {'guild_id':guild.id,'user_id':member.id,'key':key,'value':value,'user_name':member.name,'guild_name':guild.name}
        print('Set {key} for {user_name} in {guild_name} to {value}'.format(**dic))
        if type(dic['value']) == str:
            await self.bot.db.execute("UPDATE users SET {key} = '{value}' WHERE guild_id = {guild_id} AND user_id = {user_id};".format(**dic))
        else:
            await self.bot.db.execute("UPDATE users SET {key} = {value} WHERE guild_id = {guild_id} AND user_id = {user_id};".format(**dic))

    async def pull_value(self,guild,member,key):
        testRow = await self.bot.db.fetchval("SELECT %s FROM users WHERE guild_id = %d AND user_id = %d"%(key,guild.id,member.id))
        return testRow
        
    async def pull_user(self,guild,member):
        testRow = await self.bot.db.fetchrow("SELECT * FROM users WHERE guild_id = %d AND user_id = %d"%(guild.id,member.id))

        return testRow
        
    async def delete_user(self,guild,member):
        await self.bot.db.execute("DELETE FROM users WHERE user_id = %d AND guild_id = %d;"%(member.id,guild.id))

    async def generate_user(self,guild,member):
        print('Adding User %s to Guild %s'%(member.name,guild.name))

        await self.bot.db.execute("INSERT INTO users (guild_name, guild_id,user_id,user_name) VALUES ('%s', %d, %d, '%s');"%(guild.name,guild.id,member.id,member.name))

    async def check_member(self,guild,member):
        # TODO: Code to update individual profile 
        #       in a specific guild.
        #       Needs to add any new settings while
        #       not affecting existing settings
        testRow = await self.bot.db.fetch("SELECT * FROM users WHERE guild_id = %d AND user_id = %d"%(guild.id,member.id))
        if len(testRow) == 0:
            await self.generate_user(guild,member)       

    async def check_guild(self,guild):
        for member in guild.members:
            await self.check_member(guild,member) 

    async def check_all(self,guild_list):
        for guild in guild_list:
            await self.check_guild(guild)
            
    async def find_supermember(self,ctx,playerID):
        supercheck = await self.check_super(ctx.author.guild,ctx.author)
        
        if supercheck:
            member = pf.find_member(ctx.author.guild,ctx,playerID)
        else:
            member = pf.find_member(ctx.author.guild,ctx,None)
        return member

    def load_defaults(self, directory=None):
        if directory == None:
            path = 'user_defaults.ini'
        else:
            path = directory + '/user_defaults.ini'

        if os.path.exists(path):
            with open(path,'r') as f:
                content = f.readlines()
            
            
            content = [x.strip().replace('\t','').replace(' ','')  for x in content] 
            dic = {}
            for line in content:
                if len(line) > 0:
                    a = line.split('=')
                    varname = a[0]
                    vartype = a[1].split(':')[0]
                    varval = a[1].split(':')[1]
                    


                    if vartype == 'BOOL':
                        dic[a[0]] = ('BOOL',bool(int(varval)))
                    elif vartype == 'TEXT':
                        dic[a[0]] = ('TEXT',varval.replace('"',"'"))
                    elif vartype == 'FLOAT':
                        dic[a[0]] = ('FLOAT',float(varval))
                    elif vartype == 'BIGINT':
                        dic[a[0]] = ('BIGINT',int(varval))
                    else:
                        try:
                            dic[a[0]] = ('BIGINT',int(varval))
                        except ValueError:
                            dic[a[0]] = ('TEXT',str(varval))
                    
            return dic
        else:
            return {}    
        
