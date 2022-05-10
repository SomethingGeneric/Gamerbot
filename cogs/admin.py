import os, sys

import discord
from discord.ext import commands

import asyncio

from util_functions import *
from global_config import configboi

# Non-user stuff (mods/debug)
class Admin(commands.Cog):
    """Commands for guild admins"""

    def __init__(self, bot):
        self.bot = bot
        self.confmgr = configboi("config.txt", False)
        self.store = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if not isinstance(message.channel, discord.channel.DMChannel):
            for guild in self.bot.guilds:
                found = False
                for role in guild.roles:
                    if role.name == "gb_mod":
                        found = True
                        break
                if not found:
                    if not os.path.exists(".setupdone_" + str(message.guild.id)):
                        modr = await guild.create_role(
                            name="gb_mod",
                            reason="Role used to designate who can use our admin commands.",
                        )

                        found = False
                        for member in guild.members:
                            if await self.bot.is_owner(member):
                                found = True

                        await guild.owner.send(
                            "Hi! You should add your trusted server members of `"
                            + str(guild.name)
                            + "` to the role `gb_mod`"
                        )
                        await guild.owner.send(
                            "Also, if you dislike my random meows, then you, or someone else with `gb_mod` role can run `-disablemeow` so that I'll leave the guild alone."
                        )
                        if not found:
                            await guild.owner.send(
                                "You should also invite the bot's owner to this guild ;)"
                            )
                        with open(".setupdone_" + str(message.guild.id), "w") as f:
                            f.write("THIS IS THE NEWER VERSION OF THE LOCKFILE")

    def checkmod(self, member):
        for role in member.roles:
            if role.name == "gb_mod":
                return True
        return False

    @commands.command()
    async def disablemeow(self, ctx):
        if self.checkmod(ctx.message.author):
            with open(".nomeow_" + str(message.guild.id), "w") as f:
                f.write("No more meowing :(")
            await ctx.send("Disabled meowing in this guild.", reference=ctx.message)
        else:
            await ctx.send("You don't have perms in this guild.")


def setup(bot):
    bot.add_cog(Admin(bot))


# End non-user stuff
