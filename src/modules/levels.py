# ---       IMPORTS          ---#

import discord
from discord.ext import commands


# ---     CUSTOM CHECKS     --- #

def bot_channel_check(ctx):
    botspam_channels = ['bot-spam']
    if str(ctx.message.channel) in botspam_channels or ctx.author.id == 291005201840734218:
        return True


# ---       MAIN LINE       ---#

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def lvl_up(self, user):
        current_exp = user["user_xp"]
        current_level = user["user_level"]

        if current_exp >= round((4 * (current_level ** 3)) / 5):
            await self.bot.pg_con.execute(
                'UPDATE user_info SET user_level = $1 WHERE user_id = $2 AND guild_id = $3',
                current_level + 1, user["user_id"], user["guild_id"]
            )
            return True
        else:
            return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        author_id = str(message.author.id)
        guild_id = str(message.guild.id)

        user = await self.bot.pg_con.fetch(
            'SELECT * FROM user_info WHERE user_id = $1 AND guild_id = $2', author_id, guild_id
        )

        if not user:
            await self.bot.pg_con.execute(
                'INSERT INTO user_info (user_id, guild_id, user_level, user_xp) VALUES ($1, $2, 1, 0)', author_id, guild_id
            )
        user = await self.bot.pg_con.fetchrow(
            'SELECT * FROM user_info WHERE user_id = $1 AND guild_id = $2', author_id, guild_id
        )
        await self.bot.pg_con.execute(
            'UPDATE user_info SET user_xp = $1 WHERE user_id = $2 and guild_id = $3',
            user["user_xp"] + 1, author_id, guild_id
        )
        if await self.lvl_up(user):
            embed = discord.Embed(
                title=f'{message.author} is now level {user["user_level"] + 1}',
                description='',
                colour=discord.Colour.blurple()
            )
            await message.channel.send(embed=embed)

    @commands.command()
    @commands.check(bot_channel_check)
    async def level(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        member_id = str(member.id)
        guild_id = str(ctx.guild.id)

        user = await self.bot.pg_con.fetchrow(
            'SELECT * FROM user_info WHERE user_id = $1 AND guild_id = $2', member_id, guild_id
        )

        if not user:
            await ctx.send('Member does not have a level')
        else:
            embed = discord.Embed(
                title='',
                description='',
                colour=discord.Colour.blurple()
            )
            embed.add_field(name='Level', value=user[0]["user_level"])
            embed.add_field(name='EXP', value=user[0]["user_xp"])

            await ctx.send(embed=embed)


# ---       END MAIN        ---#
def setup(bot):
    bot.add_cog(Levels(bot))
