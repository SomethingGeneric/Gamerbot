import os, re, random
from random import randint

import discord
from discord.ext import commands

import asyncio

from util_functions import *


class Chat(commands.Cog):
    """Images for use in chat"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def crab(self, ctx):
        """🦀🦀🦀🦀🦀"""
        try:
            await ctx.message.delete()
        except Exception as e:
            # This should only break if we don't have manage message perm
            pass
        await ctx.send(
            "https://media.tenor.com/images/a16246936101a550918944740789de8a/tenor.gif",
        )

    @commands.command()
    async def deadchat(self, ctx):
        try:
            await ctx.message.delete()
        except Exception as e:
            # This should only break if we don't have manage message perm
            pass
        await ctx.send(
            "https://media.tenor.com/images/f799b7d7993b74a7852e1eaf2695d9d7/tenor.gif",
        )

    @commands.command()
    async def xd(self, ctx):
        """😂😂😂😂😂"""
        try:
            await ctx.message.delete()
        except Exception as e:
            # This should only break if we don't have manage message perm
            pass
        await ctx.send(file=discord.File("images/LMAO.jpg"))

    @commands.command()
    async def kat(self, ctx):
        """*sad cat noises*"""
        try:
            await ctx.message.delete()
        except Exception as e:
            # This should only break if we don't have manage message perm
            pass
        await ctx.send(file=discord.File("images/krying_kat.png"))

    @commands.command()
    async def yea(self, ctx):
        """it do be like that"""
        try:
            await ctx.message.delete()
        except Exception as e:
            # This should only break if we don't have manage message perm
            pass
        await ctx.send(file=discord.File("images/yeah.png"))

    @commands.command()
    async def no(self, ctx):
        """it do not be like that"""
        try:
            await ctx.message.delete()
        except Exception as e:
            # This should only break if we don't have manage message perm
            pass
        await ctx.send(file=discord.File("images/no.png"))

    @commands.command()
    async def stoptalking(self, ctx):
        """just do."""
        try:
            await ctx.message.delete()
        except Exception as e:
            # This should only break if we don't have manage message perm
            pass
        await ctx.send(file=discord.File("images/stop_talking.png"))

    @commands.command()
    async def forkbomb(self, ctx):
        """rip to myself"""
        try:
            await ctx.message.delete()
        except Exception as e:
            # This should only break if we don't have manage message perm
            pass
        await ctx.send(file=discord.File("images/forkbomb.jpg"))

    @commands.command()
    async def permit(self, ctx):
        """go right ahead."""
        try:
            await ctx.message.delete()
        except Exception as e:
            # This should only break if we don't have manage message perm
            pass
        await ctx.send(file=discord.File("images/permit_crab.jpg"))

    @commands.command()
    async def whenthe(self, ctx):
        """use this when the"""
        await ctx.send(
            "https://cdn.discordapp.com/attachments/732599669867413505/921838252275695686/7Vcj8V5vrrN7G71g.mp4"
        )

    @commands.command()
    async def floppa(self, ctx, *, emote=""):
        """floppa things"""
        if emote == "":
            files = os.listdir("images/floppa")
            await ctx.send(file=discord.File("images/floppa/" + random.choice(files)))
        else:
            if os.path.exists("images/floppa/" + emote + ".png"):
                await ctx.send(file=discord.File("images/floppa/" + emote + ".png"))
            else:
                await ctx.send("No such floppa: `" + emote + "`", reference=ctx.message)

    @commands.command()
    async def lahmoji(self, ctx, *, emote=""):
        if emote == "":
            files = os.listdir("images/lahcollection")
            await ctx.send(
                file=discord.File("images/lahcollection/" + random.choice(files))
            )
        else:
            for ext in [".jpg", ".png", ".gif"]:
                if os.path.exists("images/lahcollection/" + emote + ext):
                    await ctx.send(
                        file=discord.File("images/lahcollection/" + emote + ext)
                    )
                    return

            await ctx.send("No such lahmoji: `" + emote + "`", reference=ctx.message)

    @commands.Cog.listener()
    async def on_message(self, message):
        if "lost" in message.content:
            await message.channel.send("Sorry pal")
            try:
                await message.add_reaction(":map:")
            except Exception as e:
                await message.channel.send(str(e))


def setup(bot):
    bot.add_cog(Chat(bot))
