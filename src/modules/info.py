# ---       IMPORTS          ---#


import discord
import unicodedata
from bs4 import BeautifulSoup
from discord.ext import commands
from urllib.request import Request, urlopen

# ---       GLOBAL VARIABLES          ---#

# links
bot_avatar_link = 'https://cdn.discordapp.com/avatars/733004304855597056/d55234172599dca4b11e6345078a32b0.png?size=128'

# ---     CUSTOM CHECKS     --- #


def bot_channel_check(ctx):
    botspam_channels = ['bot-spam']
    if str(ctx.message.channel) in botspam_channels:
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
