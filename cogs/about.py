from discord.ext import commands

from util_functions import *


# Hopefully we'll never need logging here


class About(commands.Cog):
    """Stuff that the developer couldn't find a better category for"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def source(self, ctx):
        """Bot source code link"""
        await ctx.send(
            embed=inf_msg(
                "Source",
                "My source code lives here: https://github.com/SomethingGeneric/gamerbot2",
            )
        )

    @commands.command()
    async def license(self, ctx):
        """Bot license file"""
        await ctx.send(
            embed=inf_msg(
                "License",
                "My license lives here: https://github.com/SomethingGeneric/gamerbot2/-/blob/main/LICENSE",
            )
        )

    @commands.command()
    async def report(self, ctx):
        """Report bot issues"""
        await ctx.send(
            embed=inf_msg(
                "Issues",
                "You can file issues here: https://github.com/SomethingGeneric/gamerbot2/issues",
            )
        )

    @commands.command()
    async def suggest(self, ctx):
        """Suggest bot feature(s)"""
        await ctx.send(
            embed=inf_msg(
                "Issues",
                "You can file issues here: https://gitlab.xhec.us/Generic/Gamerbot2/issues",
            )
        )

    @commands.command()
    async def version(self, ctx):
        """Bot version"""
        commit_msg = await run_command_shell(
            "git --no-pager log --decorate=short --pretty=oneline -n1"
        )
        msg = ""
        msg += "Latest Git commit: \n"
        msg += "```" + commit_msg + "```"
        await ctx.send(embed=inf_msg("Bot Stats", msg))

    @commands.command()
    async def invite(self, ctx):
        """Add me to another server"""
        await ctx.send(
            embed=inf_msg(
                "Invite me :)",
                "https://discord.com/api/oauth2/authorize?client_id=763559371628085288&permissions=8&scope=bot%20applications.commands",
            )
        )

    @commands.command()
    async def support(self, ctx):
        """Get support for Gamerbot"""
        await ctx.send(
            embed=inf_msg("Join our server. :)", "https://discord.gg/j4nAea7cAs")
        )


def setup(bot):
    bot.add_cog(About(bot))
