import os, re, random
from random import randint

import discord
from discord.ext import commands

import asyncio

from util_functions import *


class NAG(commands.Cog):
    """When the owner doesn't respond"""

    def __init__(self, bot):
        self.bot = bot
        self.who_gets = NAG_RECIEVER

    @commands.command()
    async def nag(self, ctx, *, message):
        """Nag the bot owner"""
        try:
            await run_command_shell(
                'curl -d "' + message + '" https://ntfy.sh/' + self.who_gets
            )
            await ctx.send("Sent.", reference=ctx.message)
        except Exception as e:
            await ctx.send("Error: `" + str(e) + "`", reference=ctx.message)


def setup(bot):
    bot.add_cog(NAG(bot))
