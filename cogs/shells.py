from discord.ext import commands

from util_functions import *


# Use isup in here perhaps?


class Shells(commands.Cog):
    """Bash, Python, and others"""

    def __init__(self, bot):
        self.bot = bot
        self.confmgr = ConfigManager("config.txt", False)

        self.bash_priv = self.confmgr.get_as_bool("BASH_PRIV")
        self.bash_sandboxed = self.confmgr.get_as_bool("BASH_SANDBOXED")

        self.shell_channels = []

        if os.path.exists(".shellchannels"):
            with open(".shellchannels") as f:
                channels = f.read().strip().split("\n")
            for chan in channels:
                self.shell_channels.append(int(chan))

    async def handle_bash(self, ctx=None, msg=None, privileged=False, cmd=""):

        prepend = ""
        append = ""

        if not privileged:
            # this is the bit that will fool people (I hope)
            fn = (
                "".join(
                    random.choice(
                        string.ascii_uppercase + string.digits + string.ascii_lowercase
                    )
                    for _ in range(64)
                )
                + ".txt"
            )

            with open(fn, "w") as f:
                f.write(cmd)

            prepend = f'podman run -h $(uname -n) crystallinux/crystal /bin/bash -c "$(cat {fn})'
            append = '"'
            cmd = ""

        out = await run_command_shell(prepend + cmd + append)

        if len(out) == 0:
            if ctx is not None:
                await ctx.send(
                    embed=inf_msg("Shells: `" + cmd + "`", "Returned nothing"),
                    reference=ctx.message,
                )
        elif len(out) > 1000:
            url = paste(out)
            if ctx is not None:
                await ctx.send(
                    embed=inf_msg(
                        "Shells: Paste URL", "Output was too long. See: " + url
                    ),
                    reference=ctx.message,
                )
            elif msg is not None:
                await msg.channel.send(
                    embed=inf_msg(
                        "Shells: Paste URL", "Output was too long. See: " + url
                    ),
                    reference=msg,
                )
            else:
                print("Neither response option was valid")
        else:
            if ctx is not None:
                await ctx.send(
                    embed=inf_msg("Shells: `" + cmd + "`", "```" + out + "```"),
                    reference=ctx.message,
                )
            elif msg is not None:
                await msg.channel.send("```\n" + out + "```")
            else:
                print("Neither response option was valid")

    @commands.command()
    async def priv_bash(self, ctx, *, cmd: str):
        """Bash commands w/o sandboxing. (Must be admin or mod)"""
        if not self.bash_priv:
            await ctx.send(
                embed=err_msg(
                    "Shells error",
                    ctx.message.author.mention + ", privileged shells are not enabled.",
                )
            )
        else:  # it's enabled, but is this user allowed?
            if await self.bot.is_owner(ctx.message.author):  # yes they are
                await self.handle_bash(ctx=ctx, privileged=True, cmd=cmd)
            else:
                await ctx.send(
                    embed=err_msg(
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
                embed=err_msg(
                    "Shells error",
                    ctx.message.author.mention + ", bash shells are not enabled.",
                )
            )
        else:  # it's enabled
            await self.handle_bash(ctx=ctx, privileged=False, cmd=cmd)

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            message.channel.id in self.shell_channels
            and message.author != self.bot.user
            and message.content != "-makeshellchannel"
        ):
            await self.handle_bash(msg=message, privileged=False, cmd=message.content)

    @commands.command()
    async def make_shell_channel(self, ctx):
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
