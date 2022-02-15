import discord
from discord.ext import commands

from time import sleep
from random import *
import sys

intents = discord.Intents.default()
intents.members = True

# Start event handling and bot creation
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("-"),
    description="It's always gamer hour",
    intents=intents,
)

def log(stuff):
    with open("data.txt", "a+") as f:
        f.write(stuff + "\n")

@bot.event
async def on_ready():
    print("Am online")

    for g in bot.guilds:
        log("Start of " + g.name + ", id: " + str(g.id))
        async for lad in g.fetch_members():
            log("- Member: " + lad.name + " # " + lad.discriminator)


bot.run("", bot=False)
