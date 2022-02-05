from discord.ext import commands
import os
import discord
import sys

import functions.profile_fun as pf
import logging

logger = logging.getLogger(__name__)

class images(commands.Cog):
    def __init__(self, bot):
        logger.info('Cog Loaded: images')
        self.bot = bot

    @commands.command()
    async def upload_image(self,ctx):
        users = self.bot.get_cog('users')
        superuser = await users.check_super(ctx.guild, ctx.author)
        if superuser:
            if ctx.message.attachments:
                logger.info(ctx.message.attachments[0].filename)
                image_extensions = ['.png','.jpg','.gif']
                if ctx.message.attachments[0].filename[-4:] in image_extensions:
                    await ctx.message.attachments[0].save('data/images/' + ctx.message.attachments[0].filename)

    async def post_image(self,ctx,fileName):
        if os.path.isfile(fileName):
            #logger.info(ctx.message.content)
            try:
                await ctx.message.delete()
            except discord.errors.Forbidden:
                logger.info('Message could not be deleted:Forbidden Error')
            #logger.info(ctx.message.content)
            await ctx.send(f'From: {ctx.author.display_name}',file=discord.File(fileName)) 


    @commands.command()
    async def gitgud(self,ctx):
        await self.post_image(ctx,'data/images/gitgud.jpg')


    @commands.command()
    async def dwagon(self,ctx):
        await self.post_image(ctx,'data/images/dwagon.gif')


    @commands.command()
    async def catboy(self,ctx):
        await self.post_image(ctx,'data/images/catboy.png')


    @commands.command()
    async def airhorn(self,ctx):
        await self.post_image(ctx,'data/images/airhorn.png')


    @commands.command()
    async def trash(self,ctx):
        await self.post_image(ctx,'data/images/trash.png')


    @commands.command()
    async def icon_xl(self,ctx):
        await self.post_image(ctx,'data/images/icon_xl.png')


    @commands.command()
    async def kataki27(self,ctx):
        await self.post_image(ctx,'data/images/kataki27.png')


    @commands.command()
    async def meowdy(self,ctx):
        await self.post_image(ctx,'data/images/meowdy.png')


    @commands.command()
    async def letsgochamp(self,ctx):
        await self.post_image(ctx,'data/images/letsgochamp.png')


    @commands.command()
    async def thiscodyassmotherfucker(self,ctx):
        await self.post_image(ctx,'data/images/thiscodyassmotherfucker.png')


    @commands.command()
    async def gungan(self,ctx):
        await self.post_image(ctx,'data/images/gungan.png')


    @commands.command()
    async def friendship(self,ctx):
        await self.post_image(ctx,'data/images/Friendship.png')


    @commands.command()
    async def same(self,ctx):
        await self.post_image(ctx,'data/images/Same.png')


    @commands.command()
    async def soup(self,ctx):
        await self.post_image(ctx,'data/images/soup.png')


    @commands.command()
    async def tuffin(self,ctx):
        await self.post_image(ctx,'data/images/tuffin.png')


    @commands.command()
    async def salt(self,ctx):
        await self.post_image(ctx,'data/images/salt.png')


    @commands.command()
    async def hazers(self,ctx):
        await self.post_image(ctx,'data/images/hazers.png')


    @commands.command()
    async def yoona(self,ctx):
        await self.post_image(ctx,'data/images/yoona.png')


    @commands.command()
    async def heirloom(self,ctx):
        await self.post_image(ctx,'data/images/heirloom.png')


    @commands.command()
    async def play2win(self,ctx):
        await self.post_image(ctx,'data/images/Play2Win.png')


    @commands.command()
    async def fact(self,ctx):
        await self.post_image(ctx,'data/images/fact.png')


    @commands.command()
    async def zoeyell(self,ctx):
        await self.post_image(ctx,'data/images/zoeyell.png')


    @commands.command()
    async def yougotta(self,ctx):
        await self.post_image(ctx,'data/images/yougotta.png')


    @commands.command()
    async def hanzmeter(self,ctx):
        await self.post_image(ctx,'data/images/HanzMeter.png')


    @commands.command()
    async def rolfo(self,ctx):
        await self.post_image(ctx,'data/images/RolfO.png')


    @commands.command()
    async def basard(self,ctx):
        await self.post_image(ctx,'data/images/basard.png')


    @commands.command()
    async def beancup(self,ctx):
        await self.post_image(ctx,'data/images/beancup.png')


    @commands.command()
    async def banhammer(self,ctx):
        await self.post_image(ctx,'data/images/banhammer.png')


    @commands.command()
    async def caprese(self,ctx):
        await self.post_image(ctx,'data/images/Caprese.png')


    @commands.command()
    async def drift(self,ctx):
        await self.post_image(ctx,'data/images/drift.png')


    @commands.command()
    async def coldone(self,ctx):
        await self.post_image(ctx,'data/images/ColdOne.png')


    @commands.command()
    async def veasna2x(self,ctx):
        await self.post_image(ctx,'data/images/veasna2x.png')


    @commands.command()
    async def guillotine(self,ctx):
        await self.post_image(ctx,'data/images/guillotine.png')


    @commands.command()
    async def win(self,ctx):
        await self.post_image(ctx,'data/images/WIN.png')



