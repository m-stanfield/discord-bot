from discord.ext import commands
import os
import sys
import inspirobot
import src.functions.profile_fun as pf
import discord
import logging
from discord.commands import slash_command


logger = logging.getLogger(__name__)

class general(commands.Cog):
    def __init__(self, bot):
        logger.info('Cog Loaded: general')
        self.bot = bot

    @slash_command()
    async def inspire(self, ctx):
        await ctx.respond(inspirobot.generate().url)

    @slash_command()
    async def roll(self,ctx,*args):
        '''Rolls dice. !roll <dice string>. Dice string exmaple: 1d20 -4d2 + 8 -2d2'''
        await ctx.respond(pf.roll_dice(args))


    @slash_command()
    async def nicknames(self,ctx,member: discord.Member=None,length:float=5):
        '''Displays users past nicknames on server.'''

        '''
        Inputs
        ------
        playerID
            Member ID from @mention in a chat. Optoinal value.

        length (int)
            length of list generated.

        '''
       # await ctx.message.delete()

        directory='logs/nicknames/'
        users = self.bot.get_cog('users')
        #checking if user is superuser and can change other users settings
        member = await users.find_supermember(ctx,member)

        #building message strings from file
        message = '~~~~~\n'
        message += 'Nicknames for '+member.name + ' on Server ' + ctx.guild.name + '\n'
        fileName = directory+ member.name.replace(' ','_') +'_nicknames_'+ctx.guild.name.replace(' ','_') + '.dat'
        if os.path.exists(fileName):
            with open(fileName,'r') as f:
                lines = f.readlines()
                if len(lines) < length:
                    length = len(lines)

                for ii in range(length):
                    splitline = lines[-(ii+1)].replace('\n','').split('\t')

                    message += splitline[0] + '\t' + splitline[2] +'\n'
            await ctx.respond(message)
