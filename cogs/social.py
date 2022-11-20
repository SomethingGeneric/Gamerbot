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
        if not os.path.isfile(f"{self.volpath}/{self.ccredpath}"):
            r = RandomWords()
            w = r.get_random_word()
            Mastodon.create_app(
                f"gamerthebot-{w}-{str(randint(1,10))}",
                api_base_url=os.environ.get("MASTODON_URL"),
                to_file=f"{self.volpath}/{self.ccredpath}",
            )

        mastodon = Mastodon(client_id=f"{self.volpath}/{self.ccredpath}")

        mastodon.log_in(
            os.environ.get("MASTODON_EMAIL"),
            os.environ.get("MASTODON_PASSWORD"),
            to_file=f"{self.volpath}/{self.ucredpath}",
        )

        with open(f"{self.volpath}/post-log.txt", "a+") as f:
            f.write(
                f"User {ctx.message.author.name}#{str(ctx.message.author.discriminator)} posted: '{text}'"
            )

        res = mastodon.toot(
            f"{text} - {ctx.message.author.name}#{str(ctx.message.author.discriminator)}"
        )

        await ctx.send(f"See your post here: {res['url']}", reference=ctx.message)

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
