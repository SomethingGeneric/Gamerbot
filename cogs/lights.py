import os, re, random
from random import randint

import discord
from discord.ext import commands

import asyncio

from util_functions import *
from server_config import serverconfig

from lifxlan import *

class IOT(commands.Cog):
    """IOT Things"""

    def __init__(self, bot):
        self.bot = bot
        self.light = Light(LIFX_MAC, LIFX_IP)

    @commands.command()
    async def lifx(self, ctx, *, cmd=""):
        """Set Matt's light to a color. (Run w/o arguements for help info)"""
        colors = {
            "red": RED,
            "orange": ORANGE,
            "yellow": YELLOW,
            "green": GREEN,
            "cyan": CYAN,
            "blue": BLUE,
            "purple": PURPLE,
            "pink": PINK,
            "crystal": [50972, 65535, 65535, 4000],
        }

        if cmd == "":
            i = "Colors: "
            for c in colors.keys():
                i += "`" + c + "`, "
            await ctx.send(i)
            await ctx.send("You can also say `random`, `sample`, `on`, or `off`")
            return

        if not os.path.exists(".lifx_disabled"):
            ran = False
            while not ran:
                try:
                    if cmd == "off":
                        self.light.set_power(False)
                    elif cmd == "on":
                        self.light.set_power(True)
                    elif cmd in colors:
                        self.light.set_color(colors[cmd])
                    elif cmd == "pick":
                        c = random.choice(list(colors.values()))
                        self.light.set_color(c)
                    elif cmd == "random":
                        c = [randint(0,65535), randint(0,65535), randint(0,65535), randint(0,65535),]
                    ran = True
                except Exception as e:
                    syslog.log("IOT", "LIFX error `" + str(e) + "`")
            await ctx.send("Set light to `" + cmd + "`", reference=ctx.message)
        else:
            await ctx.send("Light control is currently disabled.", reference=ctx.message)

    @commands.command()
    async def toggle_lifx(self, ctx):
        """(Bot owner only) Enable/disable light control"""
        if ctx.message.author.id == OWNER:
            if not os.path.exists(".lifx_disabled"):
                os.system("touch .lifx_disabled")
                await ctx.send("Light control is now disabled.", reference=ctx.message)
            else:
                os.remove(".lifx_disabled")
                await ctx.send("Light control is now enabled.", reference=ctx.message)
        else:
            await ctx.send("You're not the bot owner. :angry:")

def setup(bot):
    bot.add_cog(IOT(bot))