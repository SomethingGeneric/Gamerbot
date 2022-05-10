import os, re, random
from random import randint

import discord
from discord.ext import commands

import asyncio

from util_functions import *


class Meows(commands.Cog):
    """I'm a cat, after all."""

    def __init__(self, bot):
        self.bot = bot
        self.troll_task.start()

    def cog_unload(self):
        self.troll_task.cancel()

    @commands.Cog.listener()
    async def on_message(self, message):
        reactions = {
            "cat": "🐱",
            "lost": "🗺️",
            "frog": "🐸",
            "dog": "🐶",
            "gnome": "❌",
            "gnu": "❌",
            "bsd": "✅",
            "beastie": "✅",
            "daemon": "✅",
            "tux": "✅",
            "kek": "🤣",
            "kekw": "🤣",
            "grr": "🦁",
            "wave": "🌊",
            "surfing": "🏄",
            "boo": "👻",
        }

        for word in message.content.split(" "):
            for reaction in reactions.keys():
                if re.sub(r"[^\w\s]", "", word.lower()) == reaction:
                    await message.add_reaction(reactions[reaction])

        if DO_IMAGE_RESPONSE:
            if random.randint(
                1, IMAGE_RESPONSE_PROB
            ) == IMAGE_RESPONSE_PROB and "filename" in str(message.attachments):
                if not os.path.exists(".nomeow_" + str(message.guild.id)):
                    await mchan.send(random.choice(IMAGE_RESPONSES), reference=message)

        mc = message.content.lower()
        mchan = message.channel

        triggers = {
            "scratch": "all my homies hate scratch",
            "tesla": "elon more like pee-lon",
            "elon": "elon more like pee-lon",
            "rms": "RMS is a pedo",
            "stallman": "RMS is a pedo",
            "epstein": "didn't kill himself",
            "forgor": "💀 they forgor",
            "rember": "👼 they rember",
            "crystalux": "Don't deadname! :angry:",
            "hello there": "General Kenobi.\nhttps://media1.giphy.com/media/UIeLsVh8P64G4/giphy.gif",
        }

        if message.author != self.bot.user:

            for thing in triggers.keys():
                if thing in mc:
                    await message.channel.send(triggers[thing])

            if "comrade sharkfact" in mc:
                with open("data/sharkfacts.txt", encoding="cp1252") as f:
                    sharkList = f.read().split("\n")
                await mchan.send(
                    embed=infmsg("Sharkfact", random.choice(sharkList)),
                    reference=message,
                )

    @tasks.loop(seconds=3600.0)
    async def troll_task(self):
        for guild in self.bot.guilds:
            for chan in guild.text_channels:
                try:
                    if random.randint(1, 1000) == 500:
                        if not os.path.exists(".nomeow_" + str(message.guild.id)):
                            await chan.send(random.choice(IMAGE_RESPONSES))
                            break
                except:
                    pass

    @troll_task.before_loop
    async def before_the_troll_task(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Meows(bot))
