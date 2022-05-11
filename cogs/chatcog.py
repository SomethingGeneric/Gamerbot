import os, re, random

import discord
from discord.ext import commands

import asyncio

from util_functions import *


class ChatMachine(commands.Cog):
    """I may need help"""

    def __init__(self, bot):
        self.bot = bot

        self.chat_channels = []

        if os.path.exists(".chatchannels"):
            with open(".chatchannels") as f:
                channels = f.read().strip().split("\n")
            for chan in channels:
                self.chat_channels.append(int(chan))

    @commands.command()
    async def makechatchannel(self, ctx):
        adm = False
        for role in ctx.message.author.roles:
            if role.name == "gb_mod":
                adm = True

        if adm:
            self.chat_channels.append(ctx.message.channel.id)
            with open(".chatchannels", "a+") as f:
                f.write(str(ctx.message.channel.id) + "\n")
            await ctx.send("Done!")
        else:
            await ctx.send("You're not a mod")

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            message.channel.id in self.chat_channels
            and message.author != self.bot.user
            and message.content != "-makechatchannel"
        ):
            resp = await run_command_shell(
                'python3 bin/thechatbot.py "' + message.content.replace("'", '"') + '"'
            )
            if len(resp) < 1024:
                await message.channel.send(resp)
            else:
                url = paste(resp)
                await message.channel.send(url)


def setup(bot):
    bot.add_cog(ChatMachine(bot))
