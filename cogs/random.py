import discord
from discord.ext import commands

from util_functions import *

# Hopefully we'll never need logging here


class Random(commands.Cog):
    """Stuff that the developer couldn't find a better category for"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """pong."""
        await ctx.send(
            "pong. :upside_down: :gun:", file=discord.File("images/pong.jpg")
        )

    @commands.command()
    async def math(self, ctx, *, exp):
        """Do simple math on an expression (uses BC)"""
        res = await run_command_shell('echo "' + exp + '" | bc')
        if len(res) != 0:
            if len(res) < 1998:
                await ctx.send(embed=infmsg("Eval", "`" + str(res) + "`"))
            else:
                url = paste(res)
                await ctx.send(
                    embed=infmsg(
                        "Eval", "Output was too many characters. Here's a link: " + url
                    )
                )
        else:
            await ctx.send(embed=warn_msg("Eval", "No output."))


def setup(bot):
    bot.add_cog(Random(bot))
