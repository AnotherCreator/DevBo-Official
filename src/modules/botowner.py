# ---       IMPORTS          ---#

import discord
from discord.ext import commands

# ---       MAIN LINE       ---#


class BotOwner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def updatelogs(self, ctx, message):
        # 'update-notes' channel
        channel = self.bot.get_channel(768626068629880902)
        embed = discord.Embed(
            title=f'{message}',
            description='',
            colour=discord.Colour.blurple()
        )

        await ctx.channel.send(embed=embed)


# ---       END MAIN        ---#
def setup(bot):
    bot.add_cog(BotOwner(bot))
