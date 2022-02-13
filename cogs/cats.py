import os, re, random
from random import randint

import discord
from discord.ext import commands

import asyncio

from util_functions import *
from server_config import serverconfig

import requests

class Cats(commands.Cog):
    """Just cat Things"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def catpic(self, ctx):
        r = requests.get("https://cataas.com/cat", allow_redirects=True)
        name = "".join(random.sample(string.ascii_lowercase+string.digits, 5)) + ".jpeg"
        open(name, "wb").write(r.content)
        await ctx.send(file=discord.File(name))
        os.remove(name)

    @commands.command()
    async def catgif(self, ctx):
        r = requests.get("https://cataas.com/cat/gif", allow_redirects=True)
        name = "".join(random.sample(string.ascii_lowercase+string.digits, 5)) + ".jpeg"
        open(name, "wb").write(r.content)
        await ctx.send(file=discord.File(name))
        os.remove(name)

def setup(bot):
    bot.add_cog(Cats(bot))
