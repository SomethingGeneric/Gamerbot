import os, re, random
from random import randint

import discord
from discord.ext import commands

import asyncio

from util_functions import *


from lifxlan import *


class IOT(commands.Cog):
    """IOT Things"""

    def __init__(self, bot):
        self.bot = bot
        self.light = Light(LIFX_MAC, LIFX_IP)

    def hex_to_hsbk(self, hex):
        rgb = tuple(int(hex[i : i + 2], 16) for i in (0, 2, 4))
        r = rgb[0] / 255
        g = rgb[1] / 255
        b = rgb[2] / 255
        # R, G, B values are divided by 255
        # to change the range from 0..255 to 0..1:
        r, g, b = r / 255.0, g / 255.0, b / 255.0

        # h, s, v = hue, saturation, value
        cmax = max(r, g, b)  # maximum of r, g, b
        cmin = min(r, g, b)  # minimum of r, g, b
        diff = cmax - cmin  # diff of cmax and cmin.

        # if cmax and cmax are equal then h = 0
        if cmax == cmin:
            h = 0

        # if cmax equal r then compute h
        elif cmax == r:
            h = (60 * ((g - b) / diff) + 360) % 360

        # if cmax equal g then compute h
        elif cmax == g:
            h = (60 * ((b - r) / diff) + 120) % 360

        # if cmax equal b then compute h
        elif cmax == b:
            h = (60 * ((r - g) / diff) + 240) % 360

        # if cmax equal zero
        if cmax == 0:
            s = 0
        else:
            s = (diff / cmax) * 100

        # compute v
        v = cmax * 100

        hue_lifx = int(round(0x10000 * h) / 360) % 0x10000
        saturation_lifx = int(round(0xFFFF * s / 100))
        brightness = 65535  # could be specified by the user with an extra arg
        kelvin = 4000  # could be specified by the user with an extra arg

        return [hue_lifx, saturation_lifx, brightness, kelvin]

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
            "crystal": [50929, 65535, 65535, 4000],
            "titties": [59313, 61439, 65535, 4000],
            "acid": [33595, 62384, 65535, 4000],
        }

        if not isinstance(ctx.channel, discord.channel.DMChannel):
            if cmd == "":
                i = "Colors: "
                for c in colors.keys():
                    i += "`" + c + "`, "
                await ctx.send(i)
                await ctx.send("You can also say `random`, `sample`, `on`, or `off`")
                return
            elif "#" in cmd:
                tmp = cmd.replace("#", "")
                cmd = self.hex_to_hsbk(tmp)

            if not os.path.exists(".lifx_disabled"):
                try:
                    if type(cmd) == list:
                        self.light.set_color(cmd)
                    else:
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
                            c = [
                                randint(0, 65535),
                                randint(0, 65535),
                                randint(0, 65535),
                                randint(0, 65535),
                            ]
                            self.light.set_color(c)
                            await ctx.send("Color code: `" + str(c) + "`")
                        else:
                            self.light.set_color(cmd)
                    await ctx.send(
                        "Set light to `" + str(cmd) + "`", reference=ctx.message
                    )
                except Exception as e:
                    syslog.log("IOT", "LIFX error `" + str(e) + "`")
                    emsg = await ctx.send("LIFX Error: ```" + str(e) + "```")
                    if isinstance(e, WorkflowException):
                        await ctx.send(
                            "Since this is a case of the light being non-responsive, it's safe to try again.",
                            reference=emsg,
                        )
            else:
                await ctx.send(
                    "Light control is currently disabled.", reference=ctx.message
                )
        else:
            await ctx.send(
                "Use this in a server, coward. :angry:", reference=ctx.message
            )

    @commands.command()
    async def toggle_lifx(self, ctx):
        """(Bot owner only) Enable/disable light control"""
        if ctx.message.author.id == self.bot.owner_id:
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
