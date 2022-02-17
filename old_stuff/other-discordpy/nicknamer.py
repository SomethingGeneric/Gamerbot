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


@bot.event
async def on_ready():
    print("Am online")
    g = await bot.fetch_guild(921829349613797386)
    print("Got guild")

    async for lad in g.fetch_members():
        print(str(lad.display_name))
        try:
            await lad.edit(
                nick=str(
                    randint(
                        0,
                        1000000000000000000000,
                    )
                )
            )
        except Exception as e:
            print(str(e))


bot.run("")
