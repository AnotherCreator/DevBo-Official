# ---       IMPORTS          ---#
import discord

from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from pybo import guild_ids


# ---     CUSTOM CHECKS     --- #
def bot_channel_check(ctx):
    botspam_channels = ['bot-spam']
    if str(ctx.message.channel) in botspam_channels or ctx.author.id == 291005201840734218:
        return True


# ---       MAIN LINE       ---#
class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ---       SLASH COMMANDS       --- #
    @cog_ext.cog_slash(
        name='info',
        description='',
        guild_ids=guild_ids,
        options=[
            create_option(
                name='option',
                description='Choose category!',
                required=True,
                option_type=3,
                choices=[
                    create_choice(
                        name='ping',
                        value='ping'
                    )
                ]
            )
        ]
    )
    async def _help(self, ctx: SlashContext, option: str):
        if option == 'ping':
            embed = discord.Embed(
                title=f'Pong! {str(round(self.bot.latency * 1000))}ms',
                colour=discord.Colour.blurple()
            )
        await ctx.send(embeds=[embed])

    # ---       PREFIX COMMANDS       --- #
    # @commands.command()
    # @commands.check(bot_channel_check)
    # async def ping(self, ctx):
    #     embed = discord.Embed(
    #         title=f'Pong! {str(round(self.bot.latency * 1000))}ms',
    #         colour=discord.Colour.blurple()
    #     )
    #     await ctx.send(embed=embed)


# ---       END MAIN        ---#
def setup(bot):
    bot.add_cog(Info(bot))
