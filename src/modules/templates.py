# ---       IMPORTS          ---#

import discord
from discord.ext import commands

# ---       MAIN LINE       ---#


class Templates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def template(self, ctx):
        embed = discord.Embed(
            title='Title',
            description='This is a description',
            colour=discord.Colour.blurple()
        )

        embed.set_footer(text='This is a footer.')
        embed.set_image(
            url=ctx.avatar_url)
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/445104854327623692/604275896202821632'
            '/Self-potrait_Shading.png'
        )
        embed.set_author(name='Author Name',
                         icon_url='https://cdn.discordapp.com/attachments/445104854327623692'
                                  '/604275896202821632/Self-potrait_Shading.png')
        embed.add_field(name='Field Name', value='Field Value', inline=False)
        embed.add_field(name='Field Name', value='Field Value', inline=True)
        embed.add_field(name='Field Name', value='Field Value', inline=True)

        await ctx.send(embed=embed)

    # TODO: Add a server 'template' that allows a user to type a command which makes the bot send multiple ...
    # TODO: ... messages that introduces all the majority of its commands (excluding administration commands)
    # TODO: Administration commands can go in a separate 'mod only' chat


# ---       END MAIN        ---#
def setup(bot):
    bot.add_cog(Templates(bot))
