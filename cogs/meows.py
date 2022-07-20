import re

from discord.ext import commands

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
        self.mm = MeowManager()
        self.keys = ["imageresponse", "snarkycomment", "sharkfact", "randommeow"]

    @commands.command()
    async def toggle_meow(self, ctx, key="", where=""):
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
            old_where = where
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
                    + old_where
                    + " : `"
                    + where
                    + "`"
                )
            else:
                await ctx.send(
                    "`"
                    + key
                    + "` is now disabled in this "
                    + old_where
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
            "kek": "🤣",
            "kekw": "🤣",
            "grr": "🦁",
            "wave": "🌊",
            "surfing": "🏄",
            "boo": "👻",
        }

        mc = message.content.lower()
        message_chan = message.channel

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

        if message.author.id == 839586494784340049:
            await message.channel.send("Fuck off discord", reference=message)

        if message.author != self.bot.user:

            if "bot" in mc:
                # we're being talked to
                if "bad" in mc and "sucks" in mc and "bot" in mc:
                    await message.channel.send(":(")

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
                        await message_chan.send(
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
                        shark_list = f.read().split("\n")
                    await message_chan.send(
                        embed=infmsg("Sharkfact", random.choice(shark_list)),
                        reference=message,
                    )


def setup(bot):
    bot.add_cog(Meows(bot))
