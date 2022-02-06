import os, re, random
from random import randint

import discord
from discord.ext import commands

import asyncio

from util_functions import *
from server_config import serverconfig
from memail import MEmail

class Nag(commands.Cog):
    """When Matt doesn't respond"""

    def __init__(self, bot):
        self.bot = bot
        self.email = MEmail()
        self.who_gets = NAG_RECIEVER

    @commands.command()
    async def nag(self, ctx, *, message):
        """Nag the bot owner"""
        try:
            self.email.send(self.who_gets, message)
            await ctx.send("Sent.", reference=ctx.message)
        except Exception as e:
            await ctx.send("Error: `" + str(e) + "`", reference=ctx.message)

def setup(bot):
    bot.add_cog(Nag(bot))