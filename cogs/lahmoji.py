import os, re, random
from random import randint
import asyncio

import discord
from discord.ext import commands

from util_functions import *
from server_config import serverconfig


class lahmoji(commands.Cog):
    """Just floppa things :relieved:"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lahmoji(self, ctx):
        files = os.listdir("lahcollection")
        await ctx.send(file=discord.File("lahcollection/" + random.choice(files)))


def setup(bot):
    bot.add_cog(lahmoji(bot))
