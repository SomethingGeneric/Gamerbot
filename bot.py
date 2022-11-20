# Standard py stuff
from os import listdir
from os.path import isfile, join
import sys

# Discord-py
from discord.ext import commands

# Kind've discord related
from pretty_help import PrettyHelp

# My own classes n such
from util_functions import *

# noinspection PyPackageRequirements
if os.path.sep == "\\":
    print("This bot is only supported on UNIX-like systems. Aborting.")
    sys.exit(1)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Start event handling and bot creation
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("-"),
    description="It's always gamer hour",
    intents=intents,
    owner_id=OWNER_ID,
    help_command=PrettyHelp(),
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
                embed=inf_msg("System", "Finished restarting at: `" + get_stamp() + "`")
            )
        os.remove("restarted.txt")

    ownerman = await bot.fetch_user(bot.owner_id)

    notifyowner = confmgr.get_as_bool("OWNER_DM_RESTART")

    cogs_dir = "cogs"
    for extension in [
        f.replace(".py", "") for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))
    ]:
        try:
            await bot.load_extension(cogs_dir + "." + extension)
            syslog.log("Main", "Loaded " + extension)
            # await ownerman.send(embed=infmsg("System","Loaded `" + extension + "`"))
        except Exception as e:
            try:
                await ownerman.send(
                    embed=err_msg(
                        "System",
                        "Error from cog: " + extension + ": ```" + str(e) + "```",
                    )
                )
            except:
                syslog.log("Main", f"Failed to load extension {extension}.")
            # traceback.print_exc()

    if notifyowner:
        try:
            await ownerman.send(
                embed=inf_msg("System", "Started/restarted at: `" + get_stamp() + "`")
            )
        except:
            pass

    for server in bot.guilds:
        found = False
        members = server.members
        for member in members:
            if member.id == bot.owner_id:
                found = True
        if not found:
            await server.leave()


@bot.event
async def on_message(message):
    if message.author != bot.user:
        await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    syslog.log("Main", "Error in command: " + str(error))
    if "Command" not in str(error) and "not found" not in str(error):
        await ctx.send(embed=err_msg("Error", "```" + str(error) + "```"))


@bot.command()
async def guilds(ctx):
    """Show all guilds the bot is in"""
    msg = "```"
    for server in bot.guilds:
        msg += f"- {server.name}\n"
    msg += "```"
    await ctx.send(msg)


@bot.command()
async def removecog(ctx, name):
    """Un-load a cog that was loaded by default."""
    if await bot.is_owner(ctx.message.author):
        await ctx.send(
            embed=inf_msg("Gotcha", "Ok, I'll try to disable `" + name + "`")
        )
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
            await ctx.send(embed=inf_msg("Output", text))
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

#bot.run(open(my_homedir + "/.token").read())
bot.run(os.environ.get('SECRET_TOKEN'))