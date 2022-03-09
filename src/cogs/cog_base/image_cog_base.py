from discord.ext import commands
import os
import discord
import sys

import src.functions.profile_fun as pf
import logging
from discord.commands import slash_command

logger = logging.getLogger(__name__)

class images(commands.Cog):
    def __init__(self, bot):
        logger.info('Cog Loaded: images')
        self.bot = bot

    @slash_command()
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
