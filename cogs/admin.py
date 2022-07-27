from discord.ext import commands

from util_functions import *


# Non-user stuff (mods/debug)
class Admin(commands.Cog):
    """Commands for guild admins"""

    def __init__(self, bot):
        self.bot = bot
        self.confmgr = ConfigManager("config.txt", False)
        self.store = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if not isinstance(message.channel, discord.channel.DMChannel):
            for guild in self.bot.guilds:
                if not os.path.exists(".setupdone_" + str(message.guild.id)):
                    found_role = False

                    for role in message.guild.roles:
                        if role.name == "gb_mod":
                            found_role = True

                    if not found_role:
                        modr = await guild.create_role(
                            name="gb_mod",
                            reason="Role used to designate who can use our admin commands.",
                        )

                    found = False
                    for member in guild.members:
                        if await self.bot.is_owner(member):
                            found = True

                    await guild.owner.send(
                        "Hi! You should add your trusted server members of `"
                        + str(guild.name)
                        + "` to the role `gb_mod`"
                    )
                    if not found:
                        await guild.owner.send(
                            "You should also invite the bot's owner to this guild ;)"
                        )
                    with open(".setupdone_" + str(message.guild.id), "w") as f:
                        f.write("THIS IS THE NEWER VERSION OF THE LOCKFILE")

    def check_mod(self, member):
        for role in member.roles:
            if role.name == "gb_mod":
                return True
        return False


def setup(bot):
    bot.add_cog(Admin(bot))


# End non-user stuff
