# ---       IMPORTS          ---#


import discord
from discord.ext import commands

# ---       MAIN LINE       ---#


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # TODO: Add kick command
    # TODO: Add ban command
    # TODO: Add prune command
    # TODO: Add mute command
        # Create some function that applies a 'mute' role
        # Creates a 'mute' role if it does not previously exist (Possibly easier to pre-make ...
        # ... a mute role then apply it via function)


# ---       END MAIN        ---#
def setup(bot):
    bot.add_cog(Admin(bot))