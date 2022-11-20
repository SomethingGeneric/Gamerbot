from discord.ext import commands
from util_functions import *

class Shell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    def bash(self, ctx, *, cmd):
        """Run a command"""


async def setup(bot):
    await bot.add_cog(Shell(bot))