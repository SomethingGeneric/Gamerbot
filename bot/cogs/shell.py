from discord.ext import commands
from util_functions import *


class Shell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reset_bash(self, ctx, confirm="n"):
        """Reset my bash access"""
        try:
            if confirm == "y":
                un = ctx.message.author.name.lower()
                un = un.replace("-", "").replace("_", "")
                if un[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    un = un[1:]
                await ctx.send("Resetting your user.", reference=ctx.message)
                await run_command_shell(
                    f"ssh punchingbag 'userdel {un} && rm -rf /home/{un}'"
                )
                await ctx.send("Done.", reference=ctx.message)
            else:
                await ctx.send(
                    "Just to confirm, you want to nuke your bash user. If so, re-run with `-reset_bash y`",
                    reference=ctx.message,
                )
        except Exception as e:
            await ctx.send(f"Error: ```{str(e)}```", reference=ctx.message)

    @commands.command()
    async def bash(self, ctx, *, cmd):
        """Run a command"""
        try:

            if ":(){ :|:& };:" in cmd:
                await ctx.send("No forkbombs", reference=ctx.message)
                return

            un = ctx.message.author.name.lower()
            un = un.replace("-", "").replace("_", "")
            if un[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                un = un[1:]

            await run_command_shell("scp /bot/bin/has_user punchingbag:.")
            test_user = await run_command_shell(f"ssh punchingbag './has_user {un}'")

            if "n" in test_user:  # no user
                await run_command_shell("scp /bot/bin/mk_user punchingbag:.")
                await run_command_shell(f"ssh punchingbag './mk_user {un}'")

            with open("run_this", "w") as f:
                f.write(cmd)

            await run_command_shell(f"scp run_this {un}@punchingbag:.")

            await run_command_shell(f"ssh {un}@punchingbag 'chmod +x run_this'")

            output = await run_command_shell(f"ssh {un}@punchingbag './run_this'")

            await run_command_shell(f"ssh {un}@punchingbag 'rm run_this'")

            msg = ""

            if len(output) > 1000:
                link = await paste(output)
                msg = f"See output: {link}"
            else:
                if len(output) != 0:
                    msg = f"```{output}```"
                else:
                    msg = "No output"

            await ctx.send(msg, reference=ctx.message)
        except Exception as e:
            await ctx.send(f"Error: ```{str(e)}```")


async def setup(bot):
    await bot.add_cog(Shell(bot))
