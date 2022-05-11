import os, re, random
from random import randint

import discord
from discord.ext import commands, tasks

import asyncio

from util_functions import *


class MeowManager:
    def __init__(self):
        if not os.path.exists("meowmanager"):
            os.makedirs("meowmanager")

    def check_disabled(self, action, guild, channel):
        respond = False
        if os.path.exists("meowmanager/" + str(guild) + "_" + action):
            respond = True
        elif os.path.exists("meowmanager/" + str(channel) + "_" + action):
            respond = True
        return respond

    def toggle_disabled(self, action, where):
        if os.path.exists("meowmanager/" + str(where) + "_" + action):
            os.remove("meowmanager/" + str(where) + "_" + action)
            return True
        else:
            with open("meowmanager/" + str(where) + "_" + action, "w") as f:
                f.write("Meow.")
            return False


class Meows(commands.Cog):
    """I'm a cat, after all."""

    def __init__(self, bot):
        self.bot = bot
        self.troll_task.start()
        self.mm = MeowManager()
        self.keys = ["imageresponse", "snarkycomment", "sharkfact", "randommeow"]

    def cog_unload(self):
        self.troll_task.cancel()

    @commands.command()
    async def togglemeow(self, ctx, key="", where=""):
        """Disable or enable a given type of meow"""
        if key is None or key == "" or key not in self.keys:
            await ctx.send("Accepted keys are: ```\n" + "\n".join(self.keys) + "```")
            return

        if where != "channel" and where != "guild":
            await ctx.send(
                "For the `where` argument, you must use either `channel` or `guild`."
            )
            return

        auth = False
        for role in ctx.message.author.roles:
            if role.name == "gb_mod":
                auth = True

        if auth:
            owhere = where
            if where == "channel":
                where = str(ctx.message.channel.id)
            else:
                where = str(ctx.message.guild.id)
            res = self.mm.toggle_disabled(key, where)
            if res:
                await ctx.send(
                    "`"
                    + key
                    + "` is now enabled in this "
                    + owhere
                    + " : `"
                    + where
                    + "`"
                )
            else:
                await ctx.send(
                    "`"
                    + key
                    + "` is now disabled in this "
                    + owhere
                    + " : `"
                    + where
                    + "`"
                )
        else:
            await ctx.send("You're not a moderator")

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

            for word in message.content.split(" "):
                for reaction in reactions.keys():
                    if re.sub(r"[^\w\s]", "", word.lower()) == reaction:
                        await message.add_reaction(reactions[reaction])

            if DO_IMAGE_RESPONSE:
                if random.randint(
                    1, IMAGE_RESPONSE_PROB
                ) == IMAGE_RESPONSE_PROB and "filename" in str(message.attachments):
                    if not self.mm.check_disabled(
                        "imageresponse", message.guild.id, message.channel.id
                    ):
                        await mchan.send(
                            random.choice(IMAGE_RESPONSES), reference=message
                        )

            for thing in triggers.keys():
                if thing in mc:
                    if not self.mm.check_disabled(
                        "snarkycomment", message.guild.id, message.channel.id
                    ):
                        await message.channel.send(triggers[thing])

            if "comrade sharkfact" in mc:
                if not self.mm.check_disabled(
                    "sharkfact", message.guild.id, message.channel.id
                ):
                    with open("data/sharkfacts.txt", encoding="cp1252") as f:
                        sharkList = f.read().split("\n")
                    await mchan.send(
                        embed=infmsg("Sharkfact", random.choice(sharkList)),
                        reference=message,
                    )

    @tasks.loop(seconds=60.0)
    async def troll_task(self):
        for guild in self.bot.guilds:
            for chan in guild.text_channels:
                try:
                    if random.randint(1, 1000) == 500:
                        if not self.mm.check_disabled(
                            "randommeow", message.guild.id, message.channel.id
                        ):
                            await chan.send(random.choice(IMAGE_RESPONSES))
                            break
                except:
                    pass

    @troll_task.before_loop
    async def before_the_troll_task(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Meows(bot))
