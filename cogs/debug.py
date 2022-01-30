import discord
from discord.ext import commands

from util_functions import *
from global_config import configboi
from server_config import serverconfig

# Hopefully we'll never need logging here


class Debug(commands.Cog):
    """Stuff that the developer couldn't find a better category for"""

    def __init__(self, bot):
        self.bot = bot
        self.confmgr = configboi("config.txt", False)
        self.sconf = serverconfig()

    @commands.command()
    async def resetgd(self, ctx):
        if ctx.message.author.id == ctx.message.guild.owner_id:
            self.sconf.rs(str(ctx.message.guild.id))
            await ctx.send(":thumbsup:")

    @commands.command()
    async def checkcog(self, ctx, *, n):
        """check if cog is a thing"""
        try:
            if ctx.bot.get_cog(n) is not None:
                await ctx.send(
                    embed=infmsg("Debug Tools", "Bot was able to find `" + n + "`")
                )
            else:
                await ctx.send(
                    embed=errmsg("Debug Tools", "Bot was not able to find `" + n + "`")
                )
        except Exception as e:
            await ctx.send(
                embed=errmsg(
                    "Debug Tools - ERROR",
                    "Had error `" + str(e) + "` while checking cog `" + n + "`",
                )
            )

    @commands.command()
    async def restart(self, ctx):
        """Restart the bot (Mod. only)"""
        if ctx.message.author.id in MOD_IDS:
            await ctx.send(embed=infmsg("Sad", "Ok, restarting"))
            if ctx.voice_client is not None:
                await ctx.voice_client.disconnect()
            await ctx.bot.logout()
            syslog.log(
                "Admin-Important",
                "Bot is restarting because "
                + ctx.message.author.display_name
                + " requested we do so.",
            )
            save("restarted.txt", str(ctx.message.channel.id))
            await login(os.environ["bottoken"], bot=True)
        else:
            await ctx.send(embed=errmsg("Oops", wrongperms("restart")))

    # TODO: Move to admin file?
    @commands.command()
    async def update(self, ctx):
        """Update bot from Git, and restart (Mod. only)"""
        if ctx.message.author.id in MOD_IDS:
            await ctx.send(embed=infmsg("Updater", "Updating..."))
            syslog.log(
                "Admin-Important",
                "Bot is updating & restarting because "
                + ctx.message.author.display_name
                + " requested we do so.",
            )
            # are these being upset?
            pull_out = await run_command_shell("git pull -v")
            commit_msg = await run_command_shell(
                "git --no-pager log --decorate=short --pretty=oneline -n1"
            )
            msg = (
                "Changes:"
                + "\n```"
                + pull_out
                + "```\nCommit message:\n"
                + "```"
                + commit_msg
                + "```"
            )
            await ctx.send(embed=infmsg("Updater", msg))

            await run_command_shell("pip3 install --upgrade -r requirements.txt")
            await ctx.send(embed=infmsg("Updater", "Restarting"))
            if ctx.voice_client is not None:
                await ctx.voice_client.disconnect()
            await ctx.bot.logout()
            save("restarted.txt", str(ctx.message.channel.id))
            await login(os.environ["bottoken"], bot=True)
        else:
            await ctx.send(embed=errmsg("Oops", wrongperms("update")))

    @commands.command()
    async def chbranch(self, ctx, *, branch):
        """Switch bot's upstream to a given branch (Mod. only)"""
        if ctx.message.author.id in MOD_IDS:
            await ctx.send(embed=infmsg("Updater", "Switching branch..."))
            syslog.log(
                "Admin-Important",
                "Bot is switching branch to "
                + branch
                + " because "
                + ctx.message.author.display_name
                + " requested we do so.",
            )
            await run_command_shell("git checkout " + branch)
            await ctx.send(embed=infmsg("Updater", "Done!"))
        else:
            await ctx.send(embed=errmsg("Oops", wrongperms("chbranch")))

    @commands.command()
    async def gitstatus(self, ctx):
        """Show the output of git status"""
        commit_msg = await run_command_shell(
            "git --no-pager log --decorate=short --pretty=oneline -n1"
        )
        await ctx.send(embed=infmsg("Git Status", "```" + commit_msg + "```"))

    @commands.command()
    async def purgesyslog(self, ctx):
        """Delete all existing syslogs (USE WITH CARE) (Owner only)"""
        if ctx.message.author.id == OWNER:
            purged = await run_command_shell("rm system_log* -v")
            await ctx.send(embed=infmsg("Syslog Purger", "We purged:\n```" + purged + "```"))
        else:
            await ctx.send(embed=errmsg("Oops", wrongperms("purgesyslog")))


def setup(bot):
    bot.add_cog(Debug(bot))
