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
    print(stuff)
    with open("data.txt", "a+") as f:
        f.write(stuff + "\n")


messages = ["troll", "kekw", "lol", "xd", "you're a hoe", "you're a whore"]


@bot.event
async def on_ready():
    log("Am online")

    fuckhead = await bot.fetch_user(722714559210717215)
    while True:
        await fuckhead.send(choice(messages))


bot.run("")
