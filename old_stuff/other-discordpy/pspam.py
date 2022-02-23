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
    with open("pere_69_data.txt", "a+") as f:
        f.write(stuff + "\n")


messages = ["troll", "kekw", "lol", "xd", "you're a hoe", "you're a whore"]


@bot.event
async def on_ready():
    log("Am online")

    ppl = [
        786238121846505541,
        706028008548466721,
        385348211516243968,
        713376094706991160,
        783679923054968843,
        424899221267939328,
    ]

    while True:
        for uid in ppl:
            fucker = await bot.fetch_user(uid)
            await fucker.send(choice(messages))
            log("Spammed " + str(fucker.display_name))


bot.run(open(os.getenv("HOME") + "/.fungibletoken").read(), bot=False)
