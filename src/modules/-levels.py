# THIS IS FOR PRODUCTION

# ---       IMPORTS          ---#

import discord
from discord.ext import commands
from pybo import conn, bot


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
            await self.bot.cur.execute(
                'UPDATE users set user_level = %s WHERE user_id = %s and guild_id = %s',
                current_level + 1, user["user_id"], user["guild_id"]
            )
            conn.commit()
            return True
        else:
            return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        author_id = str(message.author.id)
        guild_id = str(message.guild.id)

        user = bot.cur.execute(
            'SELECT user_id, guild_id FROM users WHERE user_id = %s and guild_id = %s', author_id, guild_id
        )

        if not user:
            await bot.cur.execute(
                'INSERT INTO users (user_id, guild_id, user_level, user_exp) VALUES (%s, %s, 1, 0)', author_id, guild_id
            )
        user = await bot.cur.execute(
            'SELECT * FROM users WHERE user_id = $1 AND guild_id = $2', author_id, guild_id
        )
        await bot.cur.execute(
            'UPDATE users SET user_xp = $1 WHERE user_id = $2 and guild_id = $3',
            user["user_xp"] + 1, author_id, guild_id
        )
        conn.commit()
        if await self.lvl_up(user):
            await message.channel.send(f'{message.author.mention} is now level {user["user_level"] + 1}')

    @commands.command()
    @commands.check(bot_channel_check)
    async def level(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        member_id = str(member.id)
        guild_id = str(ctx.guild.id)

        user = await bot.cur.fetchrow(
            'SELECT * FROM users WHERE user_id = $1 AND guild_id = $2', member_id, guild_id
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
