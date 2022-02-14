import os, re, random

import discord
from discord.ext import commands

import asyncio
from PIL import Image, ImageDraw, ImageFont

from util_functions import *


# Hopefully we'll never need logging here
# (but who knows)

# Start memes
class Memes(commands.Cog):
    """Haha image manipulation go brr"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
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
        }

        if message.author != self.bot.user:
            if "crystalux" in mc.lower():
                await mchan.send(
                    "Stop deadnaming Crystal Linux :angry:", reference=message
                )
                await mchan.send("(And stop deadnaming in general)")
            elif "hello there" in mc:
                await mchan.send(
                    "General Kenobi\nhttps://media1.giphy.com/media/UIeLsVh8P64G4/giphy.gif",
                    reference=message,
                )
            else:
                try:
                    if " " in mc:
                        tw = 0
                        act = ""
                        for word in mc.split(" "):
                            if word in triggers:
                                tw += 1
                                act = word
                        if tw == 1:
                            await mchan.send(triggers[act], reference=message)
                        elif tw > 1:
                            await mchan.send(
                                message.author.mention + " don't be an asshat. :angry:",
                                reference=message,
                            )
                    else:
                        if mc in triggers:
                            await mchan.send(triggers[mc], reference=message)
                except Exception as e:
                    await mchan.send(embed=errmsg("Error", "```" + str(e) + "```"))

            if "comrade sharkfact" in mc:
                with open("data/sharkfacts.txt", encoding="cp1252") as f:
                    sharkList = f.read().split("\n")
                await mchan.send(
                    embed=infmsg("Sharkfact", random.choice(sharkList)),
                    reference=message,
                )

            if DO_IMAGE_RESPONSE:
                if random.randint(
                    1, IMAGE_RESPONSE_PROB
                ) == IMAGE_RESPONSE_PROB and "filename" in str(message.attachments):
                    await mchan.send(random.choice(IMAGE_RESPONSES), reference=message)

    @commands.command()
    async def figlet(self, ctx, *, text):
        """Fun text art :)"""
        try:
            out = await run_command_shell("figlet " + strip_dangerous(text.strip()))
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

    @commands.command(hidden=True)
    async def ivp(self, ctx, fake, real):
        await ctx.message.delete()
        await ctx.send(
            fake
            + "||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||"
            + real
        )


# End memes
def setup(bot):
    bot.add_cog(Memes(bot))
