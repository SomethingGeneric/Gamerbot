from discord.ext import commands
from util_functions import *


class Shell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.init_done = False

    async def extrainit(self):
        await run_command_shell(
            "/bin/bash -c \"echo 'toor' | ssh root@punchingbag 'uname'\""
        )
        await run_command_shell(
            "/bin/bash -c \"echo 'toor' | ssh-copy-id root@punchingbag\""
        )
        self.init_done = True

    @commands.command()
    async def bash(self, ctx, *, cmd):
        """Run a command"""

        if not self.init_done:
            await self.extrainit()

        with open("run_this", "w") as f:
            f.write(cmd)

        await run_command_shell("scp run_this root@punchingbag:.")

        await run_command_shell("ssh root@punchingbag 'chmod +x run_this'")

        output = await run_command_shell("ssh root@punchingbag './run_this'")

        await run_command_shell("ssh root@punchingbag 'rm run_this'")

        msg = ""

        if len(output) > 1000:
            link = await paste(output)
            msg = f"See output: {link}"
        else:
            msg = f"```{output}```"

        await ctx.send(msg, reference=ctx.message)


async def setup(bot):
    await bot.add_cog(Shell(bot))
