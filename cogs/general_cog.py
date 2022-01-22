from discord.ext import commands
import os
import sys
import inspirobot
sys.path.append('functions')
import profile_fun as pf


class general(commands.Cog):
    def __init__(self, bot):
        print('Cog Loaded: general')
        self.bot = bot

    @commands.command()
    async def inspire(self, ctx, *args):
        await ctx.send(inspirobot.generate().url)
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            print("Message could not be deleted: Forbidden Error")

    @commands.command()
    async def roll(self,ctx,*args):
        '''Rolls dice. !roll <dice string>. Dice string exmaple: 1d20 -4d2 + 8 -2d2'''
        await ctx.send(pf.roll_dice(args))


    @commands.command()
    async def nicknames(self,ctx,playerID=None,length=5):
        '''Displays users past nicknames on server. !nicknames @<mention> <length>. @<mention> only works for superusers'''
        '''
        Inputs
        ------
        playerID
            Member ID from @mention in a chat. Optoinal value.

        length (int)
            length of list generated.

        '''
        await ctx.message.delete()

        directory='logs/nicknames/'
        users = self.bot.get_cog('users')
        #checking if user is superuser and can change other users settings
        member = await users.find_supermember(ctx,playerID)

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
            await ctx.send(message)
