# ---       IMPORTS          ---#

import discord
from discord.ext import commands
from time import sleep

# ---       MAIN LINE       ---#
from discord.ext.commands import MissingRequiredArgument


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # TODO: Add kick command
    @commands.command()
    async def kick (self, ctx, message):
        embed = discord.Embed(

        )
        await ctx.send(message)

    # TODO: Add ban command
    @commands.command()
    async def ban(self, ctx, message):
        embed = discord.Embed(

        )
        await ctx.send(embed=embed)

    # TODO: Add prune command
    @commands.command()
    async def prune(self, ctx, amount):
        try:
            await ctx.channel.purge(limit=int(amount) + 1)
            embed = discord.Embed(
                title=f'Successfully removed {amount} messages',
                description=' ',
                colour=discord.Colour.blurple()
            )
            await ctx.send(embed=embed, delete_after=5)
        except commands.MissingRequiredArgument:
            embed = discord.Embed(
                title='Error: Specify the amount of messages to be removed',
                description=' ',
                colour=discord.Colour.red()
            )
            embed.set_footer(text='ex => ;prune 5')
            await ctx.send(embed=embed)

    # TODO: Add mute command
    # Create some function that applies a 'mute' role
    # Creates a 'mute' role if it does not previously exist (Possibly easier to pre-make ...
    # ... a mute role then apply it via function)
    @commands.command()
    async def mute(self, ctx, message):
        embed = discord.Embed(

        )
        await ctx.send(message)


# ---       END MAIN        ---#
def setup(bot):
    bot.add_cog(Admin(bot))
