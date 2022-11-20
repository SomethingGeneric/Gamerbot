from discord.ext import commands
from mastodon import Mastodon
from random_word import RandomWords
from random import randint
import os

from util_functions import *

# /gb-data


class Social(commands.Cog):
    """Funny social internet stuff"""

    def __init__(self, bot):
        self.bot = bot

        self.volpath = "/gb-data"
        self.ccredpath = "tootclientcred.secret"
        self.ucredpath = "tootusercred.secret"

    @commands.command()
    async def toot(self, ctx, *, text="Enmpty"):
        """Send a post out to the fediverse"""
        url = os.environ.get("MASTODON_URL")
        email = os.environ.get("MASTODON_EMAIL")
        passw = os.environ.get("MASTODON_PASSWORD")
        output = await run_command_shell(
            f"python3 bin/do_toot.py '{url}' '{email}' '{passw}' '{self.volpath}' '{self.ccredpath}' '{self.ucredpath}' '{text}' '{ctx.message.author.name}' '{str(ctx.message.author.discriminator)}'"
        )

        await ctx.send(f"See your post here: {output}", reference=ctx.message)

    @commands.command()
    async def post_log(self, ctx):
        """Don't even worry about it"""
        if ctx.message.author.id == OWNER_ID:
            with open(f"{self.volpath}/post-log.txt") as f:
                raw_log = f.read()
            msg = f"```{raw_log}```"
            if len(msg) > 400:
                msg = pastef(f"{self.volpath}/post-log.txt")
            await ctx.send(msg, reference=ctx.message)
        else:
            await ctx.send(wrong_perms("post_log"))



async def setup(bot):
    await bot.add_cog(Social(bot))
