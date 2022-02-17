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
                    if not os.path.exists(".sent_" + str(message.guild.id)):
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
                            "You should also run `-setannounce` in the channel which you want messages posted by said users w/ `-announce` to go. Or, you can leave it unset if you don't wish to use my announcement feature."
                        )
                        if not found:
                            await guild.owner.send(
                                "You should also invite the bot's owner to this guild ;)"
                            )
                        with open(".sent_" + str(message.guild.id), "w") as f:
                            f.write(":yea:")

    def checkmod(self, member):
        for role in member.roles:
            if role.name == "gb_mod":
                return True
        return False

    @commands.command()
    async def setannounce(self, ctx):
        """Set current channel as the bot's announce channel"""
        if ctx.message.author == ctx.message.guild.owner:
            if not os.path.exists("gs/" + str(ctx.message.guild.id)):
                os.makedirs("gs/" + str(ctx.message.guild.id))
            with open("gs/" + str(ctx.message.guild.id) + "/ann", "w") as f:
                f.write(str(ctx.message.channel.id))
            m = await ctx.send(
                "This is now the announce channel. This message will delete in 2s"
            )
            async with ctx.typing():
                await asyncio.sleep(2)
            await m.delete()
            await ctx.message.delete()
        else:
            await ctx.send("You are not the owner of this guild. :(")

    @commands.command()
    async def announce(self, ctx, *, text):
        """Announce <text> in the channel specified in settings"""
        if not isinstance(ctx.message.channel, discord.channel.DMChannel):
            if self.checkmod(ctx.message.author):
                if not os.path.exists("gs/" + str(ctx.message.guild.id)):
                    await ctx.send(
                        embed=errmsg(
                            "Config Error",
                            "Server owner has not set the value of `announcements` to the target channel",
                        )
                    )
                else:
                    chanr = open("gs/" + str(ctx.message.guild.id) + "/ann").read()
                    chanid = int(chanr)
                    announcements = self.bot.get_channel(chanid)
                    await announcements.send(embed=infmsg("Announcement", text))
                    msg = await ctx.send(embed=infmsg("Yay", "Message sent."))
                    async with ctx.typing():
                        await asyncio.sleep(2)
                    await msg.delete()
                    await ctx.message.delete()
            else:
                await ctx.send(embed=errmsg("Oops.", wrongperms("announce")))
        else:
            await ctx.send(
                embed=errmsg("Usage error", "This command only works in servers.")
            )

    @commands.command()
    async def purgeall(self, ctx):
        """Erase all messages in channel"""
        if not isinstance(ctx.message.channel, discord.channel.DMChannel):
            if self.checkmod(ctx.message.author):
                total = 0
                async with ctx.message.channel.typing():
                    while True:
                        try:
                            deleted = await ctx.message.channel.purge(bulk=True)
                            total += deleted
                        except:
                            # total += 100
                            break
                await ctx.send(
                    embed=infmsg(
                        "Purged",
                        "Erased " + str(total) + " messages.",
                    )
                )
            else:
                await ctx.send(
                    ctx.message.author.mention,
                    embed=errmsg("Oops", "You're not a mod here."),
                )
        else:
            await ctx.send(
                embed=errmsg("Purge", "Right now, purge does not work in DM's.")
            )

    @commands.command()
    async def purge(self, ctx, count=1, filter=""):
        """Erase <x> messages, either from user <filter> or containing <filter> in contents"""
        try:
            count = int(count)
            if not isinstance(ctx.message.channel, discord.channel.DMChannel):
                if self.checkmod(ctx.message.author):
                    if "<@!" in filter or "<@" in filter:
                        try:
                            pid = (
                                filter.replace("<@!", "")
                                .replace("<@", "")
                                .replace(">", "")
                            )
                            person = await self.bot.fetch_user(int(pid))
                            if person != None:
                                await ctx.send(
                                    embed=infmsg(
                                        "Purge",
                                        "Erasing the last `"
                                        + str(count)
                                        + "` messages from "
                                        + person.mention,
                                    )
                                )
                                self.store = person
                                async with ctx.message.channel.typing():
                                    deleted = await ctx.message.channel.purge(
                                        limit=count,
                                        check=lambda m: m.author.id == person.id,
                                        bulk=True,
                                    )
                                await ctx.send(
                                    embed=infmsg(
                                        "Purged",
                                        "Erased " + str(len(deleted)) + " messages.",
                                    )
                                )
                            else:
                                await ctx.send(
                                    embed=errmsg(
                                        "Purge Error",
                                        "Couldn't any person with input `"
                                        + filter
                                        + "`",
                                    )
                                )
                        except Exception as e:
                            await ctx.send(
                                embed=errmsg("Purge Error", "```" + str(e) + "```")
                            )
                    else:
                        try:
                            await ctx.send(
                                embed=infmsg(
                                    "Purge",
                                    "Erasing the last `"
                                    + str(count)
                                    + " messages that contain `"
                                    + filter
                                    + "`",
                                )
                            )
                            self.store = filter
                            async with ctx.message.channel.typing():
                                deleted = await ctx.message.channel.purge(
                                    limit=count,
                                    check=lambda m: filter.lower() in m.content.lower(),
                                    bulk=True,
                                )
                            await ctx.send(
                                embed=infmsg(
                                    "Purged",
                                    "Erased " + str(len(deleted)) + " messages.",
                                )
                            )
                        except Exception as e:
                            await ctx.send(
                                embed=errmsg("Purge Error", "```" + str(e) + "```")
                            )
                else:
                    await ctx.send(
                        ctx.message.author.mention,
                        embed=errmsg("Oops", "You're not a mod here."),
                    )
            else:
                await ctx.send(
                    embed=errmsg("Purge", "Right now, purge does not work in DM's.")
                )
        except Exception as e:
            await ctx.send(embed=errmsg("Purge Error", "```" + str(e) + "```"))

    @commands.command(hidden=True)
    async def announce_all(self, ctx, *, message):
        if await self.bot.is_owner(ctx.message.author):
            await ctx.send("Announcing to all servers.")
            for guild in self.bot.guilds:
                for channel in guild.channels:
                    try:
                        await channel.send(message)
                        break
                    except:
                        pass


def setup(bot):
    bot.add_cog(Admin(bot))


# End non-user stuff
