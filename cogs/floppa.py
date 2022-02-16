import os, re, random

import discord
from discord.ext import commands

from util_functions import *


class Floppa(commands.Cog):
    """Just floppa things :relieved:"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def floppa(self, ctx, *, emote=""):
        if emote == "":
            files = os.listdir("floppa")
            await ctx.send(file=discord.File("floppa/" + random.choice(files)))
        else:
            if os.path.exists("floppa/" + emote + ".png"):
                await ctx.send(file=discord.File("floppa/" + emote + ".png"))
            else:
                await ctx.send("No such floppa: `" + emote + "`", reference=ctx.message)


def setup(bot):
    bot.add_cog(Floppa(bot))
