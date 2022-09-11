# Standard py stuff
from os import listdir
from os.path import isfile, join
import sys

# Pycord
from discord.ext import commands

# Kind've discord related
from pretty_help import DefaultMenu, PrettyHelp

# My own classes n such
from global_config import ConfigManager
from util_functions import *

if os.path.sep == "\\":
    print("This bot is only supported on UNIX-like systems. Aborting.")
    sys.exit(1)

intents = discord.Intents.default()
intents.members = True

# Start event handling and bot creation
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("-"),
    description="It's always gamer hour",
    intents=intents,
    owner_id=OWNER_ID,
)

helpmenu = DefaultMenu("◀️", "▶️", "❌")
bot.help_command = PrettyHelp(
    no_category="Commands", navigation=helpmenu, color=discord.Colour.blurple()
)

# Sane default?
my_homedir = os.getenv("HOME", "/home/gamerbot")

# No default b/c we're fucked long before this if PATH is none
old_path = os.getenv("PATH")
new_path = old_path + ":" + my_homedir + "/.local/bin/:" + os.getcwd() + "/bin/"
os.environ["PATH"] = new_path

print("Our PATH is: " + os.getenv("PATH"))


# Startup event
@bot.event
async def on_ready():
    syslog.log("Main-Important", "Bot has restarted at " + get_stamp())
    syslog.log("Main", f"\n{bot.user} has connected to Discord!\n")

    if check("restarted.txt"):
        channel = get("restarted.txt")
        chan = bot.get_channel(int(channel))
        if chan is not None:
            await chan.send(
                embed=infmsg("System", "Finished restarting at: `" + get_stamp() + "`")
            )
        os.remove("restarted.txt")

    ownerman = await bot.fetch_user(bot.owner_id)

    notifyowner = confmgr.get_as_bool("OWNER_DM_RESTART")

    cogs_dir = "cogs"
    for extension in [
        f.replace(".py", "") for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))
    ]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
            syslog.log("Main", "Loaded " + extension)
            # await ownerman.send(embed=infmsg("System","Loaded `" + extension + "`"))
        except Exception as e:
            await ownerman.send(
                embed=err_msg(
                    "System", "Error from cog: " + extension + ": ```" + str(e) + "```"
                )
            )
            syslog.log("Main", f"Failed to load extension {extension}.")
            # traceback.print_exc()

    if notifyowner:
        await ownerman.send(
            embed=infmsg("System", "Started/restarted at: `" + get_stamp() + "`")
        )

    for server in bot.guilds:
        found = False
        members = server.members
        for member in members:
            if member.id == bot.owner_id:
                found = True
        if not found:
            try:
                invites = server.invites()
                await ownerman.send(f"Didn't find you in {server.name}.")
                if len(invites) == 0:
                    await ownerman.send("Trying to make a new invite.")
                    chan = server.text_channels[0]
                    try:
                        invite = await chan.create_invite()
                        await ownerman.send(f"New invite: {invite.url}")
                    except discord.Forbidden:
                        await ownerman.send(f"No perms to make a new invite :( The guild id is {str(server.id)} btw")
                else:
                    for invite in invites:
                        await ownerman.send(f"Invite: {invite.url}")
            except discord.Forbidden:
                await ownerman.send(f"Didn't find your in {server.name} with {str(server.id)}, but I can't invite you to it.")
        else:
            await ownerman.send(f"We're both in {server.name}")


@bot.event
async def on_message(message):
    if message.author != bot.user:
        await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    syslog.log("Main", "Error in command: " + str(error))
    await ctx.send(embed=err_msg("Error", "```" + str(error) + "```"))


@bot.command()
async def removecog(ctx, name):
    """Un-load a cog that was loaded by default."""
    if await bot.is_owner(ctx.message.author):
        await ctx.send(embed=infmsg("Gotcha", "Ok, I'll try to disable `" + name + "`"))
        try:
            bot.remove_cog(name)
            syslog.log("Main", "Disabled cog: " + name)
            await ctx.send(embed=warn_msg("Done", "Disabled: `" + name + "`."))
        except Exception as e:
            await ctx.send(
                embed=err_msg("Broke", "Something went wrong: `" + str(e) + "`.")
            )
    else:
        await ctx.send(embed=err_msg("Oops", wrong_perms("removecog")))


@bot.command()
async def getsyslog(ctx):
    """Get a copy of the system log"""
    if await bot.is_owner(ctx.message.author):
        log = syslog.get_log()
        if len(log) > 1994:
            text = paste(log)
            await ctx.send(embed=infmsg("Output", text))
        else:
            text = "```" + log + "```"
            await ctx.send("Here you go:")
            await ctx.send(text)
    else:
        await ctx.send(embed=err_msg("Oops", wrong_perms("getsyslog")))


if UNLOAD_COGS is not None:
    # Remove any cogs as per config
    for item in UNLOAD_COGS:
        if item != "" and item != " ":
            syslog.log("Main", "Trying to remove '" + item + "'")
            res = bot.remove_cog(item)
            if res is not None:
                syslog.log("Main", "Removed '" + item + "'")
            else:
                syslog.log("Main", "Failed to remove '" + item + "'")

bot.run(open(my_homedir + "/.token").read())
