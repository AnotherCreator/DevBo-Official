# ---       IMPORTS          ---#

import discord
from discord.ext import commands

# ---       MAIN LINE       ---#


class BotOwner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# ---       END MAIN        ---#
def setup(bot):
    bot.add_cog(BotOwner(bot))
