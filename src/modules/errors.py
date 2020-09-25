# ---       IMPORTS          ---#


import discord
from discord.ext import commands

# ---       MAIN LINE       ---#


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# ---       END MAIN        ---#
def setup(bot):
    bot.add_cog(Errors(bot))