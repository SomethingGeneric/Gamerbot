import discord
from discord.ext import commands

from time import sleep
from random import *
import sys, os

intents = discord.Intents.default()
intents.members = True

# Start event handling and bot creation
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("-"),
    description="It's always gamer hour",
    intents=intents,
)


def log(stuff):
    print(stuff)
    with open("peredata.txt", "a+") as f:
        f.write(stuff + "\n")


@bot.event
async def on_ready():
    log("Am online")

    g = await bot.fetch_guild(697456171631509515)
    log("Got " + str(g.name))
    async for member in g.fetch_members():
        log(str(member.id))


bot.run(open(os.getenv("HOME") + "/.fungibletoken").read(), bot=False)
