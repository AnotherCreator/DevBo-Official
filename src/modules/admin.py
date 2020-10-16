# ---       IMPORTS          ---#

import discord
from discord.ext import commands

# ---       MAIN LINE       ---#


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # TODO: Add kick command
    @commands.command()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, message):
        embed = discord.Embed(

        )
        await ctx.send(message)

    # TODO: Add ban command
    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, message):
        embed = discord.Embed(

        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    async def prune(self, ctx, amount):
        if int(amount) > 0:
            await ctx.channel.purge(limit=int(amount) + 1)
            embed = discord.Embed(
                title=f'Successfully removed {amount} messages',
                description=' ',
                colour=discord.Colour.blurple()
            )
            await ctx.send(embed=embed, delete_after=2)
        elif int(amount) <= 0:
            embed = discord.Embed(
                title='Error: The amount must be greater than 0',
                description=' ',
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed, delete_after=5)

    @prune.error
    async def prune_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='Error: Specify amount of messages to be deleted',
                description=' ',
                colour=discord.Colour.red()
            )
            embed.set_footer(text='ex => ;prune 10')
            await ctx.send(embed=embed, delete_after=5)

    # TODO: Add mute command
    # Create some function that applies a 'mute' role
    # Creates a 'mute' role if it does not previously exist
    # (Possibly easier to pre-make a mute role then apply it via function)
    @commands.command()
    # Limited to one server
    # @commands.has_role("The Elite 4")
    # Better, more general use
    @commands.has_guild_permissions(manage_roles=True)
    async def check(self, ctx):
        embed = discord.Embed(
            title='You are able to manage roles',
            description=' ',
            colour=discord.Colour.blurple()
        )
        await ctx.send(embed=embed)

    @check.error
    async def check_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                title='Error: You are not able to manage roles',
                description=' ',
                colour=discord.Colour.red()
            )
            await ctx.send(embed=embed, delete_after=5)

    # TODO: Add unmute command
    # This will either be a separate command that removes the 'mute' role
    # or will use the already made 'mute' command

    # If it uses the 'mute' command ==>
        # Create some sort of check that determines whether a user has the 'mute' role or not
        # If the user has the 'mute' role ==> Remove the role
    # If it uses a separate command ==>
        # Check if the user has the 'mute' role
        # If the user has the 'mute' role ==> Remove the role
        # If the user does not have the 'mute' role ==> Pass an error


# ---       END MAIN        ---#
def setup(bot):
    bot.add_cog(Admin(bot))
