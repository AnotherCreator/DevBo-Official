# ---       IMPORTS          ---#


import discord
from discord.ext import commands

# ---       GLOBAL VARIABLES          ---#

bot_avatar_link = 'https://cdn.discordapp.com/avatars/733004304855597056/d55234172599dca4b11e6345078a32b0.png?size=128'

# ---       MAIN LINE       ---#


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title='Use ``;more [Module Name]`` to get more info',
            description='• Administration\n'
                        '• Info\n'
                        '• Market\n'
                        '• Experimental',
            colour=discord.Colour.blurple()
        )
        embed.set_author(name='Commands List',
                         icon_url=bot_avatar_link)

        await ctx.send(embed=embed)

    @commands.command()
    async def more(self, ctx, module):
        if module == 'Administration' or module == 'administration' or module == 'Admin' or module == 'admin':
            embed = discord.Embed(
                title='Administration',
                description=' ',
                colour=discord.Colour.blurple()
            )
            embed.set_author(name='Commands List', icon_url=bot_avatar_link)
            embed.add_field(name='UNDER CONSTRUCTION',
                            value='COMING SOON',
                            inline=False)

            await ctx.send(embed=embed)
        elif module == 'Info' or module == 'info':
            embed = discord.Embed(
                title='Info',
                description=' ',
                colour=discord.Colour.blurple()
            )
            embed.set_author(name='Commands List', icon_url=bot_avatar_link)
            embed.add_field(name=';ping', value='pong!',
                            inline=False)
            await ctx.send(embed=embed)
        elif module == 'Market' or module == 'market':
            embed = discord.Embed(
                title='Market',
                description=' ',
                colour=discord.Colour.blurple()
            )
            embed.set_author(name='Commands List', icon_url=bot_avatar_link)
            embed.add_field(name=';crypto [1-50]',
                            value='Displays Name / Current Price / Percent Change',
                            inline=False)
            embed.add_field(name=';cryptolist [1-5]',
                            value='Displays the top 50 coins',
                            inline=False)

            await ctx.send(embed=embed)
        elif module == 'Experimental' or module == 'experimental' or module == 'Experiment' or module == 'experiment':
            embed = discord.Embed(
                title='Experimental',
                description=' ',
                colour=discord.Colour.blurple()
            )
            embed.set_author(name='Commands List', icon_url=bot_avatar_link)
            embed.add_field(name=';pic',
                            value='Displays a randomly AI generated character',
                            inline=False)
            embed.add_field(name=';stool',
                            value='Your portable high-ground',
                            inline=False)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title='Invalid Command',
                description=' ',
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
