# ---       IMPORTS         --- #
import discord
from discord.ext import commands
from pybo import BOT_AVATAR


# ---     CUSTOM CHECKS     --- #
def bot_channel_check(ctx):
    botspam_channels = ['bot-spam', 'bot-commands']
    if str(ctx.message.channel) in botspam_channels or ctx.author.id == 291005201840734218:
        return True


# ---       MAIN LINE       --- #
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(bot_channel_check)
    async def help(self, ctx, module=None):
        await ctx.message.delete()  # Deletes command call
        if module is None:
            embed = discord.Embed(
                title='Use *;help* __*Module Name*__ to get more info',
                description='• Administration\n'
                            '• Info\n'
                            '• Market\n'
                            '• Experimental',
                colour=discord.Colour.blurple()
            )
            embed.set_author(name='Commands List',
                             icon_url=BOT_AVATAR)
            await ctx.send(embed=embed)
        elif module == 'Administration' or module == 'administration' or module == 'Admin' or module == 'admin':
            embed = discord.Embed(
                title='Administration',
                description=' ',
                colour=discord.Colour.blurple()
            )
            embed.set_author(name='Commands List', icon_url=BOT_AVATAR)
            embed.add_field(name=';prune __Amount__',
                            value='Removes the amount of messages specified',
                            inline=False)
            embed.add_field(name=';mute __@user / user ID__',
                            value='Mutes the specified user',
                            inline=False)
            embed.add_field(name=';unmute __@user / user ID__',
                            value='Unmutes the specified user',
                            inline=False)
            embed.set_footer(text='User IDs can be found by turning on "Developer Mode"')

            await ctx.send(embed=embed)
        elif module == 'Info' or module == 'info':
            embed = discord.Embed(
                title='Info',
                description=' ',
                colour=discord.Colour.blurple()
            )
            embed.set_author(name='Commands List', icon_url=BOT_AVATAR)
            embed.add_field(name=';ping', value='pong!',
                            inline=False)
            await ctx.send(embed=embed)
        elif module == 'Market' or module == 'market':
            embed = discord.Embed(
                title='Market',
                description=' ',
                colour=discord.Colour.blurple()
            )
            embed.set_author(name='Commands List', icon_url=BOT_AVATAR)
            embed.add_field(name=';coin __1-100__ or ;coin __name__',
                            value='Displays Name / Current Price',
                            inline=False)
            embed.add_field(name=';top __1-100__',
                            value='Displays the top # coins',
                            inline=False)

            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title='Invalid Command',
                description=' ',
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)


# ---       END MAIN            ---#
def setup(bot):
    bot.add_cog(Help(bot))
