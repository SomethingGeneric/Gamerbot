import os, re, random

import discord
from discord.ext import commands

import asyncio

from util_functions import *

# Use isup in here perhaps?


class Shells(commands.Cog):
    """Bash, Python, and others"""

    def __init__(self, bot):
        self.bot = bot
        self.confmgr = configboi("config.txt", False)

        self.bash_priv = self.confmgr.getasbool("BASH_PRIV")
        self.bash_sandboxed = self.confmgr.getasbool("BASH_SANDBOXED")
        self.sandbox_ssh_tgt = self.confmgr.get("SANDBOX_SSH_TGT")

        self.shell_channels = []

        if os.path.exists(".shellchannels"):
            with open(".shellchannels") as f:
                channels = f.read().strip().split("\n")
            for chan in channels:
                self.shell_channels.append(int(chan))

    def cog_unload(self):
        if os.path.exists(".notools_setupdone"):
            os.remove(".notools_setupdone")

    async def handle_bash(self, ctx=None, msg=None, privileged=False, cmd=""):

        prepend = ""
        append = ""

        if not privileged:
            prepend = "ssh " + self.sandbox_ssh_tgt + ' "'
            append = '"'

        if "\n" in cmd:
            cmd = cmd.split("\n")[0]

        out = await run_command_shell(prepend + cmd + append)

        if len(out) == 0:
            if ctx != None:
                await ctx.send(
                    embed=infmsg("Shells: `" + cmd + "`", "Returned nothing"),
                    reference=ctx.message,
                )
        elif len(out) > 1000:
            url = paste(out)
            if ctx != None:
                await ctx.send(
                    embed=infmsg(
                        "Shells: Paste URL", "Output was too long. See: " + url
                    ),
                    reference=ctx.message,
                )
            elif msg != None:
                await msg.channel.send(
                    embed=infmsg(
                        "Shells: Paste URL", "Output was too long. See: " + url
                    ),
                    reference=msg,
                )
            else:
                print("Neither response option was valid")
        else:
            if ctx != None:
                await ctx.send(
                    embed=infmsg("Shells: `" + cmd + "`", "```" + out + "```"),
                    reference=ctx.message,
                )
            elif msg != None:
                await msg.channel.send(out)
            else:
                print("Neither response option was valid")

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
            if await self.bot.is_owner(ctx.message.author):  # yes they are
                await self.handle_bash(ctx=ctx, privileged=True, cmd=cmd)
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
            await self.handle_bash(ctx=ctx, privileged=False, cmd=cmd)

    async def ensure_notools(self):
        if not os.path.exists(".notools_setupdone"):
            await run_command_shell(
                "wget https://git.tar.black/notools/notop/-/raw/master/notop -O bin/notop && chmod +x bin/notop"
            )
            await run_command_shell(
                "wget https://git.tar.black/notools/nofetch/-/raw/master/nofetch -O bin/nofetch && chmod +x bin/nofetch"
            )

            prepend = "ssh " + self.sandbox_ssh_tgt + ' "'
            append = '"'

            await run_command_shell(
                prepend
                + "mkdir -p bin ; wget https://git.tar.black/notools/notop/-/raw/master/notop -O bin/notop && chmod +x bin/notop"
                + append
            )
            await run_command_shell(
                prepend
                + "wget https://git.tar.black/notools/nofetch/-/raw/master/nofetch -O bin/nofetch && chmod +x bin/nofetch"
                + append
            )

            with open(".notools_setupdone", "w") as f:
                f.write("yea")

    @commands.Cog.listener("on_message")
    async def msg_func(self, message):
        await self.ensure_notools()

    @commands.command()
    async def sysinfo(self, ctx):
        """Show system stats"""
        nofetch = await run_command_shell("./bin/nofetch")
        notop = await run_command_shell("./bin/notop sysinfo")

        text = "```" + nofetch + "\n\n" + notop + "```"

        embed = infmsg(
            "Host system Stats", text, footnote="Thanks to jnats for notop and nofetch"
        )

        await ctx.send(embed=embed)

        prepend = "ssh " + self.sandbox_ssh_tgt + ' "'
        append = '"'

        nofetch = await run_command_shell(prepend + "./bin/nofetch" + append)
        notop = await run_command_shell(prepend + "./bin/notop sysinfo" + append)

        text = "```" + nofetch + "\n\n" + notop + "```"

        embed = infmsg(
            "Bash system Stats", text, footnote="Thanks to jnats for notop and nofetch"
        )

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            message.channel.id in self.shell_channels
            and message.author != self.bot.user
            and message.content != "-makeshellchannel"
        ):
            await self.handle_bash(msg=message, privileged=False, cmd=message.content)

    @commands.command()
    async def makeshellchannel(self, ctx):
        adm = False
        for role in ctx.message.author.roles:
            if role.name == "gb_mod":
                adm = True

        if adm:
            self.shell_channels.append(ctx.message.channel.id)
            with open(".shellchannels", "a+") as f:
                f.write(str(ctx.message.channel.id) + "\n")
            await ctx.send("Done!")
        else:
            await ctx.send("You're not a mod")


def setup(bot):
    bot.add_cog(Shells(bot))
