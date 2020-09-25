# ---       IMPORTS          ---#


import discord
import random
from discord.ext import commands

# ---       GLOBAL VARIABLES          ---#

bot_avatar_link = 'https://cdn.discordapp.com/avatars/733004304855597056/d55234172599dca4b11e6345078a32b0.png?size=128'

# ---       MAIN LINE       ---#


class Experimental(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pic(self, ctx):

        random_int = random.randint(1, 100000)

        embed = discord.Embed(
            title='',
            description='',
            colour=discord.Colour.blurple()
        )
        embed.set_image(
            url=f'https://www.thiswaifudoesnotexist.net/example-{random_int}.jpg')
        embed.set_author(
            name='This Character Does Not Exist',
            icon_url=bot_avatar_link
        )
        if str(random_int).find('69') != -1:
            embed.add_field(name='Fun Fact', value=f'Your link contains the number 69!', inline=False)
        elif str(random_int).find('420') != -1:
            embed.add_field(name='Fun Fact', value=f'Your link contains the number 420!', inline=False)
        elif str(random_int).find('420') != -1 and str(random_int).find('69') != -1:
            embed.add_field(name='Fun Fact', value=f'Your link contains the numbers 420 & 69!', inline=False)
        elif str(random_int).find('666') != -1:
            embed.add_field(name='Fun Fact', value=f'Your link contains the numbers 666!', inline=False)
        else:
            pass

        await ctx.send(embed=embed)

    @commands.command()
    async def stool(self, ctx):

        embed = discord.Embed(
            title='',
            description='',
            colour=discord.Colour.blurple()
        )
        embed.set_image(
            url='https://cdn11.bigcommerce.com/s-cziwra/images/stencil/500x659/products/2882/21466/step-stool-main-image-min__95926.1580400486.jpg?c=2&imbypass=on'
        )

        await ctx.send(embed=embed)


# ---       END MAIN        ---#
def setup(bot):
    bot.add_cog(Experimental(bot))