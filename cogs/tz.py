import os, re, random
from random import randint
import asyncio

import discord
from discord.ext import commands
import requests

from util_functions import *
from server_config import serverconfig


class TZ(commands.Cog):
    """Time stuffz"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def timein(self, ctx, first, second):
        """Get current time in a place"""
        r = requests.get("https://worldtimeapi.org/api/timezone/" + first + "/" + second)
        obj = r.json
        dt = obj['datetime']
        await ctx.send(dt)

def setup(bot):
    bot.add_cog(TZ(bot))
