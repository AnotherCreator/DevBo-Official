# ---       IMPORTS          ---#
import discord
from discord.ext import commands


# ---     CUSTOM CHECKS     --- #
def bot_channel_check(ctx):
    botspam_channels = ['bot-spam']
    if str(ctx.message.channel) in botspam_channels or ctx.author.id == 291005201840734218:
        return True


# ---       MAIN LINE       ---#
class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(bot_channel_check)
    async def ping(self, ctx):
        embed = discord.Embed(
            title=f'Pong! {str(round(self.bot.latency * 1000))}ms',
            colour=discord.Colour.blurple()
        )
        await ctx.send(embed=embed)


# ---       END MAIN        ---#
def setup(bot):
    bot.add_cog(Info(bot))
