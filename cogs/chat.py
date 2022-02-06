import os, re, random
from random import randint

import discord
from discord.ext import commands

import asyncio

from util_functions import *
from server_config import serverconfig

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

def setup(bot):
    bot.add_cog(Chat(bot))