# ---       IMPORTS          ---#

import discord
from discord.ext import commands

# ---       MAIN LINE          ---#


class BotOwner(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def updatelog(self, ctx, message):
        channel = self.bot.get_channel(768626068629880902)

        embed = discord.Embed(
            title=f'{message}',
            description='',
            colour=discord.Color.blurple()
        )
        await channel.send(embed=embed)





def setup(bot):
    bot.add_cog(BotOwner(bot))
