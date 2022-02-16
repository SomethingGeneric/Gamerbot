import os, re, random
from random import randint
import asyncio

import discord
from discord.ext import commands

from util_functions import *


class lahmoji(commands.Cog):
    """Just lah things :relieved:"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lahmoji(self, ctx, *, emote=""):
        if emote == "":
            files = os.listdir("lahcollection")
            await ctx.send(file=discord.File("lahcollection/" + random.choice(files)))
        else:
            if os.path.exists("lahcollection/" + emote + ".png"):
                await ctx.send(file=discord.File("lahcollection/" + emote + ".png"))
            else:
                await ctx.send("No such lahmoji: `" + emote + "`", reference=ctx.message)


def setup(bot):
    bot.add_cog(lahmoji(bot))
