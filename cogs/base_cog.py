from discord.ext import commands
import discord
import sys
import os
print(os.getcwd())
sys.path.append('functions')
import profile_fun as pf
from datetime import datetime
#from profile_fun import *

import asyncio
class base(commands.Cog):
    #Base function mainly interact through listeners and responding to server events.
    #Functions responding to messasges/user inputs will go into the more specific cogs.
    def __init__(self,bot):
        print('Cog Loaded: base')
        self.bot = bot


    @commands.command()
    @commands.is_owner()
    async def shutdown(self,ctx):
        '''Shuts bot down. Only usable by bot owner'''
        users = self.bot.get_cog('users')
        superuser = await users.pull_value(ctx.author.guild,ctx.author,'superuser')
        if superuser:
            await self.bot.logout()




    @commands.Cog.listener()
    async def on_voice_state_update(self,member: discord.Member, before,after):
        users = self.bot.get_cog('users')
        audio = self.bot.get_cog('audio')

        volume = await users.pull_value(member.guild,member,'volume')
        length = await users.pull_value(member.guild,member,'length')
        custom_audio = await users.pull_value(member.guild,member,'custom_audio')
        solo_play = await users.pull_value(member.guild,member,'solo_play')
        audio_enabled = await users.pull_value(member.guild,member,'audio_enabled')

        if audio_enabled:
            if not(after.channel == None) and not(after.channel == before.channel) and not(member.name == 'Mr. O') and self.bot.voice_clients == []:
                await audio.user_audio(channel=after.channel,member=member,volume=volume,length=length,custom_audio=custom_audio,solo_play=solo_play)


    
    
    @commands.Cog.listener()
    async def on_message(self, message):
        guild = message.guild

        # TODO: Need to implement logging

        #lis

    @commands.Cog.listener()
    async def on_member_update(self,before,after):
        if before.display_name != after.display_name:
            now = datetime.now()
            timestr = now.strftime('%Y/%m/%d  %H:%M:%S')
            with open('logs/nicknames/' + after.name.replace(' ','_') + '_nicknames_' +after.guild.name.replace(' ','_') +'.dat','a') as f:
                f.write(timestr+'\t'+before.display_name + '\t' + after.display_name +'\n')
            # TODO: audio nickname update

            # TODO: append nickname log

            print('Generating Audio for %s to say %s'%(after.name,after.display_name))
            defaultfile = 'default_' + after.name +'_'+ str(after.id)+ '_'+ str(after.guild.id) +'.mp3'
                  
            audio = self.bot.get_cog('audio')
            audio.generate_audio(after.display_name,'audio/users/'+defaultfile)


    @commands.Cog.listener()
    async def on_member_join(self,member):
        users = self.bot.get_cog('users')
        await users.check_member(member.guild,member)
        
    @commands.Cog.listener()
    async def on_ready(self):
        on_ready_message = 'Logged in as {0} ({0.id})'.format(self.bot.user)
        print('-'*len(on_ready_message))
        print(on_ready_message)
        print('-'*len(on_ready_message))
        # TODO: check for users without a profile
        users = self.bot.get_cog('users')
        guilds = self.bot.get_cog('guilds')
        audio = self.bot.get_cog('audio')

        if users is not None:


            user_default = users.load_defaults(directory='settings')
            user_string = await self.build_table(table_name = 'users',settings = user_default)
            
        print('Done with users')
        if guilds is not None:
            guild_default = guilds.load_defaults(directory='settings')
            for guild in self.bot.guilds:
                print(guild.name)
                table_name = 'guild_' + str(guild.id)
            
                table_name = table_name.replace(' ','_')
                guild_string = await self.build_table(table_name = table_name,settings = guild_default)
                            
                for member in guild.members:
                    print('Generating Audio for %s to say %s'%(member.name,member.display_name))
                    defaultfile = 'default_' + member.name +'_'+ str(member.id)+ '_'+ str(member.guild.id) +'.mp3'
                    
                    audio.generate_audio(member.display_name,'audio/users/'+defaultfile)

        await users.check_all(self.bot.guilds)

            
        done_message = '                 Bot Loaded                 '
        print('-'*len(done_message))
        print(done_message)
        print('-'*len(done_message))       
        
           
     
    async def build_table(self,table_name,settings):
        db_string = "CREATE TABLE IF NOT EXISTS %s(id SERIAL"%table_name
        print('Building table: %s'%table_name)
        
        for key in settings.keys():
            db_string += ', %s %s DEFAULT %s'%(str(key),str(settings[key][0]),str(settings[key][1]))
        db_string += ');'
        await self.bot.db.execute(db_string)
        testRow = await self.bot.db.fetchrow("SELECT * FROM %s"%table_name)
        if testRow == None:
            await self.bot.db.execute("INSERT INTO %s DEFAULT VALUES;"%table_name)
            testRow = await self.bot.db.fetchrow("SELECT * FROM %s;"%table_name)
            await self.bot.db.execute("DELETE FROM %s WHERE id = 1;"%table_name)

        
        tableKeys = []
        for key in testRow.keys():
            tableKeys.append(key)
        for key in settings.keys():
            if not(key in tableKeys):
                print('Adding column %s to table %s'%(str(key),str(table_name)))
                await self.bot.db.execute("ALTER TABLE %s ADD %s %s DEFAULT %s"%(table_name,str(key),str(settings[key][0]),str(settings[key][1])))
