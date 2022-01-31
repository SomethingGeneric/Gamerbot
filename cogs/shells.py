import os, re, random

import discord
from discord.ext import commands

import asyncio

from util_functions import *
from server_config import serverconfig


class Shells(commands.Cog):
    """Bash, Python, and others"""

    def __init__(self, bot):
        self.bot = bot
        self.confmgr = configboi("config.txt", False)

        self.bash_priv = self.confmgr.getasbool("BASH_PRIV")
        self.bash_sandboxed = self.confmgr.getasbool("BASH_SANDBOXED")
        self.do_python = self.confmgr.getasbool("PYTHON_SHELL")

        self.not_allowed = [
            "/",
            "../",
            "sudo",
            "rm",
            "mv",
            "cp",
            "sed",
            "cd",
            "shutdown",
            "poweroff",
            "reboot",
            "{",
            "}",
            "()",
            ":(){ :|:& };:",
            ":(){",
            "/dev/urandom",
            "/dev",
            "/etc",
            "gamerbot",
            "gamerbot2",
            "token",
            "~/token",
            "~",
            "/proc",
        ]

    async def handle_bash(self, ctx, privileged=False, cmd=""):

        prepend = ""
        append = ""

        if not privileged:
            dir = await run_command_shell("mktemp -d")

            prepend = "cd " + dir + " && "
            append = " && cd ../"

            if "/etc/systemd" in cmd or "token" in cmd:
                await ctx.send(
                    embed=errmsg(
                        "Shells error",
                        "You're a whore",
                    ),
                    reference=ctx.message,
                )

            if " " in cmd:
                bits = cmd.split(" ")
                for bit in bits:
                    if bit in self.not_allowed:
                        await ctx.send(
                            embed=errmsg(
                                "Shells error",
                                "The command `"
                                + bit
                                + "` is not allowed in unprivileged shells",
                            ),
                            reference=ctx.message,
                        )
                        return
            else:
                if cmd in self.not_allowed:
                    await ctx.send(
                        embed=errmsg(
                            "Shells error",
                            "The command `"
                            + cmd
                            + "` is not allowed in unprivileged shells",
                        ),
                        reference=ctx.message,
                    )
                    return

        if "\n" in cmd:
            cmd = cmd.split("\n")[0]

        out = await run_command_shell(prepend + cmd + append)

        if len(out) == 0:
            await ctx.send(
                embed=infmsg("Shells: `" + cmd + "`", "Returned nothing"),
                reference=ctx.message,
            )
        elif len(out) > 1000:
            url = paste(out)
            await ctx.send(
                embed=infmsg("Shells: Paste URL", "Output was too long. See: " + url),
                reference=ctx.message,
            )
        else:
            await ctx.send(
                embed=infmsg("Shells: `" + cmd + "`", "```" + out + "```"),
                reference=ctx.message,
            )

    @commands.command()
    async def priv_bash(self, ctx, *, cmd: str):
        """Bash commands w/o sandboxing. (Must be admin or mod)"""
        if not self.bash_priv:
            await ctx.send(
                embed=errmsg(
                    "Shells error",
                    ctx.message.author.mention + ", privileged shells are not enabled.",
                )
            )
        else:  # it's enabled, but is this user allowed?
            if (
                ctx.message.author.id in MOD_IDS or ctx.message.author.id == OWNER
            ):  # yes they are
                await self.handle_bash(ctx, True, cmd)
            else:
                await ctx.send(
                    embed=errmsg(
                        "Shells error",
                        ctx.message.author.mention
                        + ", you don't have permission to use privileged shells.",
                    )
                )

    @commands.command()
    async def bash(self, ctx, *, cmd: str):
        """Run bash shell commands. No, not forkbombs or rm /"""
        if not self.bash_sandboxed:
            await ctx.send(
                embed=errmsg(
                    "Shells error",
                    ctx.message.author.mention + ", bash shells are not enabled.",
                )
            )
        else:  # it's enabled
            await self.handle_bash(ctx, False, cmd)

    @commands.command()
    async def pyval(self, ctx, *, expr: str):
        """Run expression with python's eval() function"""
        expr = expr.replace(";", "").replace("import", "")
        dont = False
        for evil in self.not_allowed:
            if evil in expr:
                dont = True
                cmd = evil
        if not dont:
            out = str(eval(expr))
            await ctx.send(embed=infmsg("Shells", "```" + out + "```"))
        else:
            await ctx.send(
                embed=errmsg(
                    "Shells error",
                    "The command `" + cmd + "` is not allowed in unprivileged shells",
                )
            )

    @commands.command()
    async def sysinfo(self, ctx):
        """Show system stats"""
        nofetch = await run_command_shell("nofetch")
        notop = await run_command_shell("notop sysinfo")

        text = "```" + nofetch + "\n\n" + notop + "```"

        embed = infmsg(
            "System Stats", text, footnote="Thanks to jnats for notop and nofetch"
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Shells(bot))
