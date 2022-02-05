import os, re, random

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
        self.light = Light("d0:73:d5:03:58:0d", "10.0.0.33")

    @commands.command()
    async def lifx(self, ctx, *, cmd):
        """Set Matt's light to a color or 'random'"""
        colors = {
            "red": RED,
            "orange": ORANGE,
            "yellow": YELLOW,
            "green": GREEN,
            "cyan": CYAN,
            "blue": BLUE,
            "purple": PURPLE,
            "pink": PINK
        }
        if not not os.path.exists(".lifx_disabled"):
            ran = False
            while not ran:
                try:
                    if cmd == "" or cmd == None or cmd == "off":
                        self.light.set_power(False)
                    elif cmd == "on":
                        self.light.set_power(True)
                    elif cmd in colors:
                        self.light.set_color(colors[cmd])
                    elif cmd == "random":
                        c = random.choice(list(colors.values()))
                        self.light.set_color(c)
                    ran = True
                except Exception as e:
                    syslog.log("IOT", "LIFX error `" + str(e) + "`")
            await ctx.send("Set light to `" + cmd + "`", reference=ctx.message)
        else:
            await ctx.send("Light control is disabled.", reference=ctx.message)

    @commands.command()
    async def toggle_lifx(self, ctx):
        """(Bot owner only) Enable/disable light control"""
        if not os.path.exists(".lifx_disabled"):
            os.system("touch .lifx_disabled")
            await ctx.send("Light control is disabled.", reference=ctx.message)
        else:
            os.remove("touch .lifx_disabled")
            await ctx.send("Light control is enabled.", reference=ctx.message)

def setup(bot):
    bot.add_cog(IOT(bot))