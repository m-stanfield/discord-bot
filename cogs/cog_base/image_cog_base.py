from discord.ext import commands
import os
import discord
import sys

sys.path.append('functions')
import profile_fun as pf

class images(commands.Cog):
    def __init__(self, bot):
        print('Cog Loaded: images')
        self.bot = bot
        

    async def post_image(self,ctx,fileName):
        if os.path.isfile(fileName):
            #print(ctx.message.content)
            try:
                await ctx.message.delete()
            except discord.errors.Forbidden:
                print('Message could not be deleted:Forbidden Error')
            #print(ctx.message.content)
            await ctx.send(f'From: {ctx.author.display_name}',file=discord.File(fileName)) 
