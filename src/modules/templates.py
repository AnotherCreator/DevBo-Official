import discord
from discord.ext import commands

from src.pybo import bot_owner_check


class Templates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Commands
    @commands.command()
    @commands.check(bot_owner_check)
    async def template(self, ctx):
        embed = discord.Embed(
            title='Title',
            description='This is a description',
            colour=discord.Colour.blurple()
        )

        embed.set_footer(text='This is a footer.')
        embed.set_image(
            url='https://cdn.discordapp.com/attachments/445104854327623692/604275896202821632'
                '/Self-potrait_Shading.png')
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/445104854327623692/604275896202821632'
                '/Self-potrait_Shading.png')
        embed.set_author(name='Author Name',
                         icon_url='https://cdn.discordapp.com/attachments/445104854327623692'
                                  '/604275896202821632/Self-potrait_Shading.png')
        embed.add_field(name='Field Name', value='Field Value', inline=False)
        embed.add_field(name='Field Name', value='Field Value', inline=True)
        embed.add_field(name='Field Name', value='Field Value', inline=True)

        await ctx.send(embed=embed)


# ---       END MAIN        ---#
def setup(bot):
    bot.add_cog(Templates(bot))
