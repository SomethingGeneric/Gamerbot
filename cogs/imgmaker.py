import os, re, random, asyncio
from tempfile import TemporaryFile

import discord
from discord.ext import commands

import asyncio
from PIL import Image, ImageDraw, ImageFont

from util_functions import *


# Hopefully we'll never need logging here
# (but who knows)

# Start memes
class ImageMaker(commands.Cog):
    """Haha image manipulation go brr"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def figlet(self, ctx, *, text):
        """Fun text art :)"""
        try:
            out = await run_command_shell("figlet " + text.strip())
            if len(out) < 1994:
                await ctx.send("```\n " + str(out) + "```")
            else:
                link = paste(out)
                await ctx.send(
                    ctx.message.author.mention
                    + ", the figlet output is too long, so here's a link: "
                    + link
                )
        except Exception as e:
            await ctx.send(
                embed=errmsg("Error", "Had an issue running figlet: `" + str(e) + "`")
            )
            syslog.log(
                "Memes-Important", "Had an issue running figlet: `" + str(e) + "`"
            )

    @commands.command()
    async def bonk(self, ctx, *, text=""):
        """Bonk a buddy"""

        if text == "":
            text = ctx.message.author.mention

        newtext = text.strip()
        extra = ""

        if "<@!" in newtext or "<@" in newtext:
            try:
                pid = newtext.replace("<@!", "").replace("<@", "").replace(">", "")
                person = await self.bot.fetch_user(int(pid))
                if person != None:
                    newtext = person.display_name
                    extra = "Get bonked, " + person.mention
                else:
                    await ctx.send("Had trouble getting a user from: " + text)
            except Exception as e:
                await ctx.send("We had a failure: `" + str(e) + "`")

        if newtext != "":
            img = Image.open("images/bonk.png")
            bfont = ImageFont.truetype("fonts/arial.ttf", (50 - len(str(newtext))))
            draw = ImageDraw.Draw(img)
            draw.text(
                (525 - len(str(newtext)) * 5, 300),
                str(newtext),
                (0, 0, 0),
                font=bfont,
            )
            img.save("bonk-s.png")
            await ctx.send(extra, file=discord.File("bonk-s.png"))
            os.remove("bonk-s.png")
        else:
            await ctx.send(file=discord.File("images/bonk.png"))

    @commands.command()
    async def space(self, ctx, *, who):
        """Send ur friends to space lol"""
        user = who.strip()

        if "<@!" in user or "<@" in user:
            try:
                pid = user.replace("<@!", "").replace("<@", "").replace(">", "")
                person = await self.bot.fetch_user(int(pid))
                if person != None:
                    pfp = str(person.avatar_url)
                    os.system("wget " + pfp + " -O prof.webp")
                    bg = Image.open("images/spacex.jpg")
                    fg = Image.open("prof.webp")
                    fg = fg.resize((128, 128))
                    bg.paste(fg, (620, 0), fg.convert("RGBA"))
                    bg.save("temp.png")
                    await ctx.send(
                        ":rocket::sparkles: See ya later "
                        + person.mention
                        + " :sparkles::rocket:",
                        file=discord.File("temp.png"),
                    )
                    os.remove("temp.png")
                    os.remove("prof.webp")
                else:
                    await ctx.send("Had trouble getting a user from: " + text)
            except Exception as e:
                await ctx.send("We had a failure: `" + str(e) + "`")
        else:
            await ctx.send(
                ctx.message.author.mention + ", who are you sending to space?"
            )

    @commands.command()
    async def pfp(self, ctx, *, who):
        """Yoink a cool PFP from a user"""
        user = who.strip()

        if "<@!" in user or "<@" in user:
            try:
                pid = user.replace("<@!", "").replace("<@", "").replace(">", "")
                person = await self.bot.fetch_user(int(pid))
                if person != None:
                    pfp = str(person.avatar_url)
                    await ctx.send(ctx.message.author.mention + " here: " + pfp)
                else:
                    await ctx.send("Had trouble getting a user from: " + text)
            except Exception as e:
                await ctx.send("We had a failure: `" + str(e) + "`")
        else:
            await ctx.send(ctx.message.author.mention + ", that ain't a user.")


# End memes
def setup(bot):
    bot.add_cog(ImageMaker(bot))
