from discord.ext import commands

from global_config import ConfigManager
from util_functions import *


# Hopefully we'll never need logging here


class Debug(commands.Cog):
    """Stuff that the developer couldn't find a better category for"""

    def __init__(self, bot):
        self.bot = bot
        self.confmgr = ConfigManager("config.txt", False)

    @commands.command()
    async def check_cog(self, ctx, *, n):
        """check if cog is a thing"""
        try:
            if ctx.bot.get_cog(n) is not None:
                await ctx.send(
                    embed=inf_msg("Debug Tools", "Bot was able to find `" + n + "`")
                )
            else:
                await ctx.send(
                    embed=err_msg("Debug Tools", "Bot was not able to find `" + n + "`")
                )
        except Exception as e:
            await ctx.send(
                embed=err_msg(
                    "Debug Tools - ERROR",
                    "Had error `" + str(e) + "` while checking cog `" + n + "`",
                )
            )

    @commands.command()
    async def git_status(self, ctx):
        """Show the output of git status"""
        commit_msg = await run_command_shell(
            "git --no-pager log --decorate=short --pretty=oneline -n1"
        )
        await ctx.send(embed=inf_msg("Git Status", "```" + commit_msg + "```"))

    @commands.command()
    async def purge_syslog(self, ctx):
        """Delete all existing syslogs (USE WITH CARE) (Owner only)"""
        if ctx.message.author.id == self.bot.owner_id:
            purged = await run_command_shell("rm system_log* -v")
            await ctx.send(
                embed=inf_msg("Syslog Purger", "We purged:\n```" + purged + "```")
            )
        else:
            await ctx.send(embed=err_msg("Oops", wrong_perms("purgesyslog")))


def setup(bot):
    bot.add_cog(Debug(bot))
