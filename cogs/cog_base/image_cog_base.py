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

    @commands.command()
    async def upload_image(self,ctx):
        users = self.bot.get_cog('users')
        superuser = await users.check_super(ctx.guild, ctx.author)
        if superuser:
            if ctx.message.attachments:
                print(ctx.message.attachments[0].filename)
                image_extensions = ['.png','.jpg','.gif']
                if ctx.message.attachments[0].filename[-4:] in image_extensions:
                    await ctx.message.attachments[0].save('images/' + ctx.message.attachments[0].filename)

    async def post_image(self,ctx,fileName):
        if os.path.isfile(fileName):
            #print(ctx.message.content)
            try:
                await ctx.message.delete()
            except discord.errors.Forbidden:
                print('Message could not be deleted:Forbidden Error')
            #print(ctx.message.content)
            await ctx.send(f'From: {ctx.author.display_name}',file=discord.File(fileName)) 
