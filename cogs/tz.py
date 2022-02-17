import os, re, random
from random import randint
import asyncio

import discord
from discord.ext import commands
import requests

from util_functions import *


class TZ(commands.Cog):
    """Time stuffz"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def timein(self, ctx, first, second):
        """Get current time in a place"""
        r = requests.get(
            "https://worldtimeapi.org/api/timezone/" + first + "/" + second
        )
        obj = r.json()
        dt = obj["datetime"]

        date = dt.split("T")[0]
        time = dt.split("T")[1]


def setup(bot):
    bot.add_cog(TZ(bot))
