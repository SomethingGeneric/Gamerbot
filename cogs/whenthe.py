import discord
from discord.ext import commands

from util_functions import *

# i hope this works

class WhenThe(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def whenthe(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/732599669867413505/921838252275695686/7Vcj8V5vrrN7G71g.mp4")

def setup(bot):
    bot.add_cog(WhenThe(bot))
