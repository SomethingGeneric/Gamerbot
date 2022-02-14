import os, re, random
from random import randint
import asyncio

import discord
from discord.ext import commands

from util_functions import *


class Floppa(commands.Cog):
    """Just floppa things :relieved:"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def floppa(self, ctx):
        files = os.listdir("floppa")
        await ctx.send(file=discord.File("floppa/" + random.choice(files)))


def setup(bot):
    bot.add_cog(Floppa(bot))
